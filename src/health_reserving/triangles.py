"""Triangle construction with explicit observed/future cell semantics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from .config import FREQUENCY_LABELS, TriangleConfig
from .validation import BLOCKING, PreparedClaims


@dataclass
class TriangleResult:
    canonical_detail: pd.DataFrame
    aggregated_long: pd.DataFrame
    incremental: pd.DataFrame
    cumulative: pd.DataFrame
    observed_mask: pd.DataFrame
    diagnostics: pd.DataFrame
    gates: pd.DataFrame
    reconciled: bool


def _period_labels(periods: pd.PeriodIndex, frequency: str) -> list[str]:
    if frequency == "M":
        return [period.strftime("%Y-%m") for period in periods]
    if frequency == "Q":
        return [f"{period.year}-T{period.quarter}" for period in periods]
    return [str(period.year) for period in periods]


def _metric(name: str, value: Any, interpretation: str) -> dict[str, Any]:
    return {"indicador": name, "valor": value, "interpretacion": interpretation}


def build_triangles(prepared: PreparedClaims, config: TriangleConfig) -> TriangleResult:
    """Build incremental/cumulative triangles after all blocking controls pass."""

    if prepared.has_blocking_issues:
        codes = ", ".join(issue.code for issue in prepared.blocking_issues)
        raise ValueError("No se puede construir el triángulo. Controles fallidos: " + codes)
    if prepared.data.empty:
        raise ValueError("No hay datos para construir el triángulo")

    data = prepared.data.copy()
    data["periodo_origen"] = data["fecha_origen"].dt.to_period(config.frequency)
    data["periodo_calendario"] = data["fecha_movimiento"].dt.to_period(config.frequency)
    data["edad_desarrollo"] = (
        data["periodo_calendario"].astype("int64")
        - data["periodo_origen"].astype("int64")
    ).astype(int)

    if data["edad_desarrollo"].lt(0).any():
        raise RuntimeError("Se detectaron rezagos negativos después de la validación")

    observed_maximum = int(data["edad_desarrollo"].max())
    maximum_development = (
        observed_maximum
        if config.maximum_development is None
        else int(config.maximum_development)
    )
    if maximum_development < observed_maximum:
        raise ValueError(
            "La edad máxima seleccionada excluye movimientos observados en edad "
            f"{observed_maximum}. Use un valor igual o superior."
        )

    valuation_period = pd.Timestamp(config.valuation_date).to_period(config.frequency)
    minimum_origin = data["periodo_origen"].min()
    maximum_origin = data["periodo_origen"].max()
    origins = pd.period_range(minimum_origin, maximum_origin, freq=config.frequency)
    development_ages = list(range(maximum_development + 1))
    origin_labels = _period_labels(origins, config.frequency)
    development_labels = [f"dev_{age}" for age in development_ages]

    observed = np.zeros((len(origins), len(development_ages)), dtype=bool)
    incremental_values = np.full(observed.shape, np.nan, dtype=float)
    for row_index, origin in enumerate(origins):
        max_observed = min(maximum_development, valuation_period.ordinal - origin.ordinal)
        if max_observed >= 0:
            observed[row_index, : max_observed + 1] = True
            incremental_values[row_index, : max_observed + 1] = 0.0

    grouped = (
        data.groupby(["periodo_origen", "periodo_calendario", "edad_desarrollo"], observed=True)[
            "importe_incremental"
        ]
        .sum()
        .reset_index()
        .sort_values(["periodo_origen", "edad_desarrollo"])
    )
    origin_positions = {period.ordinal: index for index, period in enumerate(origins)}
    for row in grouped.itertuples(index=False):
        row_index = origin_positions[row.periodo_origen.ordinal]
        column_index = int(row.edad_desarrollo)
        if not observed[row_index, column_index]:
            raise RuntimeError("Un movimiento quedó fuera de la diagonal de valoración")
        incremental_values[row_index, column_index] = float(row.importe_incremental)

    incremental = pd.DataFrame(
        incremental_values,
        index=pd.Index(origin_labels, name="periodo_origen"),
        columns=development_labels,
    )
    cumulative = incremental.cumsum(axis=1, skipna=False)
    observed_mask = pd.DataFrame(
        observed,
        index=incremental.index.copy(),
        columns=incremental.columns.copy(),
    )

    detail_columns = [
        "fila_fuente",
        "fecha_origen",
        "fecha_movimiento",
        "periodo_origen",
        "periodo_calendario",
        "edad_desarrollo",
        "importe_incremental",
    ]
    detail_columns.extend(
        column
        for column in ("id_movimiento", "tipo_movimiento", "segmento")
        if column in data.columns
    )
    canonical_detail = data[detail_columns].copy()
    canonical_detail["periodo_origen"] = canonical_detail["periodo_origen"].astype(str)
    canonical_detail["periodo_calendario"] = canonical_detail["periodo_calendario"].astype(str)

    aggregated_long = grouped.copy()
    aggregated_long["periodo_origen"] = aggregated_long["periodo_origen"].astype(str)
    aggregated_long["periodo_calendario"] = aggregated_long["periodo_calendario"].astype(str)

    source_total = float(data["importe_incremental"].sum())
    triangle_total = float(np.nansum(incremental.to_numpy(dtype=float)))
    difference = triangle_total - source_total
    tolerance = max(0.01, abs(source_total) * 1e-10)
    reconciled = bool(np.isclose(source_total, triangle_total, rtol=1e-10, atol=tolerance))

    origins_with_data = int(data["periodo_origen"].nunique())
    empty_origins = int(len(origins) - origins_with_data)
    minimum_age = min(config.minimum_development_periods, maximum_development)
    origins_at_minimum_age = int(observed_mask.iloc[:, minimum_age].sum())
    metrics = [
        _metric("frecuencia", FREQUENCY_LABELS[config.frequency], "Granularidad seleccionada."),
        _metric("filas_procesadas", len(data), "Registros después del filtro de segmento."),
        _metric("periodos_origen", origins_with_data, "Periodos con movimientos registrados."),
        _metric("periodos_origen_vacios", empty_origins, "Periodos intermedios sin movimientos."),
        _metric("horizonte_desarrollo", maximum_development, "Última edad incluida."),
        _metric(
            "celdas_observadas",
            int(observed.sum()),
            "Celdas hasta la diagonal de valoración.",
        ),
        _metric(
            "celdas_futuras",
            int((~observed).sum()),
            "Celdas todavía no observadas; permanecen vacías.",
        ),
        _metric(
            "ceros_observados",
            int(((incremental == 0) & observed_mask).sum().sum()),
            "Celdas observadas sin importe incremental.",
        ),
        _metric(
            "origenes_observados_edad_minima",
            origins_at_minimum_age,
            f"Orígenes observados al menos hasta edad {minimum_age}.",
        ),
        _metric("total_fuente", source_total, "Suma de importes canónicos."),
        _metric("total_triangulo", triangle_total, "Suma de celdas incrementales observadas."),
        _metric("diferencia_reconciliacion", difference, "Debe ser cero dentro de tolerancia."),
        _metric(
            "estado_reconciliacion",
            "RECONCILIADO" if reconciled else "NO_RECONCILIADO",
            "Control previo a cualquier modelación.",
        ),
    ]
    diagnostics = pd.DataFrame(metrics)
    gates = evaluate_readiness_gates(
        prepared,
        config,
        origins_with_data,
        maximum_development,
        empty_origins,
        reconciled,
    )

    return TriangleResult(
        canonical_detail=canonical_detail,
        aggregated_long=aggregated_long,
        incremental=incremental,
        cumulative=cumulative,
        observed_mask=observed_mask,
        diagnostics=diagnostics,
        gates=gates,
        reconciled=reconciled,
    )


def evaluate_readiness_gates(
    prepared: PreparedClaims,
    config: TriangleConfig,
    origin_periods: int,
    development_horizon: int,
    empty_origins: int,
    reconciled: bool,
) -> pd.DataFrame:
    """Evaluate the subset of Demo 4 gates relevant to triangle construction."""

    issue_codes = {issue.code for issue in prepared.issues if issue.severity == BLOCKING}
    date_codes = {
        "FECHA_ORIGEN_NULA",
        "FECHA_MOVIMIENTO_NULA",
        "REZAGO_NEGATIVO",
        "POSTERIOR_VALORACION",
        "ORIGEN_POSTERIOR_VALORACION",
        "SEM_ORIGEN",
        "SEM_MOVIMIENTO",
        "SEM_CORTE",
    }
    amount_codes = {"IMPORTE_NULO", "IMPORTE_NO_FINITO", "IMPORTES_NEGATIVOS", "SEM_IMPORTE"}
    integrity_codes = {"DUPLICADO_EXACTO", "ID_MOVIMIENTO_DUPLICADO"}
    values = {
        "G0": (
            config.obligation_defined and "SEM_G0" not in issue_codes,
            "Obligación y medida objetivo definidas.",
        ),
        "G1": (not bool(issue_codes & date_codes), "Fechas y corte coherentes."),
        "G2": (
            not bool(issue_codes & amount_codes),
            "Importes interpretables y semántica confirmada.",
        ),
        "G3": (
            not bool(issue_codes & integrity_codes) and reconciled,
            "Integridad y reconciliación del triángulo.",
        ),
        "G4": (
            origin_periods >= config.minimum_origin_periods
            and development_horizon >= config.minimum_development_periods
            and empty_origins == 0,
            "Historia mínima educativa y continuidad de periodos.",
        ),
        "G7": (
            config.representative_history,
            "Representatividad histórica confirmada por el usuario.",
        ),
        "G9": (True, "Configuración y salidas versionables."),
    }
    return pd.DataFrame(
        [
            {
                "gate": gate,
                "resultado": "CUMPLE" if passed else "NO_CUMPLE",
                "descripcion": description,
            }
            for gate, (passed, description) in values.items()
        ]
    )
