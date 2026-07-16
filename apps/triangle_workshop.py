#!/usr/bin/env python3
"""Local Streamlit interface for Demo 5."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from health_reserving import (  # noqa: E402
    TriangleConfig,
    build_results_zip,
    build_triangles,
    excel_sheet_names,
    parse_date_series,
    prepare_and_validate_claims,
    read_tabular_file,
)


NONE = "— No seleccionado —"
FREQUENCIES = {
    "Mensual": "M",
    "Trimestral": "Q",
    "Anual": "Y",
}
SENSITIVE_HINTS = (
    "nombre",
    "documento",
    "identificacion",
    "paciente",
    "afiliado",
    "correo",
    "email",
    "telefono",
    "direccion",
)


def normalize_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", normalized.lower()).strip("_")


def guessed_column(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    normalized = {normalize_name(column): column for column in columns}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    for candidate in candidates:
        for normalized_name, original in normalized.items():
            if candidate in normalized_name:
                return original
    return None


def column_selector(
    label: str,
    columns: list[str],
    candidates: tuple[str, ...],
    *,
    key: str,
    required: bool,
    help_text: str,
) -> str | None:
    options = [NONE, *columns]
    guess = guessed_column(columns, candidates)
    default = options.index(guess) if guess in options else 0
    selected = st.selectbox(label, options, index=default, key=key, help=help_text)
    if required and selected == NONE:
        st.caption("Campo requerido para continuar.")
    return None if selected == NONE else selected


def safe_preview(frame: pd.DataFrame) -> pd.DataFrame:
    preview = frame.head(10).iloc[:, :20].copy()
    for column in preview.columns:
        if any(hint in normalize_name(str(column)) for hint in SENSITIVE_HINTS):
            preview[column] = "••• oculto •••"
    return preview


def estimate_dates(
    frame: pd.DataFrame,
    origin_column: str,
    movement_column: str,
    frequency: str,
    dayfirst: bool,
) -> tuple[date, int]:
    origins = parse_date_series(frame[origin_column], dayfirst=dayfirst)
    movements = parse_date_series(frame[movement_column], dayfirst=dayfirst)
    maximum_date = movements.max()
    default_date = maximum_date.date() if pd.notna(maximum_date) else date.today()
    valid = origins.notna() & movements.notna() & movements.ge(origins)
    if not valid.any():
        return default_date, 0
    origin_periods = origins.loc[valid].dt.to_period(frequency)
    movement_periods = movements.loc[valid].dt.to_period(frequency)
    ages = movement_periods.astype("int64") - origin_periods.astype("int64")
    return default_date, max(0, int(ages.max()))


def dataframe_signature(frame_bytes: bytes, config: TriangleConfig) -> str:
    digest = hashlib.sha256()
    digest.update(frame_bytes)
    digest.update(json.dumps(config.to_dict(), sort_keys=True).encode("utf-8"))
    return digest.hexdigest()


def show_issues(prepared) -> None:
    issues = prepared.issues_frame()
    if issues.empty:
        st.success("Todos los controles iniciales fueron superados.")
        return
    st.dataframe(issues, width="stretch", hide_index=True)
    if prepared.has_blocking_issues:
        st.error(
            "El triángulo no fue construido. Corrige o confirma los controles "
            "bloqueantes y vuelve a ejecutar."
        )
    else:
        st.warning("El triángulo puede construirse, pero conserva las advertencias mostradas.")


def show_result(prepared, result, config: TriangleConfig) -> None:
    st.header("Resultado")
    diagnostics = result.diagnostics.set_index("indicador")["valor"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Periodos de origen", int(diagnostics["periodos_origen"]))
    col2.metric("Horizonte", int(diagnostics["horizonte_desarrollo"]))
    col3.metric("Celdas observadas", int(diagnostics["celdas_observadas"]))
    col4.metric("Reconciliación", str(diagnostics["estado_reconciliacion"]))

    if result.reconciled:
        st.success("El total de los datos canónicos reconcilia con el triángulo incremental.")
    else:
        st.error("La reconciliación falló. No utilices este resultado para modelación.")

    incremental_tab, cumulative_tab, long_tab, controls_tab, gates_tab = st.tabs(
        ["Incremental", "Acumulado", "Formato largo", "Diagnóstico", "Gates"]
    )
    with incremental_tab:
        st.caption("Los ceros son observados; las celdas vacías corresponden a desarrollo futuro.")
        st.dataframe(
            result.incremental.style.format("{:,.2f}", na_rep=""),
            width="stretch",
        )
    with cumulative_tab:
        st.caption("Cada celda es la suma de los incrementales observados hasta esa edad.")
        st.dataframe(
            result.cumulative.style.format("{:,.2f}", na_rep=""),
            width="stretch",
        )
    with long_tab:
        st.dataframe(result.aggregated_long, width="stretch", hide_index=True)
    with controls_tab:
        diagnostics_display = result.diagnostics.copy()
        diagnostics_display["valor"] = diagnostics_display["valor"].astype(str)
        st.dataframe(diagnostics_display, width="stretch", hide_index=True)
    with gates_tab:
        st.dataframe(result.gates, width="stretch", hide_index=True)
        if (result.gates["resultado"] == "NO_CUMPLE").any():
            st.warning(
                "Un triángulo descriptivo puede estar reconciliado y aun no cumplir "
                "los gates para modelación."
            )

    with st.expander("Ver la lógica Python aprendida en este paso"):
        st.code(
            """# 1. Crear periodos actuariales
datos["periodo_origen"] = datos["fecha_origen"].dt.to_period("M")
datos["periodo_calendario"] = datos["fecha_movimiento"].dt.to_period("M")

# 2. Calcular edad de desarrollo
datos["edad_desarrollo"] = (
    datos["periodo_calendario"].astype("int64")
    - datos["periodo_origen"].astype("int64")
)

# 3. Agregar y pivotar
triangulo_incremental = datos.pivot_table(
    index="periodo_origen",
    columns="edad_desarrollo",
    values="importe_incremental",
    aggfunc="sum",
)

# 4. Acumular sin convertir el futuro en cero
triangulo_acumulado = triangulo_incremental.cumsum(axis=1)
""",
            language="python",
        )

    st.subheader("Descargar resultados")
    include_detail = st.checkbox(
        "Incluir detalle canónico fila a fila en el ZIP",
        value=False,
        help="Déjalo desmarcado si los identificadores o movimientos son sensibles.",
    )
    package = build_results_zip(
        prepared,
        result,
        config,
        include_detail=include_detail,
    )
    st.download_button(
        "Descargar paquete de resultados",
        data=package,
        file_name="demo5_resultados_triangulos.zip",
        mime="application/zip",
        type="primary",
    )


st.set_page_config(
    page_title="Demo 5 · Triángulos actuariales",
    page_icon="📐",
    layout="wide",
)

st.title("Demo 5 · De datos propios a triángulos actuariales")
st.write(
    "Asistente educativo local para mapear, validar y transformar movimientos de reclamaciones "
    "en triángulos incrementales y acumulados."
)
st.info(
    "Privacidad: el archivo se procesa en esta sesión local. No se envía a GitHub ni se guarda "
    "automáticamente dentro del repositorio."
)

with st.sidebar:
    st.header("Alcance del MVP")
    st.markdown(
        """
        - CSV y XLSX
        - Pagos o medidas incrementales
        - Frecuencia mensual, trimestral o anual
        - Un segmento por ejecución
        - Triángulos incremental y acumulado
        - Validación, gates y reconciliación

        **No estima todavía ultimate ni IBNR.**
        """
    )
    if st.button("Borrar resultados de la sesión"):
        for state_key in ("demo5_prepared", "demo5_result", "demo5_signature", "demo5_config"):
            st.session_state.pop(state_key, None)
        st.success("Resultados eliminados de la memoria de la sesión.")

st.header("1. Selecciona los datos")
source_mode = st.radio(
    "Fuente",
    ["Aprender con el ejemplo incluido", "Usar mi archivo local"],
    horizontal=True,
)

uploaded = None
if source_mode == "Usar mi archivo local":
    uploaded = st.file_uploader(
        "Selecciona un CSV o XLSX",
        type=["csv", "xlsx"],
        help="Para este MVP utiliza archivos de hasta 200 MB.",
    )
    if uploaded is None:
        st.stop()
    filename = uploaded.name
    source = uploaded
    source_bytes = uploaded.getvalue()
else:
    sample = (
        ROOT
        / "data"
        / "demo_triangulos_mensuales"
        / "reclamaciones_pagadas_mensuales_largo.csv"
    )
    filename = sample.name
    source = sample
    source_bytes = sample.read_bytes()
    st.caption(f"Ejemplo sintético: `{sample.relative_to(ROOT)}`")

suffix = Path(filename).suffix.lower()
separator = ","
decimal = "."
thousands = None
encoding = "utf-8"
sheet_name: str | int = 0

with st.expander("Opciones de lectura", expanded=False):
    if suffix == ".csv":
        separator_label = st.selectbox(
            "Separador de columnas", ["Coma (,) ", "Punto y coma (;)", "Tabulación", "Detectar"]
        )
        separator = {
            "Coma (,) ": ",",
            "Punto y coma (;)": ";",
            "Tabulación": "\t",
            "Detectar": "auto",
        }[separator_label]
        decimal = st.selectbox("Separador decimal", [".", ","])
        thousands_label = st.selectbox("Separador de miles", ["Ninguno", ",", ".", "Espacio"])
        thousands = {"Ninguno": None, ",": ",", ".": ".", "Espacio": " "}[thousands_label]
        encoding = st.selectbox("Codificación", ["utf-8", "utf-8-sig", "latin-1"])
    else:
        try:
            sheets = excel_sheet_names(source)
            sheet_name = st.selectbox("Hoja de Excel", sheets)
        except Exception as exc:
            st.error(f"No fue posible inspeccionar el archivo Excel: {exc}")
            st.stop()

try:
    data = read_tabular_file(
        source,
        filename,
        sheet_name=sheet_name,
        separator=separator,
        decimal=decimal,
        thousands=thousands,
        encoding=encoding,
    )
except Exception as exc:
    st.error(f"No fue posible leer el archivo: {exc}")
    st.stop()

col1, col2 = st.columns(2)
col1.metric("Filas", f"{len(data):,}")
col2.metric("Columnas", len(data.columns))
st.dataframe(safe_preview(data), width="stretch", hide_index=True)
if len(data.columns) > 20:
    st.caption("La vista preliminar muestra solamente las primeras 20 columnas.")

st.header("2. Mapea tus columnas")
columns = list(data.columns)
left, middle, right = st.columns(3)
with left:
    origin_column = column_selector(
        "Fecha de origen *",
        columns,
        ("mes_origen", "periodo_origen", "fecha_servicio", "fecha_origen", "fecha_ocurrencia"),
        key="origin_column",
        required=True,
        help_text="Fecha de servicio, ocurrencia, egreso u otra definición declarada.",
    )
with middle:
    movement_column = column_selector(
        "Fecha de movimiento *",
        columns,
        (
            "mes_pago",
            "fecha_pago",
            "fecha_movimiento",
            "periodo_calendario",
            "fecha_contabilizacion",
        ),
        key="movement_column",
        required=True,
        help_text="Fecha de pago o del movimiento que define el eje calendario.",
    )
with right:
    amount_column = column_selector(
        "Importe incremental *",
        columns,
        ("pago_incremental", "importe_incremental", "costo_pagado", "valor_pagado", "costo"),
        key="amount_column",
        required=True,
        help_text="Movimiento del periodo; no debe ser un saldo acumulado por fila.",
    )

left, middle, right = st.columns(3)
with left:
    id_column = column_selector(
        "Identificador de movimiento",
        columns,
        ("id_movimiento", "id_transaccion", "transaction_id", "folio"),
        key="id_column",
        required=False,
        help_text="Recomendado para detectar duplicados con mayor precisión.",
    )
with middle:
    movement_type_column = column_selector(
        "Tipo de movimiento",
        columns,
        ("tipo_movimiento", "componente", "movement_type"),
        key="movement_type_column",
        required=False,
        help_text="Pago, reverso, recuperación, glosa u otra clasificación.",
    )
with right:
    segment_column = column_selector(
        "Segmento",
        columns,
        ("segmento", "producto", "cobertura", "tipo_servicio", "region"),
        key="segment_column",
        required=False,
        help_text="Permite ejecutar el análisis para una población homogénea.",
    )

segment_value = None
if segment_column:
    segment_values = sorted(data[segment_column].dropna().astype(str).unique().tolist())
    segment_choice = st.selectbox("Población a procesar", ["Todos los segmentos", *segment_values])
    if segment_choice != "Todos los segmentos":
        segment_value = segment_choice

st.header("3. Define el alcance actuarial")
left, middle, right = st.columns(3)
with left:
    frequency_label = st.selectbox("Periodicidad", list(FREQUENCIES))
    frequency = FREQUENCIES[frequency_label]
    dayfirst = st.checkbox("Fechas con día primero", value=True, help="Ejemplo: 31/12/2025")
with middle:
    try:
        default_valuation, observed_development = estimate_dates(
            data, origin_column, movement_column, frequency, dayfirst
        )
    except Exception:
        default_valuation, observed_development = date.today(), 0
    valuation_date = st.date_input("Fecha de valoración", value=default_valuation)
    maximum_development = st.number_input(
        "Edad máxima de desarrollo",
        min_value=0,
        value=observed_development,
        step=1,
        help="No puede ser menor que la última edad con movimientos observados.",
        key=f"max_dev_{frequency}_{origin_column}_{movement_column}",
    )
with right:
    currency = st.text_input("Moneda", value="COP").strip().upper() or "COP"
    allow_negative_amounts = st.checkbox(
        "Incluir negativos clasificados",
        value=False,
        help="Actívalo solo si reversos, recuperaciones o ajustes fueron revisados.",
    )

st.subheader("Confirmaciones de negocio")
st.caption(
    "Estas confirmaciones no pueden inferirse únicamente a partir del nombre de las columnas."
)
c1, c2 = st.columns(2)
with c1:
    obligation_defined = st.checkbox("La obligación y la medida objetivo están definidas")
    origin_confirmed = st.checkbox("Confirmo la semántica de la fecha de origen")
    movement_confirmed = st.checkbox("Confirmo la semántica de la fecha de movimiento")
with c2:
    amount_confirmed = st.checkbox("El importe es incremental y corresponde a la medida")
    complete_through_valuation = st.checkbox("El archivo está completo hasta la valoración")
    representative_history = st.checkbox("La historia es representativa del proceso actual")

try:
    config = TriangleConfig(
        origin_column=origin_column or "",
        movement_column=movement_column or "",
        amount_column=amount_column or "",
        valuation_date=str(valuation_date),
        frequency=frequency,
        maximum_development=int(maximum_development),
        id_column=id_column,
        movement_type_column=movement_type_column,
        segment_column=segment_column,
        segment_value=segment_value,
        dayfirst=dayfirst,
        allow_negative_amounts=allow_negative_amounts,
        obligation_defined=obligation_defined,
        origin_semantics_confirmed=origin_confirmed,
        movement_semantics_confirmed=movement_confirmed,
        amount_semantics_confirmed=amount_confirmed,
        complete_through_valuation=complete_through_valuation,
        representative_history=representative_history,
        currency=currency,
    )
except ValueError as exc:
    st.error(str(exc))
    st.stop()

current_signature = dataframe_signature(source_bytes, config)
if st.button("Validar y construir triángulos", type="primary"):
    try:
        prepared = prepare_and_validate_claims(data, config)
        result = None if prepared.has_blocking_issues else build_triangles(prepared, config)
        st.session_state["demo5_prepared"] = prepared
        st.session_state["demo5_result"] = result
        st.session_state["demo5_signature"] = current_signature
        st.session_state["demo5_config"] = config
    except Exception as exc:
        st.error(f"La ejecución se detuvo de forma segura: {exc}")

if st.session_state.get("demo5_signature") == current_signature:
    stored_prepared = st.session_state.get("demo5_prepared")
    stored_result = st.session_state.get("demo5_result")
    stored_config = st.session_state.get("demo5_config")
    if stored_prepared is not None:
        st.header("4. Validaciones")
        show_issues(stored_prepared)
    if stored_result is not None:
        show_result(stored_prepared, stored_result, stored_config)
elif st.session_state.get("demo5_signature"):
    st.warning(
        "La configuración cambió. Ejecuta nuevamente la validación para actualizar los resultados."
    )

st.divider()
st.caption(
    "Uso educativo. La construcción de un triángulo no sustituye validación actuarial, "
    "reconciliación contable, gobierno del modelo ni revisión regulatoria."
)
