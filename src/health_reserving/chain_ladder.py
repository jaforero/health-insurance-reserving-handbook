"""Deterministic Chain Ladder with explicit selections and diagnostics."""

from __future__ import annotations

import hashlib
import io
import json
import math
import re
import zipfile
from dataclasses import asdict, dataclass
from typing import Any, Literal, Mapping

import numpy as np
import pandas as pd


SelectionMethod = Literal[
    "volume_weighted",
    "simple_mean",
    "median",
    "latest_3",
    "manual",
]

SELECTION_LABELS: dict[SelectionMethod, str] = {
    "volume_weighted": "Promedio ponderado por volumen",
    "simple_mean": "Promedio simple de ratios",
    "median": "Mediana de ratios",
    "latest_3": "Promedio de los últimos 3 orígenes",
    "manual": "Selección manual",
}

_DEVELOPMENT_COLUMN = re.compile(r"^dev_(\d+)$")


@dataclass(frozen=True)
class ChainLadderConfig:
    """Traceable assumptions for one deterministic Chain Ladder run."""

    selection_method: SelectionMethod = "volume_weighted"
    tail_factor: float = 1.0
    minimum_observations: int = 3
    manual_factors: Mapping[str, float] | None = None
    currency: str = "COP"
    measure: str = "PAGADO_ACUMULADO"

    def __post_init__(self) -> None:
        if self.selection_method not in SELECTION_LABELS:
            raise ValueError("El método de selección de factores no es válido")
        if not math.isfinite(self.tail_factor) or self.tail_factor <= 0:
            raise ValueError("El factor de cola debe ser finito y mayor que cero")
        if self.minimum_observations < 1:
            raise ValueError("El mínimo de observaciones debe ser al menos uno")
        if self.selection_method == "manual" and not self.manual_factors:
            raise ValueError("La selección manual requiere factores para todos los enlaces")

    def to_dict(self) -> dict[str, Any]:
        values = asdict(self)
        if self.manual_factors is not None:
            values["manual_factors"] = dict(self.manual_factors)
        return values


@dataclass
class ChainLadderResult:
    """Auditable deterministic Chain Ladder outputs."""

    observed_cumulative: pd.DataFrame
    observed_mask: pd.DataFrame
    individual_factors: pd.DataFrame
    factor_summary: pd.DataFrame
    selected_factors: pd.Series
    cdf_to_ultimate: pd.Series
    projected_cumulative: pd.DataFrame
    projected_incremental: pd.DataFrame
    origin_summary: pd.DataFrame
    totals: pd.DataFrame
    diagnostics: pd.DataFrame


@dataclass
class TrianglePackage:
    """The aggregate, non-record-level inputs recovered from a Demo 5 ZIP."""

    cumulative: pd.DataFrame
    observed_mask: pd.DataFrame
    manifest: dict[str, Any]
    triangle_config: dict[str, Any]


def _development_ages(columns: pd.Index) -> list[int]:
    ages: list[int] = []
    for column in columns:
        match = _DEVELOPMENT_COLUMN.fullmatch(str(column))
        if match is None:
            raise ValueError(
                "Las columnas de desarrollo deben llamarse dev_0, dev_1, ... sin columnas extra"
            )
        ages.append(int(match.group(1)))
    if ages != list(range(len(ages))):
        raise ValueError("Las edades de desarrollo deben ser consecutivas y comenzar en dev_0")
    if len(ages) < 2:
        raise ValueError("Chain Ladder requiere al menos dos edades de desarrollo")
    return ages


def _coerce_inputs(
    cumulative: pd.DataFrame,
    observed_mask: pd.DataFrame | None,
) -> tuple[pd.DataFrame, pd.DataFrame, list[int]]:
    if cumulative.empty:
        raise ValueError("El triángulo acumulado está vacío")
    if cumulative.index.has_duplicates:
        raise ValueError("Los periodos de origen no pueden estar duplicados")
    if cumulative.columns.has_duplicates:
        raise ValueError("Las edades de desarrollo no pueden estar duplicadas")

    values = cumulative.copy()
    values.index = pd.Index(
        values.index.astype(str), name=cumulative.index.name or "periodo_origen"
    )
    values.columns = pd.Index(values.columns.astype(str))
    ages = _development_ages(values.columns)
    numeric = values.apply(pd.to_numeric, errors="coerce").astype(float)

    if observed_mask is None:
        mask = numeric.notna()
    else:
        if not cumulative.index.equals(observed_mask.index) or not cumulative.columns.equals(
            observed_mask.columns
        ):
            raise ValueError("La máscara observada debe tener las mismas filas y columnas")
        raw_mask = observed_mask.copy()
        raw_mask.index = numeric.index.copy()
        raw_mask.columns = numeric.columns.copy()
        if raw_mask.isna().any().any():
            raise ValueError("La máscara observada no puede contener valores vacíos")
        allowed = raw_mask.isin([0, 1, False, True])
        if not bool(allowed.all().all()):
            raise ValueError("La máscara observada solo puede contener 0 y 1")
        mask = raw_mask.astype(bool)

    if bool((mask & numeric.isna()).any().any()):
        raise ValueError("Cada celda marcada como observada debe contener un valor numérico")
    observed_values = numeric.where(mask).to_numpy(dtype=float)
    if not np.isfinite(observed_values[~np.isnan(observed_values)]).all():
        raise ValueError("El triángulo contiene valores observados no finitos")
    if bool(((~mask) & numeric.notna()).any().any()):
        raise ValueError("Las celdas futuras deben permanecer vacías en el triángulo de entrada")

    for origin in numeric.index:
        positions = np.flatnonzero(mask.loc[origin].to_numpy(dtype=bool))
        if not len(positions):
            raise ValueError(f"El periodo {origin} no contiene celdas observadas")
        if not np.array_equal(positions, np.arange(positions[-1] + 1)):
            raise ValueError(f"El periodo {origin} contiene vacíos dentro de la historia observada")

    return numeric.where(mask), mask, ages


def _link_label(from_age: int, to_age: int) -> str:
    return f"dev_{from_age}->dev_{to_age}"


def _calculate_factor_tables(
    cumulative: pd.DataFrame,
    mask: pd.DataFrame,
    ages: list[int],
    config: ChainLadderConfig,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    links = [_link_label(age, age + 1) for age in ages[:-1]]
    individual = pd.DataFrame(np.nan, index=cumulative.index.copy(), columns=links)
    summary_rows: list[dict[str, Any]] = []
    selected_values: list[float] = []

    for position, from_age in enumerate(ages[:-1]):
        left = cumulative.iloc[:, position]
        right = cumulative.iloc[:, position + 1]
        observed_pair = mask.iloc[:, position] & mask.iloc[:, position + 1]
        eligible = observed_pair & left.gt(0)
        excluded_nonpositive = int((observed_pair & left.le(0)).sum())
        ratios = (right.loc[eligible] / left.loc[eligible]).astype(float)
        link = links[position]
        individual.loc[eligible, link] = ratios

        if ratios.empty:
            raise ValueError(f"No existen pares válidos para estimar el enlace {link}")
        denominator = float(left.loc[eligible].sum())
        numerator = float(right.loc[eligible].sum())
        candidates = {
            "volume_weighted": numerator / denominator,
            "simple_mean": float(ratios.mean()),
            "median": float(ratios.median()),
            "latest_3": float(ratios.tail(3).mean()),
        }
        if config.selection_method == "manual":
            manual = dict(config.manual_factors or {})
            if link not in manual:
                raise ValueError(f"Falta el factor manual para {link}")
            selected = float(manual[link])
        else:
            selected = float(candidates[config.selection_method])
        if not math.isfinite(selected) or selected <= 0:
            raise ValueError(f"El factor seleccionado para {link} debe ser finito y positivo")

        observations = int(ratios.count())
        ratio_mean = float(ratios.mean())
        ratio_cv = (
            float(ratios.std(ddof=1) / abs(ratio_mean))
            if observations > 1 and not math.isclose(ratio_mean, 0.0)
            else 0.0
        )
        review_reasons: list[str] = []
        if observations < config.minimum_observations:
            review_reasons.append("pocas observaciones")
        if selected < 1.0:
            review_reasons.append("factor menor que 1")
        if ratio_cv > 0.25:
            review_reasons.append("alta dispersión")

        summary_rows.append(
            {
                "enlace": link,
                "desarrollo_desde": from_age,
                "desarrollo_hasta": from_age + 1,
                "observaciones": observations,
                "excluidos_denominador_no_positivo": excluded_nonpositive,
                "factor_ponderado": candidates["volume_weighted"],
                "promedio_simple": candidates["simple_mean"],
                "mediana": candidates["median"],
                "promedio_ultimos_3": candidates["latest_3"],
                "cv_ratios_individuales": ratio_cv,
                "factor_seleccionado": selected,
                "metodo_seleccion": SELECTION_LABELS[config.selection_method],
                "estado": "REVISAR" if review_reasons else "CUMPLE",
                "comentario": ", ".join(review_reasons)
                if review_reasons
                else "Sin alerta automática",
            }
        )
        selected_values.append(selected)

    selected_series = pd.Series(selected_values, index=links, name="factor_seleccionado")
    return individual, pd.DataFrame(summary_rows), selected_series


def _cdf_series(ages: list[int], selected: pd.Series, tail_factor: float) -> pd.Series:
    values = np.ones(len(ages), dtype=float)
    values[-1] = tail_factor
    for position in range(len(ages) - 2, -1, -1):
        link = _link_label(ages[position], ages[position + 1])
        values[position] = float(selected.loc[link]) * values[position + 1]
    return pd.Series(values, index=[f"dev_{age}" for age in ages], name="cdf_a_ultimate")


def _project_triangle(
    cumulative: pd.DataFrame,
    mask: pd.DataFrame,
    ages: list[int],
    selected: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    projected = cumulative.copy()
    for origin in projected.index:
        observed_positions = np.flatnonzero(mask.loc[origin].to_numpy(dtype=bool))
        latest_position = int(observed_positions[-1])
        for position in range(latest_position, len(ages) - 1):
            link = _link_label(ages[position], ages[position + 1])
            projected.iat[projected.index.get_loc(origin), position + 1] = projected.iat[
                projected.index.get_loc(origin), position
            ] * float(selected.loc[link])

    incremental = projected.diff(axis=1)
    incremental.iloc[:, 0] = projected.iloc[:, 0]
    return projected, incremental


def _origin_summary(
    cumulative: pd.DataFrame,
    mask: pd.DataFrame,
    ages: list[int],
    cdf: pd.Series,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for origin in cumulative.index:
        latest_position = int(np.flatnonzero(mask.loc[origin].to_numpy(dtype=bool))[-1])
        latest_age = ages[latest_position]
        observed = float(cumulative.loc[origin, f"dev_{latest_age}"])
        origin_cdf = float(cdf.loc[f"dev_{latest_age}"])
        ultimate = observed * origin_cdf
        ibnr = ultimate - observed
        rows.append(
            {
                "periodo_origen": origin,
                "ultima_edad_observada": latest_age,
                "acumulado_observado": observed,
                "cdf_a_ultimate": origin_cdf,
                "madurez": 1.0 / origin_cdf,
                "ultimate": ultimate,
                "ibnr": ibnr,
            }
        )
    summary = pd.DataFrame(rows).set_index("periodo_origen")
    total_ibnr = float(summary["ibnr"].sum())
    summary["participacion_ibnr"] = (
        summary["ibnr"] / total_ibnr if not math.isclose(total_ibnr, 0.0) else 0.0
    )
    return summary


def _totals(summary: pd.DataFrame, config: ChainLadderConfig) -> pd.DataFrame:
    observed = float(summary["acumulado_observado"].sum())
    ultimate = float(summary["ultimate"].sum())
    ibnr = float(summary["ibnr"].sum())
    return pd.DataFrame(
        [
            {"indicador": "periodos_origen", "valor": len(summary)},
            {"indicador": "acumulado_observado_total", "valor": observed},
            {"indicador": "ultimate_total", "valor": ultimate},
            {"indicador": "ibnr_total", "valor": ibnr},
            {
                "indicador": "ibnr_sobre_ultimate",
                "valor": ibnr / ultimate if not math.isclose(ultimate, 0.0) else np.nan,
            },
            {"indicador": "factor_cola", "valor": config.tail_factor},
        ]
    )


def _diagnostics(
    cumulative: pd.DataFrame,
    mask: pd.DataFrame,
    individual: pd.DataFrame,
    factors: pd.DataFrame,
    summary: pd.DataFrame,
    config: ChainLadderConfig,
) -> pd.DataFrame:
    adjacent_observed = mask.iloc[:, 1:].to_numpy() & mask.iloc[:, :-1].to_numpy()
    differences = cumulative.diff(axis=1).iloc[:, 1:].to_numpy(dtype=float)
    decreasing = int(np.sum(adjacent_observed & (differences < 0)))
    ratios_below_one = int((individual < 1.0).sum().sum())
    reviewed_links = int(factors["estado"].eq("REVISAR").sum())
    zero_latest = int(summary["acumulado_observado"].eq(0).sum())
    total_ibnr = float(summary["ibnr"].sum())
    recent_count = min(12, len(summary))
    recent_ibnr = float(summary.tail(recent_count)["ibnr"].sum())
    concentration = recent_ibnr / total_ibnr if not math.isclose(total_ibnr, 0.0) else np.nan

    rows = [
        {
            "codigo": "CL01_ACUMULADOS_DECRECIENTES",
            "nivel": "ADVERTENCIA" if decreasing else "INFO",
            "valor": decreasing,
            "mensaje": "Celdas observadas donde el acumulado disminuye frente a la edad anterior.",
        },
        {
            "codigo": "CL02_RATIOS_MENORES_1",
            "nivel": "ADVERTENCIA" if ratios_below_one else "INFO",
            "valor": ratios_below_one,
            "mensaje": "Ratios individuales menores que uno; revisar recuperaciones o ajustes.",
        },
        {
            "codigo": "CL03_ENLACES_REVISAR",
            "nivel": "ADVERTENCIA" if reviewed_links else "INFO",
            "valor": reviewed_links,
            "mensaje": "Enlaces con baja suficiencia, alta dispersión o selección menor que uno.",
        },
        {
            "codigo": "CL04_ORIGENES_CERO",
            "nivel": "ADVERTENCIA" if zero_latest else "INFO",
            "valor": zero_latest,
            "mensaje": "Periodos cuyo último acumulado observado es cero.",
        },
        {
            "codigo": "CL05_CONCENTRACION_RECIENTE",
            "nivel": "INFO",
            "valor": concentration,
            "mensaje": f"Proporción del IBNR en los últimos {recent_count} periodos de origen.",
        },
        {
            "codigo": "CL06_FACTOR_COLA",
            "nivel": "ADVERTENCIA" if not math.isclose(config.tail_factor, 1.0) else "INFO",
            "valor": config.tail_factor,
            "mensaje": "Factor aplicado después de la última edad visible del triángulo.",
        },
    ]
    return pd.DataFrame(rows)


def fit_chain_ladder(
    cumulative: pd.DataFrame,
    observed_mask: pd.DataFrame | None = None,
    config: ChainLadderConfig | None = None,
) -> ChainLadderResult:
    """Fit deterministic Chain Ladder to an observed cumulative triangle."""

    selected_config = config or ChainLadderConfig()
    observed, mask, ages = _coerce_inputs(cumulative, observed_mask)
    individual, factor_summary, selected = _calculate_factor_tables(
        observed, mask, ages, selected_config
    )
    cdf = _cdf_series(ages, selected, selected_config.tail_factor)
    projected_cumulative, projected_incremental = _project_triangle(observed, mask, ages, selected)
    summary = _origin_summary(observed, mask, ages, cdf)
    totals = _totals(summary, selected_config)
    diagnostics = _diagnostics(
        observed,
        mask,
        individual,
        factor_summary,
        summary,
        selected_config,
    )
    return ChainLadderResult(
        observed_cumulative=observed,
        observed_mask=mask,
        individual_factors=individual,
        factor_summary=factor_summary,
        selected_factors=selected,
        cdf_to_ultimate=cdf,
        projected_cumulative=projected_cumulative,
        projected_incremental=projected_incremental,
        origin_summary=summary,
        totals=totals,
        diagnostics=diagnostics,
    )


def compare_factor_methods(
    cumulative: pd.DataFrame,
    observed_mask: pd.DataFrame | None = None,
    *,
    tail_factor: float = 1.0,
    minimum_observations: int = 3,
) -> pd.DataFrame:
    """Compare deterministic totals under the four automatic factor selections."""

    rows: list[dict[str, Any]] = []
    for method in ("volume_weighted", "simple_mean", "median", "latest_3"):
        config = ChainLadderConfig(
            selection_method=method,
            tail_factor=tail_factor,
            minimum_observations=minimum_observations,
        )
        result = fit_chain_ladder(cumulative, observed_mask, config)
        summary = result.origin_summary
        rows.append(
            {
                "metodo": method,
                "seleccion": SELECTION_LABELS[method],
                "ultimate_total": float(summary["ultimate"].sum()),
                "ibnr_total": float(summary["ibnr"].sum()),
            }
        )
    sensitivity = pd.DataFrame(rows)
    baseline = float(
        sensitivity.loc[sensitivity["metodo"].eq("volume_weighted"), "ibnr_total"].iloc[0]
    )
    sensitivity["diferencia_ibnr_vs_ponderado"] = sensitivity["ibnr_total"] - baseline
    return sensitivity


def _source_bytes(source: bytes | bytearray | io.BufferedIOBase) -> bytes:
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    if hasattr(source, "getvalue"):
        return bytes(source.getvalue())
    if hasattr(source, "read"):
        position = source.tell() if hasattr(source, "tell") else None
        content = source.read()
        if position is not None and hasattr(source, "seek"):
            source.seek(position)
        return bytes(content)
    raise TypeError("La fuente debe ser contenido binario o un archivo abierto")


def load_demo5_triangle_package(
    source: bytes | bytearray | io.BufferedIOBase,
    *,
    maximum_member_bytes: int = 100 * 1024 * 1024,
) -> TrianglePackage:
    """Load and verify aggregate triangle inputs from a Demo 5 result package."""

    content = _source_bytes(source)
    if not zipfile.is_zipfile(io.BytesIO(content)):
        raise ValueError("El archivo seleccionado no es un ZIP válido")
    required = {
        "02_datos_largos_agregados.csv",
        "04_triangulo_acumulado.csv",
        "05_mascara_observada.csv",
        "08_configuracion.json",
        "09_manifiesto.json",
    }
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        names = set(archive.namelist())
        missing = sorted(required - names)
        if missing:
            raise ValueError("El ZIP de Demo 5 está incompleto: " + ", ".join(missing))
        for name in required:
            if archive.getinfo(name).file_size > maximum_member_bytes:
                raise ValueError(f"El archivo interno {name} excede el límite permitido")

        manifest = json.loads(archive.read("09_manifiesto.json").decode("utf-8"))
        triangle_config = json.loads(archive.read("08_configuracion.json").decode("utf-8"))
        if manifest.get("reconciliado") is not True:
            raise ValueError("El paquete no declara un triángulo reconciliado")
        aggregated = archive.read("02_datos_largos_agregados.csv")
        expected_digest = manifest.get("hash_datos_agregados_sha256")
        actual_digest = hashlib.sha256(aggregated).hexdigest()
        if expected_digest and expected_digest != actual_digest:
            raise ValueError("El hash de los datos agregados no coincide con el manifiesto")

        cumulative = pd.read_csv(
            io.BytesIO(archive.read("04_triangulo_acumulado.csv")), index_col=0
        )
        raw_mask = pd.read_csv(io.BytesIO(archive.read("05_mascara_observada.csv")), index_col=0)
    mask = raw_mask.astype(int).astype(bool)
    cumulative.index.name = cumulative.index.name or "periodo_origen"
    mask.index.name = cumulative.index.name
    return TrianglePackage(
        cumulative=cumulative,
        observed_mask=mask,
        manifest=manifest,
        triangle_config=triangle_config,
    )
