"""Deterministic Benktander reserving with explicit iterations and reconciliation."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import pandas as pd

from .bornhuetter_ferguson import BornhuetterFergusonResult
from .chain_ladder import ChainLadderResult


_CL_COLUMNS = (
    "acumulado_observado",
    "cdf_a_ultimate",
    "ultimate",
    "ibnr",
)

_BF_COLUMNS = (
    "acumulado_observado",
    "cdf_a_ultimate",
    "porcentaje_desarrollado",
    "porcentaje_no_desarrollado",
    "ultimate_esperado_prior",
    "ultimate_bf",
    "ibnr_bf",
    "ultimate_chain_ladder",
    "ibnr_chain_ladder",
)


@dataclass(frozen=True)
class BenktanderConfig:
    """Traceable assumptions for a deterministic Benktander run."""

    iterations: int = 2
    sensitivity_iterations: tuple[int, ...] = (0, 1, 2, 3)
    currency: str = "COP"
    measure: str = "PAGADO_ACUMULADO"

    def __post_init__(self) -> None:
        if isinstance(self.iterations, bool) or not isinstance(self.iterations, (int, np.integer)):
            raise ValueError("El número de iteraciones Benktander debe ser un entero")
        iterations = int(self.iterations)
        if not 1 <= iterations <= 50:
            raise ValueError("Las iteraciones Benktander deben estar entre 1 y 50")

        try:
            sensitivity = tuple(self.sensitivity_iterations)
        except TypeError as error:
            raise ValueError("Las iteraciones de sensibilidad deben ser una secuencia") from error
        if not sensitivity:
            raise ValueError("La sensibilidad debe incluir al menos una iteración")
        normalised: list[int] = []
        for value in sensitivity:
            if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
                raise ValueError("Cada iteración de sensibilidad debe ser un entero")
            integer = int(value)
            if not 0 <= integer <= 50:
                raise ValueError("Las iteraciones de sensibilidad deben estar entre 0 y 50")
            normalised.append(integer)
        if len(set(normalised)) != len(normalised):
            raise ValueError("Las iteraciones de sensibilidad no pueden estar duplicadas")
        selected = tuple(sorted(set(normalised + [iterations])))

        if not str(self.currency).strip():
            raise ValueError("La moneda no puede estar vacía")
        if not str(self.measure).strip():
            raise ValueError("La medida no puede estar vacía")
        object.__setattr__(self, "iterations", iterations)
        object.__setattr__(self, "sensitivity_iterations", selected)

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable configuration snapshot."""

        values = asdict(self)
        values["sensitivity_iterations"] = list(self.sensitivity_iterations)
        return values


@dataclass
class BenktanderResult:
    """Auditable deterministic Benktander outputs."""

    config: BenktanderConfig
    origin_summary: pd.DataFrame
    totals: pd.DataFrame
    sensitivity: pd.DataFrame
    diagnostics: pd.DataFrame


def _normalise_index(index: pd.Index, *, source: str) -> pd.Index:
    values = pd.Series(index, dtype="object")
    if values.isna().any():
        raise ValueError(f"{source} contiene periodos de origen vacíos")
    normalised = values.astype(str).str.strip()
    if normalised.eq("").any():
        raise ValueError(f"{source} contiene periodos de origen vacíos")
    result = pd.Index(normalised, name="periodo_origen")
    if result.has_duplicates:
        raise ValueError(f"{source} contiene periodos de origen duplicados")
    return result


def _numeric(frame: pd.DataFrame, columns: tuple[str, ...], *, source: str) -> pd.DataFrame:
    missing = [column for column in columns if column not in frame]
    if missing:
        raise ValueError(f"{source} no contiene las columnas requeridas: {', '.join(missing)}")
    result = frame.loc[:, columns].apply(pd.to_numeric, errors="coerce").astype(float)
    if not np.isfinite(result.to_numpy(dtype=float)).all():
        raise ValueError(f"{source} contiene valores vacíos, no numéricos o no finitos")
    return result


def _validated_inputs(
    chain_ladder_result: ChainLadderResult,
    bf_result: BornhuetterFergusonResult,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not hasattr(chain_ladder_result, "origin_summary") or not isinstance(
        chain_ladder_result.origin_summary, pd.DataFrame
    ):
        raise TypeError("Se requiere un resultado válido de Chain Ladder")
    if not hasattr(bf_result, "origin_summary") or not isinstance(
        bf_result.origin_summary, pd.DataFrame
    ):
        raise TypeError("Se requiere un resultado válido de Bornhuetter-Ferguson")
    if chain_ladder_result.origin_summary.empty or bf_result.origin_summary.empty:
        raise ValueError("Los resultados de entrada no pueden estar vacíos")

    chain_ladder = chain_ladder_result.origin_summary.copy(deep=True)
    bf = bf_result.origin_summary.copy(deep=True)
    chain_ladder.index = _normalise_index(chain_ladder.index, source="Chain Ladder")
    bf.index = _normalise_index(bf.index, source="Bornhuetter-Ferguson")
    if not chain_ladder.index.equals(bf.index):
        raise ValueError("Los periodos de Chain Ladder y BF deben coincidir exactamente y en orden")

    chain_ladder_numeric = _numeric(chain_ladder, _CL_COLUMNS, source="Chain Ladder")
    bf_numeric = _numeric(bf, _BF_COLUMNS, source="Bornhuetter-Ferguson")
    if bool(chain_ladder_numeric["cdf_a_ultimate"].le(0).any()):
        raise ValueError("Los CDF de Chain Ladder deben ser mayores que cero")

    if not np.allclose(
        chain_ladder_numeric["ultimate"],
        chain_ladder_numeric["acumulado_observado"] + chain_ladder_numeric["ibnr"],
        rtol=1e-10,
        atol=1e-8,
    ):
        raise ValueError("Costo proyectado, observado y pasivo no pagado no se reconcilian en Chain Ladder")
    if not np.allclose(
        chain_ladder_numeric["ultimate"],
        chain_ladder_numeric["acumulado_observado"]
        * chain_ladder_numeric["cdf_a_ultimate"],
        rtol=1e-10,
        atol=1e-8,
    ):
        raise ValueError("Costo proyectado y CDF no se reconcilian en Chain Ladder")

    shared_pairs = (
        ("acumulado_observado", "acumulado_observado"),
        ("cdf_a_ultimate", "cdf_a_ultimate"),
        ("ultimate", "ultimate_chain_ladder"),
        ("ibnr", "ibnr_chain_ladder"),
    )
    for cl_column, bf_column in shared_pairs:
        if not np.allclose(
            chain_ladder_numeric[cl_column],
            bf_numeric[bf_column],
            rtol=1e-10,
            atol=1e-8,
        ):
            raise ValueError(f"Chain Ladder y BF no coinciden en {cl_column}")

    developed = 1.0 / chain_ladder_numeric["cdf_a_ultimate"]
    undeveloped = 1.0 - developed
    expected_bf = (
        chain_ladder_numeric["acumulado_observado"]
        + undeveloped * bf_numeric["ultimate_esperado_prior"]
    )
    if not np.allclose(bf_numeric["porcentaje_desarrollado"], developed):
        raise ValueError("La madurez BF no se reconcilia con el CDF")
    if not np.allclose(bf_numeric["porcentaje_no_desarrollado"], undeveloped):
        raise ValueError("La proporción no desarrollada BF no se reconcilia con el CDF")
    if not np.allclose(bf_numeric["ultimate_bf"], expected_bf, rtol=1e-10, atol=1e-8):
        raise ValueError("El costo final BF no se reconcilia con observado, madurez y prior")
    if not np.allclose(
        bf_numeric["ibnr_bf"],
        bf_numeric["ultimate_bf"] - bf_numeric["acumulado_observado"],
        rtol=1e-10,
        atol=1e-8,
    ):
        raise ValueError("Costo final, observado y pasivo no pagado no se reconcilian en BF")
    return chain_ladder_numeric, bf_numeric


def _estimate_for_iterations(
    observed: pd.Series,
    undeveloped: pd.Series,
    prior: pd.Series,
    chain_ladder_ultimate: pd.Series,
    iterations: int,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    iterative = prior.copy(deep=True)
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(iterations):
            iterative = observed + undeveloped * iterative
        prior_weight = undeveloped.pow(iterations)
        closed = (1.0 - prior_weight) * chain_ladder_ultimate + prior_weight * prior
    values = np.column_stack((iterative, closed, prior_weight))
    if not np.isfinite(values).all():
        raise ValueError("El cálculo Benktander produjo valores no finitos")
    return iterative, closed, prior_weight


def _origin_results(
    chain_ladder: pd.DataFrame,
    bf: pd.DataFrame,
    config: BenktanderConfig,
) -> pd.DataFrame:
    summary = pd.DataFrame(index=chain_ladder.index.copy())
    summary["acumulado_observado"] = chain_ladder["acumulado_observado"]
    summary["cdf_a_ultimate"] = chain_ladder["cdf_a_ultimate"]
    summary["porcentaje_desarrollado"] = 1.0 / summary["cdf_a_ultimate"]
    summary["porcentaje_no_desarrollado"] = 1.0 - summary["porcentaje_desarrollado"]
    summary["ultimate_esperado_prior"] = bf["ultimate_esperado_prior"]
    summary["ultimate_chain_ladder"] = chain_ladder["ultimate"]
    summary["ibnr_chain_ladder"] = chain_ladder["ibnr"]
    summary["ultimate_bf"] = bf["ultimate_bf"]
    summary["ibnr_bf"] = bf["ibnr_bf"]

    iterative, closed, prior_weight = _estimate_for_iterations(
        summary["acumulado_observado"],
        summary["porcentaje_no_desarrollado"],
        summary["ultimate_esperado_prior"],
        summary["ultimate_chain_ladder"],
        config.iterations,
    )
    if not np.allclose(iterative, closed, rtol=1e-10, atol=1e-8):
        raise ArithmeticError("Las formas iterativa y cerrada de Benktander no coinciden")

    summary["iteraciones_benktander"] = config.iterations
    summary["peso_prior_inicial"] = prior_weight
    summary["peso_chain_ladder"] = 1.0 - prior_weight
    summary["ultimate_benktander_iterativo"] = iterative
    summary["ultimate_benktander_cerrado"] = closed
    summary["diferencia_formas"] = iterative - closed
    summary["ultimate_benktander"] = closed
    summary["ibnr_benktander"] = closed - summary["acumulado_observado"]
    summary["diferencia_ibnr_bk_vs_cl"] = (
        summary["ibnr_benktander"] - summary["ibnr_chain_ladder"]
    )
    summary["diferencia_ibnr_bk_vs_bf"] = summary["ibnr_benktander"] - summary["ibnr_bf"]
    summary["costo_proyectado_horizonte_seleccionado_benktander"] = summary[
        "ultimate_benktander"
    ]
    summary["pasivo_no_pagado_estimado_benktander"] = summary["ibnr_benktander"]
    summary["costo_proyectado_horizonte_seleccionado_chain_ladder"] = summary[
        "ultimate_chain_ladder"
    ]
    summary["pasivo_no_pagado_estimado_chain_ladder"] = summary["ibnr_chain_ladder"]
    summary["costo_proyectado_horizonte_seleccionado_bf"] = summary["ultimate_bf"]
    summary["pasivo_no_pagado_estimado_bf"] = summary["ibnr_bf"]
    return summary


def _totals(summary: pd.DataFrame) -> pd.DataFrame:
    indicators = {
        "periodos_origen": float(len(summary)),
        "acumulado_observado_total": float(summary["acumulado_observado"].sum()),
        "costo_final_esperado_prior_total": float(summary["ultimate_esperado_prior"].sum()),
        "costo_proyectado_horizonte_seleccionado_chain_ladder_total": float(
            summary["ultimate_chain_ladder"].sum()
        ),
        "pasivo_no_pagado_estimado_chain_ladder_total": float(summary["ibnr_chain_ladder"].sum()),
        "costo_proyectado_horizonte_seleccionado_bf_total": float(summary["ultimate_bf"].sum()),
        "pasivo_no_pagado_estimado_bf_total": float(summary["ibnr_bf"].sum()),
        "costo_proyectado_horizonte_seleccionado_benktander_total": float(
            summary["ultimate_benktander"].sum()
        ),
        "pasivo_no_pagado_estimado_benktander_total": float(summary["ibnr_benktander"].sum()),
        "ultimate_esperado_prior_total": float(summary["ultimate_esperado_prior"].sum()),
        "ultimate_chain_ladder_total": float(summary["ultimate_chain_ladder"].sum()),
        "ibnr_chain_ladder_total": float(summary["ibnr_chain_ladder"].sum()),
        "ultimate_bf_total": float(summary["ultimate_bf"].sum()),
        "ibnr_bf_total": float(summary["ibnr_bf"].sum()),
        "ultimate_benktander_total": float(summary["ultimate_benktander"].sum()),
        "ibnr_benktander_total": float(summary["ibnr_benktander"].sum()),
        "diferencia_ibnr_bk_vs_cl_total": float(summary["diferencia_ibnr_bk_vs_cl"].sum()),
        "diferencia_ibnr_bk_vs_bf_total": float(summary["diferencia_ibnr_bk_vs_bf"].sum()),
    }
    if not all(math.isfinite(value) for value in indicators.values()):
        raise ValueError("Los totales Benktander no son finitos")
    ultimate = indicators["ultimate_benktander_total"]
    indicators["ibnr_benktander_sobre_ultimate"] = (
        indicators["ibnr_benktander_total"] / ultimate
        if not math.isclose(ultimate, 0.0)
        else np.nan
    )
    return pd.DataFrame(
        [{"indicador": indicator, "valor": value} for indicator, value in indicators.items()]
    )


def _sensitivity(summary: pd.DataFrame, config: BenktanderConfig) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for iterations in config.sensitivity_iterations:
        iterative, closed, prior_weight = _estimate_for_iterations(
            summary["acumulado_observado"],
            summary["porcentaje_no_desarrollado"],
            summary["ultimate_esperado_prior"],
            summary["ultimate_chain_ladder"],
            iterations,
        )
        if not np.allclose(iterative, closed, rtol=1e-10, atol=1e-8):
            raise ArithmeticError("La sensibilidad no reconcilia las formas Benktander")
        ultimate = float(closed.sum())
        ibnr = float((closed - summary["acumulado_observado"]).sum())
        rows.append(
            {
                "iteraciones": iterations,
                "escenario": (
                    "Prior inicial" if iterations == 0
                    else "Bornhuetter-Ferguson" if iterations == 1
                    else f"Benktander {iterations} iteraciones"
                ),
                "ultimate_total": ultimate,
                "ibnr_total": ibnr,
                "diferencia_ibnr_vs_cl": ibnr - float(summary["ibnr_chain_ladder"].sum()),
                "diferencia_ibnr_vs_bf": ibnr - float(summary["ibnr_bf"].sum()),
                "peso_prior_promedio": float(prior_weight.mean()),
                "max_diferencia_formas": float((iterative - closed).abs().max()),
            }
        )
    return pd.DataFrame(rows)


def _diagnostics(summary: pd.DataFrame, config: BenktanderConfig) -> pd.DataFrame:
    cdf_below_one = int(summary["cdf_a_ultimate"].lt(1.0).sum())
    weight_outside = int(
        (
            summary["peso_prior_inicial"].lt(0.0)
            | summary["peso_prior_inicial"].gt(1.0)
            | summary["peso_chain_ladder"].lt(0.0)
            | summary["peso_chain_ladder"].gt(1.0)
        ).sum()
    )
    negative_ibnr = int(summary["ibnr_benktander"].lt(0.0).sum())
    max_difference = float(summary["diferencia_formas"].abs().max())
    convergence_gap = float(summary["diferencia_ibnr_bk_vs_cl"].abs().sum())
    return pd.DataFrame(
        [
            {
                "codigo": "BK01_ENTRADAS_RECONCILIADAS",
                "nivel": "INFO",
                "valor": len(summary),
                "mensaje": "Periodos conciliados entre Chain Ladder, BF y Benktander.",
            },
            {
                "codigo": "BK02_CDF_MENORES_1",
                "nivel": "ADVERTENCIA" if cdf_below_one else "INFO",
                "valor": cdf_below_one,
                "mensaje": "Periodos con CDF menor que uno; los pesos dejan de ser convexos.",
            },
            {
                "codigo": "BK03_PESOS_FUERA_RANGO",
                "nivel": "ADVERTENCIA" if weight_outside else "INFO",
                "valor": weight_outside,
                "mensaje": "Periodos con pesos fuera de cero a uno.",
            },
            {
                "codigo": "BK04_PASIVO_NO_PAGADO_NEGATIVO",
                "nivel": "ADVERTENCIA" if negative_ibnr else "INFO",
                "valor": negative_ibnr,
                "mensaje": "Periodos con pasivo no pagado Benktander negativo.",
            },
            {
                "codigo": "BK05_RECONCILIACION_FORMAS",
                "nivel": "INFO" if max_difference <= 1e-8 else "ADVERTENCIA",
                "valor": max_difference,
                "mensaje": "Máxima diferencia entre forma iterativa y forma cerrada.",
            },
            {
                "codigo": "BK06_ITERACIONES_SELECCIONADAS",
                "nivel": "INFO",
                "valor": config.iterations,
                "mensaje": "Número de iteraciones aplicado al resultado seleccionado.",
            },
            {
                "codigo": "BK07_BRECHA_CONVERGENCIA_CL",
                "nivel": "INFO",
                "valor": convergence_gap,
                "mensaje": "Suma absoluta de diferencias del pasivo no pagado frente a Chain Ladder.",
            },
        ]
    )


def fit_benktander(
    chain_ladder_result: ChainLadderResult,
    bornhuetter_ferguson_result: BornhuetterFergusonResult,
    config: BenktanderConfig | None = None,
) -> BenktanderResult:
    """Estimate Benktander final cost and unpaid liability from reconciled CL and BF results.

    Iteration one is Bornhuetter-Ferguson. As iterations increase, and when the unreported
    proportion is between zero and one, the estimate converges to Chain Ladder. Inputs are copied
    and never mutated.
    """

    selected_config = config or BenktanderConfig()
    chain_ladder, bf = _validated_inputs(chain_ladder_result, bornhuetter_ferguson_result)
    summary = _origin_results(chain_ladder, bf, selected_config)
    totals = _totals(summary)
    sensitivity = _sensitivity(summary, selected_config)
    diagnostics = _diagnostics(summary, selected_config)
    return BenktanderResult(
        config=selected_config,
        origin_summary=summary,
        totals=totals,
        sensitivity=sensitivity,
        diagnostics=diagnostics,
    )
