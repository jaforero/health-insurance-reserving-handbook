#!/usr/bin/env python3
"""Local Streamlit interface for Demo 6 deterministic Chain Ladder."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from health_reserving import (  # noqa: E402
    SELECTION_LABELS,
    ChainLadderConfig,
    build_chain_ladder_zip,
    compare_factor_methods,
    fit_chain_ladder,
    load_demo5_triangle_package,
)
from health_reserving.ui_theme import (  # noqa: E402
    configure_page,
    inject_corporate_theme,
    render_brand_hero,
    render_corporate_footer,
    render_kpi_grid,
    render_sidebar_brand,
)


METHOD_BY_LABEL = {label: method for method, label in SELECTION_LABELS.items()}
SAMPLE = ROOT / "data" / "demo_triangulos_mensuales" / "triangulo_pagado_mensual_acumulado.csv"


def run_signature(
    cumulative: pd.DataFrame,
    mask: pd.DataFrame,
    config: ChainLadderConfig,
) -> str:
    """Return a deterministic signature for inputs and assumptions."""

    digest = hashlib.sha256()
    digest.update(cumulative.to_csv(index=True, lineterminator="\n").encode("utf-8"))
    digest.update(mask.astype(int).to_csv(index=True, lineterminator="\n").encode("utf-8"))
    digest.update(json.dumps(config.to_dict(), sort_keys=True).encode("utf-8"))
    return digest.hexdigest()


def money(value: float, currency: str) -> str:
    grouped = f"{value:,.0f}".replace(",", ".")
    return f"{currency} {grouped}"


def metric_value(result, indicator: str) -> float:
    row = result.totals.loc[result.totals["indicador"].eq(indicator), "valor"]
    return float(row.iloc[0])


def display_diagnostics(result) -> None:
    warnings = result.diagnostics.loc[result.diagnostics["nivel"].eq("ADVERTENCIA")]
    if warnings.empty:
        st.success("Los diagnósticos automáticos no identificaron alertas.")
    else:
        for row in warnings.itertuples(index=False):
            st.warning(f"{row.codigo}: {row.mensaje} Valor: {row.valor}")
    with st.expander("Ver todos los diagnósticos", expanded=False):
        st.dataframe(result.diagnostics, width="stretch", hide_index=True)


def display_result(
    result,
    sensitivity: pd.DataFrame,
    config: ChainLadderConfig,
    source_metadata: dict[str, Any],
) -> None:
    currency = config.currency
    observed = metric_value(result, "acumulado_observado_total")
    ultimate = metric_value(result, "ultimate_total")
    ibnr = metric_value(result, "ibnr_total")
    ratio = metric_value(result, "ibnr_sobre_ultimate")

    st.header("3. Revisa factores y diagnósticos")
    st.caption(
        "Los candidatos son referencias automáticas. La selección final debe justificarse con "
        "contexto operativo, suficiencia, estabilidad y materialidad."
    )
    factor_view = result.factor_summary.copy()
    numeric_columns = [
        "factor_ponderado",
        "promedio_simple",
        "mediana",
        "promedio_ultimos_3",
        "cv_ratios_individuales",
        "factor_seleccionado",
    ]
    factor_view[numeric_columns] = factor_view[numeric_columns].round(6)
    st.dataframe(factor_view, width="stretch", hide_index=True)
    st.line_chart(
        factor_view.set_index("enlace")[["factor_seleccionado"]],
        y_label="Factor seleccionado",
    )
    display_diagnostics(result)

    with st.expander("Ratios individuales por periodo de origen", expanded=False):
        st.dataframe(result.individual_factors.round(6), width="stretch")

    st.subheader("Sensibilidad por método automático")
    sensitivity_view = sensitivity.copy()
    sensitivity_view["ultimate_total"] = sensitivity_view["ultimate_total"].round(2)
    sensitivity_view["ibnr_total"] = sensitivity_view["ibnr_total"].round(2)
    sensitivity_view["diferencia_ibnr_vs_ponderado"] = sensitivity_view[
        "diferencia_ibnr_vs_ponderado"
    ].round(2)
    st.dataframe(sensitivity_view, width="stretch", hide_index=True)

    st.header("4. Interpreta ultimate e IBNR")
    render_kpi_grid(
        (
            ("Acumulado observado", money(observed, currency)),
            ("Ultimate estimado", money(ultimate, currency)),
            ("IBNR estimado", money(ibnr, currency)),
            ("IBNR / ultimate", f"{ratio:.1%}".replace(".", ",")),
        )
    )

    summary_view = result.origin_summary.reset_index()
    st.dataframe(summary_view, width="stretch", hide_index=True)
    st.bar_chart(
        result.origin_summary[["ibnr"]],
        y_label=f"IBNR ({currency})",
        x_label="Periodo de origen",
    )

    observed_tab, projected_tab, incremental_tab = st.tabs(
        ["Acumulado observado", "Acumulado proyectado", "Incremental proyectado"]
    )
    with observed_tab:
        st.dataframe(result.observed_cumulative, width="stretch")
    with projected_tab:
        st.dataframe(result.projected_cumulative, width="stretch")
    with incremental_tab:
        st.dataframe(result.projected_incremental, width="stretch")

    package = build_chain_ladder_zip(
        result,
        config,
        source_metadata=source_metadata,
    )
    st.download_button(
        "Descargar resultados Chain Ladder",
        data=package,
        file_name="demo6_resultados_chain_ladder.zip",
        mime="application/zip",
        type="primary",
    )
    st.info(
        "El resultado es determinístico. No incluye error de predicción de Mack, bootstrap ni "
        "intervalos de confianza."
    )


configure_page("Demo 6 · Chain Ladder")
inject_corporate_theme()
render_brand_hero(
    "Demo 6",
    "Del triángulo a ultimate e IBNR",
    (
        "Asistente educativo local para estimar factores edad-a-edad, completar el triángulo "
        "acumulado y calcular ultimate e IBNR mediante Chain Ladder determinístico."
    ),
    tags=("Chain Ladder", "Selección trazable", "Datos agregados"),
)
st.info(
    "Privacidad: Demo 6 trabaja con triángulos agregados. El archivo seleccionado se procesa en "
    "la sesión local y no se envía a GitHub."
)

with st.sidebar:
    render_sidebar_brand()
    st.header("Alcance de Demo 6")
    st.markdown(
        """
        - Triángulos acumulados de Demo 5
        - Factores individuales y candidatos
        - Selección automática o manual
        - Factor de cola explícito
        - Ultimate, IBNR y sensibilidad
        - Exportación reproducible

        **No cuantifica todavía incertidumbre estocástica.**
        """
    )
    if st.button("Borrar resultados Chain Ladder"):
        for state_key in (
            "demo6_result",
            "demo6_sensitivity",
            "demo6_signature",
            "demo6_config",
            "demo6_source_metadata",
        ):
            st.session_state.pop(state_key, None)
        st.success("Resultados eliminados de la memoria de la sesión.")

st.header("1. Selecciona el triángulo acumulado")
source_mode = st.radio(
    "Fuente",
    ["Aprender con el ejemplo mensual", "Usar un paquete ZIP de Demo 5"],
    horizontal=True,
)

if source_mode == "Aprender con el ejemplo mensual":
    cumulative = pd.read_csv(SAMPLE, index_col=0)
    mask = cumulative.notna()
    source_metadata: dict[str, Any] = {
        "tipo": "ejemplo_sintetico",
        "ruta": str(SAMPLE.relative_to(ROOT)),
    }
    default_currency = "COP"
    st.caption(f"Ejemplo sintético: `{SAMPLE.relative_to(ROOT)}`")
else:
    uploaded = st.file_uploader(
        "Selecciona el paquete ZIP descargado desde Demo 5",
        type=["zip"],
        help="Debe contener el triángulo acumulado, la máscara, configuración y manifiesto.",
    )
    if uploaded is None:
        st.stop()
    try:
        triangle_package = load_demo5_triangle_package(uploaded)
    except Exception as exc:
        st.error(f"No fue posible validar el paquete de Demo 5: {exc}")
        st.stop()
    cumulative = triangle_package.cumulative
    mask = triangle_package.observed_mask
    source_metadata = {
        "tipo": "paquete_demo5_verificado",
        "hash_datos_agregados_sha256": triangle_package.manifest.get("hash_datos_agregados_sha256"),
        "version_motor_demo5": triangle_package.manifest.get("version_motor"),
    }
    default_currency = str(triangle_package.triangle_config.get("currency", "COP"))
    st.success("Paquete de Demo 5 verificado: manifiesto, hash y reconciliación correctos.")

col1, col2, col3 = st.columns(3)
col1.metric("Periodos de origen", len(cumulative))
col2.metric("Edades de desarrollo", len(cumulative.columns))
col3.metric("Celdas observadas", int(mask.sum().sum()))
st.dataframe(cumulative, width="stretch")

st.header("2. Selecciona los factores")
left, middle, right = st.columns(3)
with left:
    selection_label = st.selectbox("Método de selección", list(METHOD_BY_LABEL))
    selection_method = METHOD_BY_LABEL[selection_label]
with middle:
    tail_factor = st.number_input(
        "Factor de cola",
        min_value=0.000001,
        value=1.0,
        step=0.001,
        format="%.6f",
        help="Se aplica después de la última edad visible. Uno significa sin cola adicional.",
    )
with right:
    minimum_observations = st.number_input(
        "Mínimo de observaciones por enlace",
        min_value=1,
        value=3,
        step=1,
        help="Heurística configurable para activar alertas; no es un estándar universal.",
    )

currency = st.text_input("Moneda", value=default_currency).strip().upper() or "COP"
manual_factors = None
if selection_method == "manual":
    try:
        automatic = fit_chain_ladder(
            cumulative,
            mask,
            ChainLadderConfig(
                selection_method="volume_weighted",
                tail_factor=float(tail_factor),
                minimum_observations=int(minimum_observations),
            ),
        )
    except Exception as exc:
        st.error(f"No fue posible preparar la selección manual: {exc}")
        st.stop()
    editor = automatic.factor_summary[["enlace", "factor_ponderado"]].rename(
        columns={"factor_ponderado": "factor_seleccionado"}
    )
    edited = st.data_editor(
        editor,
        width="stretch",
        hide_index=True,
        disabled=["enlace"],
        num_rows="fixed",
    )
    manual_factors = {
        str(row.enlace): float(row.factor_seleccionado) for row in edited.itertuples(index=False)
    }

try:
    config = ChainLadderConfig(
        selection_method=selection_method,
        tail_factor=float(tail_factor),
        minimum_observations=int(minimum_observations),
        manual_factors=manual_factors,
        currency=currency,
    )
except ValueError as exc:
    st.error(str(exc))
    st.stop()

review_confirmed = st.checkbox(
    "Confirmo que revisé la representatividad histórica, los factores seleccionados y la cola"
)
current_signature = run_signature(cumulative, mask, config)
if st.button("Estimar ultimate e IBNR", type="primary"):
    if not review_confirmed:
        st.error("Confirma la revisión actuarial de factores y cola antes de estimar.")
    else:
        try:
            result = fit_chain_ladder(cumulative, mask, config)
            sensitivity = compare_factor_methods(
                cumulative,
                mask,
                tail_factor=config.tail_factor,
                minimum_observations=config.minimum_observations,
            )
            st.session_state["demo6_result"] = result
            st.session_state["demo6_sensitivity"] = sensitivity
            st.session_state["demo6_signature"] = current_signature
            st.session_state["demo6_config"] = config
            st.session_state["demo6_source_metadata"] = source_metadata
        except Exception as exc:
            st.error(f"La estimación se detuvo de forma segura: {exc}")

if st.session_state.get("demo6_signature") == current_signature:
    stored_result = st.session_state.get("demo6_result")
    stored_sensitivity = st.session_state.get("demo6_sensitivity")
    stored_config = st.session_state.get("demo6_config")
    stored_metadata = st.session_state.get("demo6_source_metadata")
    if stored_result is not None:
        display_result(stored_result, stored_sensitivity, stored_config, stored_metadata)
elif st.session_state.get("demo6_signature"):
    st.warning("Los factores o datos cambiaron. Ejecuta nuevamente la estimación.")

render_corporate_footer(
    "Uso educativo. Chain Ladder requiere validación de datos, supuestos, factores, cola, "
    "reconciliación y gobierno del modelo antes de cualquier uso profesional."
)
