"""Deterministic Bornhuetter-Ferguson with explicit and traceable priors."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd

from .chain_ladder import ChainLadderResult


PriorMode = Literal["expected_ultimate", "exposure_rate"]

PRIOR_MODE_LABELS: dict[PriorMode, str] = {
    "expected_ultimate": "Ultimate esperado directo",
    "exposure_rate": "Exposición por tasa esperada",
}

_CHAIN_LADDER_COLUMNS = (
    "acumulado_observado",
    "cdf_a_ultimate",
    "ultimate",
    "ibnr",
)


@dataclass(frozen=True)
class BornhuetterFergusonConfig:
    """Traceable assumptions for one deterministic BF run."""

    prior_mode: PriorMode = "expected_ultimate"
    origin_column: str = "periodo_origen"
    expected_ultimate_column: str = "ultimate_esperado"
    exposure_column: str = "exposicion"
    expected_rate_column: str = "tasa_esperada"
    sensitivity_shocks: tuple[float, ...] = (-0.10, 0.0, 0.10)
    currency: str = "COP"
    measure: str = "PAGADO_ACUMULADO"

    def __post_init__(self) -> None:
        if self.prior_mode not in PRIOR_MODE_LABELS:
            raise ValueError("El modo de expectativa previa no es válido")
        for attribute in (
            "origin_column",
            "expected_ultimate_column",
            "exposure_column",
            "expected_rate_column",
            "currency",
            "measure",
        ):
            if not str(getattr(self, attribute)).strip():
                raise ValueError(f"La configuración {attribute} no puede estar vacía")

        relevant_columns = (
            (self.origin_column, self.expected_ultimate_column)
            if self.prior_mode == "expected_ultimate"
            else (self.origin_column, self.exposure_column, self.expected_rate_column)
        )
        if len(set(relevant_columns)) != len(relevant_columns):
            raise ValueError("Las columnas requeridas del prior deben tener nombres diferentes")

        try:
            shocks = tuple(float(value) for value in self.sensitivity_shocks)
        except (TypeError, ValueError) as error:
            raise ValueError("Los shocks del prior deben ser numéricos") from error
        if not shocks:
            raise ValueError("La sensibilidad debe incluir al menos un shock del prior")
        if not all(math.isfinite(value) and value > -1.0 for value in shocks):
            raise ValueError("Cada shock del prior debe ser finito y mayor que -100%")
        if len(set(shocks)) != len(shocks):
            raise ValueError("Los shocks del prior no pueden estar duplicados")
        if not any(math.isclose(value, 0.0, abs_tol=1e-12) for value in shocks):
            raise ValueError("La sensibilidad debe incluir el escenario base de 0%")
        object.__setattr__(self, "sensitivity_shocks", shocks)

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable configuration snapshot."""

        values = asdict(self)
        values["sensitivity_shocks"] = list(self.sensitivity_shocks)
        values["prior_mode_label"] = PRIOR_MODE_LABELS[self.prior_mode]
        return values


@dataclass
class BornhuetterFergusonResult:
    """Auditable deterministic Bornhuetter-Ferguson outputs."""

    config: BornhuetterFergusonConfig
    prior_input: pd.DataFrame
    origin_summary: pd.DataFrame
    totals: pd.DataFrame
    sensitivity: pd.DataFrame
    diagnostics: pd.DataFrame


def _normalise_origins(values: pd.Index | pd.Series, *, source: str) -> pd.Index:
    raw = pd.Series(values, dtype="object")
    if raw.isna().any():
        raise ValueError(f"{source} contiene periodos de origen vacíos")
    normalised = raw.astype(str).str.strip()
    if normalised.eq("").any():
        raise ValueError(f"{source} contiene periodos de origen vacíos")
    index = pd.Index(normalised, name="periodo_origen")
    if index.has_duplicates:
        raise ValueError(f"{source} contiene periodos de origen duplicados")
    return index


def _validated_chain_ladder_summary(result: ChainLadderResult) -> pd.DataFrame:
    if not hasattr(result, "origin_summary") or not isinstance(result.origin_summary, pd.DataFrame):
        raise TypeError("Se requiere un resultado válido de Chain Ladder")
    if result.origin_summary.empty:
        raise ValueError("El resultado de Chain Ladder no contiene periodos de origen")

    missing = [column for column in _CHAIN_LADDER_COLUMNS if column not in result.origin_summary]
    if missing:
        raise ValueError(
            "El resultado de Chain Ladder no contiene las columnas requeridas: "
            + ", ".join(missing)
        )

    summary = result.origin_summary.copy(deep=True)
    summary.index = _normalise_origins(summary.index, source="El resultado de Chain Ladder")
    for column in _CHAIN_LADDER_COLUMNS:
        summary[column] = pd.to_numeric(summary[column], errors="coerce")
        values = summary[column].to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError(f"La columna {column} de Chain Ladder contiene valores no finitos")
    if bool(summary["cdf_a_ultimate"].le(0).any()):
        raise ValueError("Los CDF de Chain Ladder deben ser mayores que cero")
    if not np.allclose(
        summary["ultimate"],
        summary["acumulado_observado"] + summary["ibnr"],
        rtol=1e-10,
        atol=1e-8,
    ):
        raise ValueError("Ultimate, observado e IBNR no se reconcilian en Chain Ladder")
    if not np.allclose(
        summary["ultimate"],
        summary["acumulado_observado"] * summary["cdf_a_ultimate"],
        rtol=1e-10,
        atol=1e-8,
    ):
        raise ValueError("Ultimate y CDF no se reconcilian en Chain Ladder")
    return summary


def _numeric_column(frame: pd.DataFrame, column: str, *, label: str) -> pd.Series:
    if column not in frame:
        raise ValueError(f"Falta la columna requerida para {label}: {column}")
    numeric = pd.to_numeric(frame[column], errors="coerce").astype(float)
    if not np.isfinite(numeric.to_numpy(dtype=float)).all():
        raise ValueError(f"La columna {column} contiene valores vacíos, no numéricos o no finitos")
    return numeric


def _prepare_prior(
    prior: pd.DataFrame,
    origins: pd.Index,
    config: BornhuetterFergusonConfig,
) -> pd.DataFrame:
    if not isinstance(prior, pd.DataFrame):
        raise TypeError("La expectativa previa debe entregarse como un DataFrame")
    if prior.empty:
        raise ValueError("La tabla de expectativa previa está vacía")

    frame = prior.copy(deep=True)
    if frame.columns.has_duplicates:
        raise ValueError("La tabla de expectativa previa contiene columnas duplicadas")
    if config.origin_column in frame.columns:
        origin_values = frame.pop(config.origin_column)
    else:
        origin_values = frame.index
    frame.index = _normalise_origins(origin_values, source="La tabla de expectativa previa")

    missing_origins = origins.difference(frame.index).tolist()
    extra_origins = frame.index.difference(origins).tolist()
    if missing_origins or extra_origins:
        details: list[str] = []
        if missing_origins:
            details.append("faltan: " + ", ".join(missing_origins))
        if extra_origins:
            details.append("sobran: " + ", ".join(extra_origins))
        raise ValueError(
            "Los periodos del prior deben coincidir exactamente con Chain Ladder ("
            + "; ".join(details)
            + ")"
        )
    frame = frame.reindex(origins)

    prepared = pd.DataFrame(index=origins.copy())
    prepared["modo_prior"] = PRIOR_MODE_LABELS[config.prior_mode]
    if config.prior_mode == "expected_ultimate":
        expected = _numeric_column(
            frame,
            config.expected_ultimate_column,
            label="el ultimate esperado",
        )
    else:
        exposure = _numeric_column(frame, config.exposure_column, label="la exposición")
        expected_rate = _numeric_column(
            frame,
            config.expected_rate_column,
            label="la tasa esperada",
        )
        if bool(exposure.lt(0).any()):
            raise ValueError("La exposición no puede contener valores negativos")
        if bool(expected_rate.lt(0).any()):
            raise ValueError("La tasa esperada no puede contener valores negativos")
        prepared["exposicion"] = exposure
        prepared["tasa_esperada"] = expected_rate
        with np.errstate(over="ignore", invalid="ignore"):
            expected = exposure * expected_rate

    if not np.isfinite(expected.to_numpy(dtype=float)).all():
        raise ValueError("El cálculo del ultimate esperado produjo valores no finitos")
    if bool(expected.lt(0).any()):
        raise ValueError("El ultimate esperado no puede contener valores negativos")
    prepared["ultimate_esperado_prior"] = expected
    return prepared


def _origin_results(
    chain_ladder: pd.DataFrame,
    prior: pd.DataFrame,
) -> pd.DataFrame:
    summary = pd.DataFrame(index=chain_ladder.index.copy())
    summary["acumulado_observado"] = chain_ladder["acumulado_observado"]
    summary["cdf_a_ultimate"] = chain_ladder["cdf_a_ultimate"]
    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        summary["porcentaje_desarrollado"] = 1.0 / summary["cdf_a_ultimate"]
        summary["porcentaje_no_desarrollado"] = 1.0 - summary["porcentaje_desarrollado"]
    if "exposicion" in prior:
        summary["exposicion"] = prior["exposicion"]
        summary["tasa_esperada"] = prior["tasa_esperada"]
    summary["ultimate_esperado_prior"] = prior["ultimate_esperado_prior"]
    with np.errstate(over="ignore", invalid="ignore"):
        summary["ibnr_bf"] = (
            summary["ultimate_esperado_prior"] * summary["porcentaje_no_desarrollado"]
        )
        summary["ultimate_bf"] = summary["acumulado_observado"] + summary["ibnr_bf"]
    summary["ultimate_chain_ladder"] = chain_ladder["ultimate"]
    summary["ibnr_chain_ladder"] = chain_ladder["ibnr"]
    summary["diferencia_ultimate_bf_vs_cl"] = (
        summary["ultimate_bf"] - summary["ultimate_chain_ladder"]
    )
    summary["diferencia_ibnr_bf_vs_cl"] = summary["ibnr_bf"] - summary["ibnr_chain_ladder"]

    calculated_columns = (
        "porcentaje_desarrollado",
        "porcentaje_no_desarrollado",
        "ibnr_bf",
        "ultimate_bf",
        "diferencia_ultimate_bf_vs_cl",
        "diferencia_ibnr_bf_vs_cl",
    )
    if not np.isfinite(summary.loc[:, calculated_columns].to_numpy(dtype=float)).all():
        raise ValueError("El cálculo Bornhuetter-Ferguson produjo valores no finitos")

    total_ibnr = float(summary["ibnr_bf"].sum())
    summary["participacion_ibnr_bf"] = (
        summary["ibnr_bf"] / total_ibnr if not math.isclose(total_ibnr, 0.0) else 0.0
    )
    return summary


def _totals(summary: pd.DataFrame) -> pd.DataFrame:
    observed = float(summary["acumulado_observado"].sum())
    expected = float(summary["ultimate_esperado_prior"].sum())
    ultimate_bf = float(summary["ultimate_bf"].sum())
    ibnr_bf = float(summary["ibnr_bf"].sum())
    ultimate_cl = float(summary["ultimate_chain_ladder"].sum())
    ibnr_cl = float(summary["ibnr_chain_ladder"].sum())
    if not all(
        math.isfinite(value)
        for value in (observed, expected, ultimate_bf, ibnr_bf, ultimate_cl, ibnr_cl)
    ):
        raise ValueError("Los totales Bornhuetter-Ferguson no son finitos")
    return pd.DataFrame(
        [
            {"indicador": "periodos_origen", "valor": len(summary)},
            {"indicador": "acumulado_observado_total", "valor": observed},
            {"indicador": "ultimate_esperado_prior_total", "valor": expected},
            {"indicador": "ultimate_bf_total", "valor": ultimate_bf},
            {"indicador": "ibnr_bf_total", "valor": ibnr_bf},
            {
                "indicador": "ibnr_bf_sobre_ultimate",
                "valor": ibnr_bf / ultimate_bf if not math.isclose(ultimate_bf, 0.0) else np.nan,
            },
            {"indicador": "ultimate_chain_ladder_total", "valor": ultimate_cl},
            {"indicador": "ibnr_chain_ladder_total", "valor": ibnr_cl},
            {
                "indicador": "diferencia_ultimate_bf_vs_cl_total",
                "valor": ultimate_bf - ultimate_cl,
            },
            {"indicador": "diferencia_ibnr_bf_vs_cl_total", "valor": ibnr_bf - ibnr_cl},
        ]
    )


def _sensitivity(
    summary: pd.DataFrame,
    config: BornhuetterFergusonConfig,
) -> pd.DataFrame:
    observed_total = float(summary["acumulado_observado"].sum())
    expected = summary["ultimate_esperado_prior"]
    unreported = summary["porcentaje_no_desarrollado"]
    base_ibnr = float((expected * unreported).sum())
    rows: list[dict[str, Any]] = []
    for shock in sorted(float(value) for value in config.sensitivity_shocks):
        multiplier = 1.0 + shock
        scenario_ibnr = float((expected * multiplier * unreported).sum())
        scenario_ultimate = observed_total + scenario_ibnr
        scenario_expected = float(expected.sum()) * multiplier
        if not all(
            math.isfinite(value) for value in (scenario_expected, scenario_ibnr, scenario_ultimate)
        ):
            raise ValueError("La sensibilidad del prior produjo valores no finitos")
        label = "Base" if math.isclose(shock, 0.0, abs_tol=1e-12) else f"Prior {shock:+.0%}"
        rows.append(
            {
                "escenario": label,
                "shock_prior": shock,
                "multiplicador_prior": multiplier,
                "ultimate_esperado_prior_total": scenario_expected,
                "ultimate_bf_total": scenario_ultimate,
                "ibnr_bf_total": scenario_ibnr,
                "diferencia_ibnr_vs_base": scenario_ibnr - base_ibnr,
                "diferencia_ultimate_vs_base": scenario_ibnr - base_ibnr,
            }
        )
    return pd.DataFrame(rows)


def _diagnostics(
    summary: pd.DataFrame,
    sensitivity: pd.DataFrame,
) -> pd.DataFrame:
    cdf_below_one = int(summary["cdf_a_ultimate"].lt(1.0).sum())
    prior_below_observed = int(
        summary["ultimate_esperado_prior"].lt(summary["acumulado_observado"]).sum()
    )
    zero_prior = int(summary["ultimate_esperado_prior"].eq(0.0).sum())
    negative_ibnr = int(summary["ibnr_bf"].lt(0.0).sum())
    total_ibnr = float(summary["ibnr_bf"].sum())
    recent_count = min(12, len(summary))
    recent_ibnr = float(summary.tail(recent_count)["ibnr_bf"].sum())
    concentration = recent_ibnr / total_ibnr if not math.isclose(total_ibnr, 0.0) else np.nan
    sensitivity_range = float(
        sensitivity["ibnr_bf_total"].max() - sensitivity["ibnr_bf_total"].min()
    )

    return pd.DataFrame(
        [
            {
                "codigo": "BF01_PRIOR_RECONCILIADO",
                "nivel": "INFO",
                "valor": len(summary),
                "mensaje": "Periodos con prior alineado uno a uno con Chain Ladder.",
            },
            {
                "codigo": "BF02_CDF_MENORES_1",
                "nivel": "ADVERTENCIA" if cdf_below_one else "INFO",
                "valor": cdf_below_one,
                "mensaje": "Periodos con CDF menor que uno y porcentaje no desarrollado negativo.",
            },
            {
                "codigo": "BF03_PRIOR_MENOR_OBSERVADO",
                "nivel": "ADVERTENCIA" if prior_below_observed else "INFO",
                "valor": prior_below_observed,
                "mensaje": "Periodos cuyo ultimate esperado a priori es menor que lo observado.",
            },
            {
                "codigo": "BF04_PRIOR_CERO",
                "nivel": "ADVERTENCIA" if zero_prior else "INFO",
                "valor": zero_prior,
                "mensaje": "Periodos con expectativa previa igual a cero.",
            },
            {
                "codigo": "BF05_IBNR_NEGATIVO",
                "nivel": "ADVERTENCIA" if negative_ibnr else "INFO",
                "valor": negative_ibnr,
                "mensaje": "Periodos con IBNR BF negativo; revisar CDF, recuperaciones y ajustes.",
            },
            {
                "codigo": "BF06_CONCENTRACION_RECIENTE",
                "nivel": "INFO",
                "valor": concentration,
                "mensaje": f"Proporción del IBNR BF en los últimos {recent_count} periodos.",
            },
            {
                "codigo": "BF07_RANGO_SENSIBILIDAD_PRIOR",
                "nivel": "INFO",
                "valor": sensitivity_range,
                "mensaje": "Rango del IBNR total entre los shocks configurados del prior.",
            },
        ]
    )


def fit_bornhuetter_ferguson(
    chain_ladder_result: ChainLadderResult,
    prior: pd.DataFrame,
    config: BornhuetterFergusonConfig | None = None,
) -> BornhuetterFergusonResult:
    """Estimate BF ultimate and IBNR from Chain Ladder maturity and an explicit prior.

    The prior must contain exactly one row per Chain Ladder origin. It can provide either a
    direct expected ultimate or exposure multiplied by an expected rate, according to ``config``.
    Inputs are copied and never mutated.
    """

    selected_config = config or BornhuetterFergusonConfig()
    chain_ladder = _validated_chain_ladder_summary(chain_ladder_result)
    prepared_prior = _prepare_prior(prior, chain_ladder.index, selected_config)
    summary = _origin_results(chain_ladder, prepared_prior)
    totals = _totals(summary)
    sensitivity = _sensitivity(summary, selected_config)
    diagnostics = _diagnostics(summary, sensitivity)
    return BornhuetterFergusonResult(
        config=selected_config,
        prior_input=prepared_prior,
        origin_summary=summary,
        totals=totals,
        sensitivity=sensitivity,
        diagnostics=diagnostics,
    )
