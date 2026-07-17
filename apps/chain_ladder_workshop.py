#!/usr/bin/env python3
"""Local Streamlit interface for Demo 6 deterministic Chain Ladder."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import altair as alt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from health_reserving import (  # noqa: E402
    PRIOR_MODE_LABELS,
    SELECTION_LABELS,
    BornhuetterFergusonConfig,
    ChainLadderConfig,
    build_chain_ladder_zip,
    build_classical_methods_zip,
    compare_factor_methods,
    excel_sheet_names,
    fit_bornhuetter_ferguson,
    fit_chain_ladder,
    load_demo5_triangle_package,
    read_tabular_file,
)
from health_reserving.ui_theme import (  # noqa: E402
    configure_page,
    inject_corporate_theme,
    render_brand_hero,
    render_corporate_footer,
    render_kpi_grid,
    render_method_comparison,
    render_sidebar_brand,
)


METHOD_BY_LABEL = {label: method for method, label in SELECTION_LABELS.items()}
PRIOR_MODE_BY_LABEL = {label: mode for mode, label in PRIOR_MODE_LABELS.items()}
SAMPLE = ROOT / "data" / "demo_triangulos_mensuales" / "triangulo_pagado_mensual_acumulado.csv"
SAMPLE_PRIOR = (
    ROOT / "data" / "demo_triangulos_mensuales" / "prior_bornhuetter_ferguson_mensual.csv"
)
VISUAL_BUILD = "Sprint 2 · comparación visual 0.2.2"


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


def bf_run_signature(
    chain_ladder_signature: str,
    prior: pd.DataFrame,
    config: BornhuetterFergusonConfig,
) -> str:
    """Return a deterministic signature for the CL run, prior and BF assumptions."""

    digest = hashlib.sha256(chain_ladder_signature.encode("utf-8"))
    digest.update(prior.to_csv(index=True, lineterminator="\n").encode("utf-8"))
    digest.update(json.dumps(config.to_dict(), sort_keys=True).encode("utf-8"))
    return digest.hexdigest()


def money(value: float, currency: str) -> str:
    grouped = f"{value:,.0f}".replace(",", ".")
    return f"{currency} {grouped}"


def signed_money(value: float, currency: str) -> str:
    """Format a signed amount with the sign before the currency."""

    if value > 0:
        sign = "+"
    elif value < 0:
        sign = "−"
    else:
        sign = ""
    grouped = f"{abs(value):,.0f}".replace(",", ".")
    return f"{sign}{currency} {grouped}"


def signed_percentage(value: float) -> str:
    """Format a signed ratio using Spanish decimal punctuation."""

    if value > 0:
        sign = "+"
    elif value < 0:
        sign = "−"
    else:
        sign = ""
    return f"{sign}{abs(value):.2%}".replace(".", ",")


def metric_value(result, indicator: str) -> float:
    row = result.totals.loc[result.totals["indicador"].eq(indicator), "valor"]
    return float(row.iloc[0])


def method_comparison_charts(
    comparison: pd.DataFrame,
    currency: str,
) -> tuple[alt.Chart, alt.LayerChart]:
    """Build non-stacked CL/BF trajectory and signed-difference charts."""

    plot_frame = comparison.reset_index()
    origin_column = str(plot_frame.columns[0])
    plot_frame = plot_frame.rename(columns={origin_column: "periodo_origen"})
    plot_frame["periodo_origen"] = plot_frame["periodo_origen"].astype(str)
    origin_order = plot_frame["periodo_origen"].tolist()

    series = plot_frame.melt(
        id_vars="periodo_origen",
        value_vars=["ibnr_chain_ladder", "ibnr_bf"],
        var_name="metodo",
        value_name="ibnr",
    )
    series["metodo"] = series["metodo"].map(
        {
            "ibnr_chain_ladder": "Chain Ladder",
            "ibnr_bf": "Bornhuetter-Ferguson",
        }
    )
    method_domain = ["Chain Ladder", "Bornhuetter-Ferguson"]
    axis = alt.Axis(labelAngle=-45, labelOverlap="greedy", title="Periodo de origen")
    trajectory = (
        alt.Chart(series)
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=24), strokeWidth=2.2)
        .encode(
            x=alt.X("periodo_origen:O", sort=origin_order, axis=axis),
            y=alt.Y(
                "ibnr:Q",
                title=f"IBNR ({currency})",
                scale=alt.Scale(zero=True),
                axis=alt.Axis(format="~s"),
            ),
            color=alt.Color(
                "metodo:N",
                title="Método",
                sort=method_domain,
                scale=alt.Scale(domain=method_domain, range=["#260080", "#526cfe"]),
            ),
            strokeDash=alt.StrokeDash(
                "metodo:N",
                sort=method_domain,
                scale=alt.Scale(domain=method_domain, range=[[1, 0], [6, 3]]),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("periodo_origen:N", title="Periodo de origen"),
                alt.Tooltip("metodo:N", title="Método"),
                alt.Tooltip("ibnr:Q", title=f"IBNR ({currency})", format=",.0f"),
            ],
        )
        .properties(height=320)
    )

    difference_frame = plot_frame[
        ["periodo_origen", "ibnr_chain_ladder", "diferencia_ibnr_bf_vs_cl"]
    ].copy()
    difference_frame["diferencia_relativa_vs_cl"] = difference_frame[
        "diferencia_ibnr_bf_vs_cl"
    ].div(difference_frame["ibnr_chain_ladder"].where(difference_frame["ibnr_chain_ladder"].ne(0)))
    bars = (
        alt.Chart(difference_frame)
        .mark_bar()
        .encode(
            x=alt.X("periodo_origen:O", sort=origin_order, axis=axis),
            y=alt.Y(
                "diferencia_ibnr_bf_vs_cl:Q",
                title=f"Diferencia BF − CL ({currency})",
                scale=alt.Scale(zero=True),
                axis=alt.Axis(format="~s"),
            ),
            color=alt.condition(
                alt.datum.diferencia_ibnr_bf_vs_cl >= 0,
                alt.value("#4e00ff"),
                alt.value("#9b90b4"),
            ),
            tooltip=[
                alt.Tooltip("periodo_origen:N", title="Periodo de origen"),
                alt.Tooltip(
                    "diferencia_ibnr_bf_vs_cl:Q",
                    title=f"BF − CL ({currency})",
                    format="+,.0f",
                ),
                alt.Tooltip(
                    "diferencia_relativa_vs_cl:Q",
                    title="BF − CL / IBNR CL",
                    format="+.2%",
                ),
            ],
        )
    )
    zero_line = (
        alt.Chart(pd.DataFrame({"cero": [0.0]}))
        .mark_rule(color="#1f2430", strokeWidth=1)
        .encode(y="cero:Q")
    )
    difference = (bars + zero_line).properties(height=220)
    return trajectory, difference


def select_prior_column(
    label: str,
    columns: list[str],
    candidates: tuple[str, ...],
    *,
    key: str,
) -> str:
    """Render a column selector with a deterministic best-effort suggestion."""

    normalised = {str(column).strip().lower(): position for position, column in enumerate(columns)}
    suggested = next(
        (
            normalised[candidate.lower()]
            for candidate in candidates
            if candidate.lower() in normalised
        ),
        0,
    )
    return str(st.selectbox(label, columns, index=suggested, key=key))


def load_prior_data(use_sample: bool) -> tuple[pd.DataFrame | None, dict[str, Any] | None]:
    """Read a synthetic or local prior without persisting its source file."""

    if use_sample:
        source = SAMPLE_PRIOR
        filename = source.name
        metadata: dict[str, Any] = {
            "tipo": "prior_sintetico_incluido",
            "ruta": str(source.relative_to(ROOT)),
            "hash_archivo_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }
        st.caption(f"Prior sintético: `{source.relative_to(ROOT)}`")
    else:
        uploaded = st.file_uploader(
            "Selecciona el archivo de prior o exposición",
            type=["csv", "txt", "xlsx", "parquet", "pq"],
            key="bf_prior_upload",
            help="Una fila por periodo de origen; máximo 200 MB para este demo local.",
        )
        if uploaded is None:
            st.info("Carga un archivo para continuar con Bornhuetter-Ferguson.")
            return None, None
        source = uploaded
        filename = uploaded.name
        metadata = {
            "tipo": "archivo_local_prior",
            "nombre_archivo": filename,
            "hash_archivo_sha256": hashlib.sha256(uploaded.getvalue()).hexdigest(),
        }

    suffix = Path(filename).suffix.lower()
    separator = ","
    decimal = "."
    thousands = None
    encoding = "utf-8"
    sheet_name: str | int = 0
    with st.expander("Opciones de lectura del prior", expanded=False):
        if suffix in {".csv", ".txt"}:
            separator_label = st.selectbox(
                "Separador de columnas del prior",
                ["Coma (,)", "Punto y coma (;)", "Tabulación", "Barra vertical (|)", "Detectar"],
                key="bf_separator",
            )
            separator = {
                "Coma (,)": ",",
                "Punto y coma (;)": ";",
                "Tabulación": "\t",
                "Barra vertical (|)": "|",
                "Detectar": "auto",
            }[separator_label]
            decimal = st.selectbox("Separador decimal del prior", [".", ","], key="bf_decimal")
            thousands_label = st.selectbox(
                "Separador de miles del prior",
                ["Ninguno", ",", ".", "Espacio"],
                key="bf_thousands",
            )
            thousands = {"Ninguno": None, ",": ",", ".": ".", "Espacio": " "}[thousands_label]
            encoding = st.selectbox(
                "Codificación del prior",
                ["utf-8", "utf-8-sig", "latin-1"],
                key="bf_encoding",
            )
        elif suffix == ".xlsx":
            try:
                sheets = excel_sheet_names(source)
                sheet_name = st.selectbox("Hoja del prior", sheets, key="bf_sheet")
            except Exception as exc:
                st.error(f"No fue posible inspeccionar el archivo Excel: {exc}")
                return None, None
        else:
            st.caption("Parquet conserva sus tipos y no requiere opciones de texto.")

    try:
        frame = read_tabular_file(
            source,
            filename,
            sheet_name=sheet_name,
            separator=separator,
            decimal=decimal,
            thousands=thousands,
            encoding=encoding,
        )
    except Exception as exc:
        st.error(f"No fue posible leer el prior: {exc}")
        return None, None
    return frame, metadata


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
    origin_order = summary_view["periodo_origen"].astype(str).tolist()
    chain_ladder_chart = (
        alt.Chart(summary_view.assign(periodo_origen=summary_view["periodo_origen"].astype(str)))
        .mark_bar(color="#4e00ff")
        .encode(
            x=alt.X(
                "periodo_origen:O",
                sort=origin_order,
                title="Periodo de origen",
                axis=alt.Axis(labelAngle=-45, labelOverlap="greedy"),
            ),
            y=alt.Y(
                "ibnr:Q",
                title=f"IBNR ({currency})",
                scale=alt.Scale(zero=True),
                axis=alt.Axis(format="~s"),
            ),
            tooltip=[
                alt.Tooltip("periodo_origen:N", title="Periodo de origen"),
                alt.Tooltip("ibnr:Q", title=f"IBNR ({currency})", format=",.0f"),
            ],
        )
        .properties(height=280)
    )
    st.altair_chart(chain_ladder_chart, width="stretch")

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


def display_bf_result(
    result,
    chain_ladder_result,
    chain_ladder_config: ChainLadderConfig,
    source_metadata: dict[str, Any],
    prior_metadata: dict[str, Any],
) -> None:
    """Render BF comparison, sensitivity, diagnostics and the joint export."""

    currency = chain_ladder_config.currency
    observed = metric_value(result, "acumulado_observado_total")
    ultimate_cl = metric_value(result, "ultimate_chain_ladder_total")
    ultimate_bf = metric_value(result, "ultimate_bf_total")
    ibnr_cl = metric_value(result, "ibnr_chain_ladder_total")
    ibnr_bf = metric_value(result, "ibnr_bf_total")
    difference = metric_value(result, "diferencia_ibnr_bf_vs_cl_total")
    ratio_cl = ibnr_cl / ultimate_cl if ultimate_cl else 0.0
    ratio_bf = ibnr_bf / ultimate_bf if ultimate_bf else 0.0
    relative_difference = difference / ibnr_cl if ibnr_cl else 0.0

    st.header("6. Compara Chain Ladder y Bornhuetter-Ferguson")
    st.caption(
        "El acumulado observado es la misma base para ambos métodos. Las tarjetas conservan "
        "idéntica jerarquía para que ultimate e IBNR puedan compararse sin sugerir aditividad."
    )
    render_method_comparison(
        ("Base común · Acumulado observado", money(observed, currency)),
        (
            (
                "Chain Ladder",
                (
                    ("Ultimate", money(ultimate_cl, currency)),
                    ("IBNR", money(ibnr_cl, currency)),
                    ("IBNR / ultimate", f"{ratio_cl:.2%}".replace(".", ",")),
                ),
            ),
            (
                "Bornhuetter-Ferguson",
                (
                    ("Ultimate", money(ultimate_bf, currency)),
                    ("IBNR", money(ibnr_bf, currency)),
                    ("IBNR / ultimate", f"{ratio_bf:.2%}".replace(".", ",")),
                ),
            ),
        ),
        (
            "Diferencia de IBNR · BF − CL",
            signed_money(difference, currency),
            f"{signed_percentage(relative_difference)} respecto al IBNR Chain Ladder",
        ),
    )

    comparison = result.origin_summary[
        [
            "ultimate_chain_ladder",
            "ultimate_bf",
            "ibnr_chain_ladder",
            "ibnr_bf",
            "diferencia_ibnr_bf_vs_cl",
        ]
    ]
    trajectory_chart, difference_chart = method_comparison_charts(comparison, currency)
    st.subheader("IBNR por periodo de origen")
    st.caption(
        "Las líneas son estimaciones alternativas de la misma magnitud y utilizan una escala "
        "común desde cero; no deben sumarse ni apilarse."
    )
    st.altair_chart(trajectory_chart, width="stretch")

    st.subheader("Diferencia por periodo de origen")
    st.caption(
        "Cada barra representa BF − CL con una línea cero. Valores positivos indican mayor IBNR "
        "BF y valores negativos, menor IBNR BF. Como el observado es común, la diferencia de "
        "ultimate es exactamente igual a la diferencia de IBNR."
    )
    st.altair_chart(difference_chart, width="stretch")

    with st.expander("Ver comparación numérica por periodo", expanded=False):
        st.dataframe(comparison.reset_index(), width="stretch", hide_index=True)

    st.subheader("Sensibilidad a la expectativa previa")
    sensitivity = result.sensitivity.copy()
    amount_columns = [
        "ultimate_esperado_prior_total",
        "ultimate_bf_total",
        "ibnr_bf_total",
        "diferencia_ibnr_vs_base",
        "diferencia_ultimate_vs_base",
    ]
    sensitivity[amount_columns] = sensitivity[amount_columns].round(2)
    st.dataframe(sensitivity, width="stretch", hide_index=True)
    st.line_chart(
        sensitivity.set_index("escenario")[["ibnr_bf_total"]],
        y_label=f"IBNR BF ({currency})",
        x_label="Escenario del prior",
    )

    st.subheader("Diagnósticos Bornhuetter-Ferguson")
    display_diagnostics(result)
    with st.expander("Ver prior normalizado y reconciliado", expanded=False):
        st.dataframe(result.prior_input, width="stretch")

    package = build_classical_methods_zip(
        chain_ladder_result,
        chain_ladder_config,
        result,
        source_metadata=source_metadata,
        prior_metadata=prior_metadata,
    )
    st.download_button(
        "Descargar comparación Chain Ladder + BF",
        data=package,
        file_name="demo6_resultados_chain_ladder_bf.zip",
        mime="application/zip",
        type="primary",
    )
    st.info(
        "BF estabiliza los periodos inmaduros mediante una expectativa previa, pero no vuelve "
        "objetivo ni preciso un prior débil. La fuente y los ajustes deben documentarse."
    )


def render_bf_workflow(
    chain_ladder_result,
    chain_ladder_config: ChainLadderConfig,
    chain_ladder_signature: str,
    source_metadata: dict[str, Any],
    *,
    sample_triangle: bool,
) -> None:
    """Render the optional BF stage after a valid Chain Ladder result."""

    st.header("5. Incorpora exposición o expectativa previa")
    st.caption(
        "BF reconoce lo observado y aplica el prior únicamente a la proporción no desarrollada. "
        "El archivo debe contener exactamente un registro por periodo de origen."
    )
    source_options = ["Usar mi archivo local"]
    if sample_triangle:
        source_options.insert(0, "Aprender con el prior sintético incluido")
    prior_source = st.radio(
        "Fuente del prior",
        source_options,
        horizontal=True,
        key="bf_prior_source",
    )
    prior_data, prior_metadata = load_prior_data(
        prior_source == "Aprender con el prior sintético incluido"
    )
    if prior_data is None or prior_metadata is None:
        return

    st.caption(f"{len(prior_data):,} periodos y {len(prior_data.columns)} columnas en el prior.")
    st.dataframe(prior_data.head(100), width="stretch", hide_index=True)
    columns = [str(column) for column in prior_data.columns]
    origin_column = select_prior_column(
        "Periodo de origen del prior",
        columns,
        ("periodo_origen", "mes_origen", "origin_month", "accident_period"),
        key="bf_origin_column",
    )

    mode_labels = [
        PRIOR_MODE_LABELS["exposure_rate"],
        PRIOR_MODE_LABELS["expected_ultimate"],
    ]
    mode_label = st.radio(
        "Definición de la expectativa previa",
        mode_labels,
        horizontal=True,
        key="bf_prior_mode",
    )
    prior_mode = PRIOR_MODE_BY_LABEL[mode_label]
    expected_ultimate_column = "ultimate_esperado"
    exposure_column = "exposicion"
    expected_rate_column = "tasa_esperada"
    if prior_mode == "expected_ultimate":
        expected_ultimate_column = select_prior_column(
            "Ultimate esperado",
            columns,
            ("ultimate_esperado", "expected_ultimate", "perdida_esperada"),
            key="bf_expected_ultimate_column",
        )
    else:
        left, right = st.columns(2)
        with left:
            exposure_column = select_prior_column(
                "Exposición",
                columns,
                ("miembros_mes", "exposicion", "member_months", "prima_devengada"),
                key="bf_exposure_column",
            )
        with right:
            expected_rate_column = select_prior_column(
                "Tasa o costo esperado por unidad",
                columns,
                (
                    "costo_esperado_por_miembro",
                    "tasa_esperada",
                    "expected_cost_per_member",
                    "elr",
                ),
                key="bf_expected_rate_column",
            )

    low_column, high_column = st.columns(2)
    with low_column:
        low_shock = st.number_input(
            "Shock inferior del prior (%)",
            min_value=-99.0,
            max_value=-0.1,
            value=-10.0,
            step=1.0,
            key="bf_low_shock",
        )
    with high_column:
        high_shock = st.number_input(
            "Shock superior del prior (%)",
            min_value=0.1,
            max_value=500.0,
            value=10.0,
            step=1.0,
            key="bf_high_shock",
        )

    try:
        bf_config = BornhuetterFergusonConfig(
            prior_mode=prior_mode,
            origin_column=origin_column,
            expected_ultimate_column=expected_ultimate_column,
            exposure_column=exposure_column,
            expected_rate_column=expected_rate_column,
            sensitivity_shocks=(float(low_shock) / 100.0, 0.0, float(high_shock) / 100.0),
            currency=chain_ladder_config.currency,
            measure=chain_ladder_config.measure,
        )
    except ValueError as exc:
        st.error(str(exc))
        return

    confirmed = st.checkbox(
        "Confirmo que documenté la fuente del prior, su fecha, unidad, independencia y ajustes",
        key="bf_prior_confirmed",
    )
    current_signature = bf_run_signature(chain_ladder_signature, prior_data, bf_config)
    if st.button("Comparar Chain Ladder y Bornhuetter-Ferguson", type="primary"):
        if not confirmed:
            st.error("Confirma la trazabilidad de la expectativa previa antes de ejecutar BF.")
        else:
            try:
                bf_result = fit_bornhuetter_ferguson(
                    chain_ladder_result,
                    prior_data,
                    bf_config,
                )
                st.session_state["demo6_bf_result"] = bf_result
                st.session_state["demo6_bf_signature"] = current_signature
                st.session_state["demo6_bf_prior_metadata"] = prior_metadata
            except Exception as exc:
                st.error(f"La comparación BF se detuvo de forma segura: {exc}")

    if st.session_state.get("demo6_bf_signature") == current_signature:
        stored_result = st.session_state.get("demo6_bf_result")
        stored_prior_metadata = st.session_state.get("demo6_bf_prior_metadata")
        if stored_result is not None and stored_prior_metadata is not None:
            display_bf_result(
                stored_result,
                chain_ladder_result,
                chain_ladder_config,
                source_metadata,
                stored_prior_metadata,
            )
    elif st.session_state.get("demo6_bf_signature"):
        st.warning("El prior, su mapeo o los shocks cambiaron. Ejecuta nuevamente BF.")


configure_page("Demo 6 · Chain Ladder y BF")
inject_corporate_theme()
render_brand_hero(
    "Demo 6",
    "Del triángulo a ultimate e IBNR",
    (
        "Asistente educativo local para estimar factores edad-a-edad, completar el triángulo "
        "acumulado y comparar Chain Ladder con Bornhuetter-Ferguson."
    ),
    tags=("Chain Ladder", "Bornhuetter-Ferguson", "Prior trazable"),
)
st.info(
    "Privacidad: Demo 6 trabaja con triángulos agregados y priors por periodo de origen. Los "
    "archivos seleccionados se procesan en la sesión local y no se envían a GitHub."
)

with st.sidebar:
    render_sidebar_brand()
    st.caption(VISUAL_BUILD)
    st.header("Alcance de Demo 6")
    st.markdown(
        """
        - Triángulos acumulados de Demo 5
        - Factores individuales y candidatos
        - Selección automática o manual
        - Factor de cola explícito
        - Prior directo o exposición × tasa
        - Comparación Chain Ladder vs. BF
        - Sensibilidad y exportación conjunta

        **No cuantifica todavía incertidumbre estocástica.**
        """
    )
    if st.button("Borrar resultados de Demo 6"):
        for state_key in (
            "demo6_result",
            "demo6_sensitivity",
            "demo6_signature",
            "demo6_config",
            "demo6_source_metadata",
            "demo6_bf_result",
            "demo6_bf_signature",
            "demo6_bf_prior_metadata",
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
            for state_key in (
                "demo6_bf_result",
                "demo6_bf_signature",
                "demo6_bf_prior_metadata",
            ):
                st.session_state.pop(state_key, None)
        except Exception as exc:
            st.error(f"La estimación se detuvo de forma segura: {exc}")

if st.session_state.get("demo6_signature") == current_signature:
    stored_result = st.session_state.get("demo6_result")
    stored_sensitivity = st.session_state.get("demo6_sensitivity")
    stored_config = st.session_state.get("demo6_config")
    stored_metadata = st.session_state.get("demo6_source_metadata")
    if stored_result is not None:
        display_result(stored_result, stored_sensitivity, stored_config, stored_metadata)
        render_bf_workflow(
            stored_result,
            stored_config,
            current_signature,
            stored_metadata,
            sample_triangle=source_mode == "Aprender con el ejemplo mensual",
        )
elif st.session_state.get("demo6_signature"):
    st.warning("Los factores o datos cambiaron. Ejecuta nuevamente la estimación.")

render_corporate_footer(
    "Uso educativo. Chain Ladder y BF requieren validación de datos, prior, factores, cola, "
    "reconciliación y gobierno antes de cualquier uso profesional."
)
