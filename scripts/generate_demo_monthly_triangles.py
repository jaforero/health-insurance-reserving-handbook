#!/usr/bin/env python3
"""Generate a bilingual monthly paid-claims triangle demo using only stdlib.

The default design uses 60 monthly origin periods and development ages 0–24.
It is an educational starting point, not a universal actuarial minimum.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_VALUATION_MONTH = "2025-12"
DEFAULT_ORIGIN_MONTHS = 60
DEFAULT_DEVELOPMENT_MONTHS = 24
DEFAULT_SEED = 20260714
DEMO_FACTOR_THRESHOLD = 24

# Illustrative cumulative paid emergence through development month 24.
BASE_CUMULATIVE_PATTERN = (
    0.2800,
    0.4550,
    0.5850,
    0.6850,
    0.7650,
    0.8270,
    0.8750,
    0.9110,
    0.9380,
    0.9580,
    0.9720,
    0.9815,
    0.9880,
    0.9922,
    0.9950,
    0.9968,
    0.9980,
    0.9988,
    0.99925,
    0.99955,
    0.99972,
    0.99984,
    0.99991,
    0.99996,
    1.0000,
)


@dataclass(frozen=True)
class OriginRecord:
    origin_index: int
    origin_month: str
    member_months: int
    seasonal_index: float
    ultimate_paid: float
    increments: tuple[float, ...]


@dataclass(frozen=True)
class DemoResult:
    valuation_index: int
    origins: tuple[OriginRecord, ...]
    incremental: dict[str, dict[int, float]]
    cumulative: dict[str, dict[int, float]]
    factors: tuple[dict[str, float | int | str], ...]
    estimates: tuple[dict[str, float | int | str], ...]
    observed_cells: int
    complete_origins: int
    total_ibnr: float


LABELS = {
    "es": {
        "data_dir": "demo_triangulos_mensuales",
        "asset_dir": "demo_triangulos_mensuales",
        "long": "reclamaciones_pagadas_mensuales_largo.csv",
        "incremental": "triangulo_pagado_mensual_incremental.csv",
        "cumulative": "triangulo_pagado_mensual_acumulado.csv",
        "factors": "factores_mensuales_edad_a_edad.csv",
        "results": "resultados_chain_ladder_mensual.csv",
        "bf_prior": "prior_bornhuetter_ferguson_mensual.csv",
        "diagnostics": "diagnostico_suficiencia.csv",
        "summary": "resumen_ejecucion.txt",
        "triangle_svg": "triangulo_pagado_mensual_acumulado.svg",
        "curve_svg": "curva_maduracion_mensual.svg",
        "observations_svg": "observaciones_por_factor.svg",
    },
    "en": {
        "data_dir": "demo_monthly_triangles",
        "asset_dir": "demo_monthly_triangles",
        "long": "monthly_paid_claims_long.csv",
        "incremental": "monthly_paid_incremental_triangle.csv",
        "cumulative": "monthly_paid_cumulative_triangle.csv",
        "factors": "monthly_age_to_age_factors.csv",
        "results": "monthly_chain_ladder_results.csv",
        "bf_prior": "monthly_bornhuetter_ferguson_prior.csv",
        "diagnostics": "data_sufficiency_diagnostics.csv",
        "summary": "run_summary.txt",
        "triangle_svg": "monthly_paid_cumulative_triangle.svg",
        "curve_svg": "monthly_maturity_curve.svg",
        "observations_svg": "observations_per_factor.svg",
    },
}


def parse_month(value: str) -> int:
    try:
        year_text, month_text = value.split("-")
        year, month = int(year_text), int(month_text)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError("Use YYYY-MM, for example 2025-12") from exc
    if year < 1900 or not 1 <= month <= 12:
        raise argparse.ArgumentTypeError("Use a valid month in YYYY-MM format")
    return year * 12 + month - 1


def month_label(index: int) -> str:
    year, zero_based_month = divmod(index, 12)
    return f"{year:04d}-{zero_based_month + 1:02d}"


def month_short(index: int) -> str:
    year, zero_based_month = divmod(index, 12)
    return f"{year:04d}-{zero_based_month + 1:02d}"


def validate_parameters(origin_months: int, development_months: int) -> None:
    if development_months != 24:
        raise ValueError(
            "This documented demo currently supports exactly 24 development months. "
            "Change the emergence pattern and documentation before using another horizon."
        )
    if origin_months < development_months + 12:
        raise ValueError(
            "Use at least development_months + 12 origin months so the last link has "
            "a minimally useful number of observations."
        )


def simulate_origins(
    valuation_index: int,
    origin_months: int,
    development_months: int,
    seed: int,
) -> tuple[OriginRecord, ...]:
    rng = random.Random(seed)
    start = valuation_index - origin_months + 1
    base_increments = [BASE_CUMULATIVE_PATTERN[0]]
    base_increments.extend(
        BASE_CUMULATIVE_PATTERN[j] - BASE_CUMULATIVE_PATTERN[j - 1]
        for j in range(1, development_months + 1)
    )
    records: list[OriginRecord] = []

    for position, origin_index in enumerate(range(start, valuation_index + 1)):
        _, zero_based_month = divmod(origin_index, 12)
        angle = 2.0 * math.pi * zero_based_month / 12.0
        seasonal_index = 1.0 + 0.085 * math.cos(angle) + 0.025 * math.sin(angle)
        member_months = round(82_000 * (1.0022**position) * rng.uniform(0.985, 1.015))
        monthly_trend = 1.0060**position
        morbidity = rng.lognormvariate(0.0, 0.025)
        cost_per_member = 215_000 * monthly_trend * seasonal_index * morbidity
        ultimate = member_months * cost_per_member

        noisy_weights: list[float] = []
        for dev, base_weight in enumerate(base_increments):
            # More noise in the sparse tail, while retaining positive increments.
            sigma = 0.035 + 0.0035 * dev
            noisy_weights.append(base_weight * rng.lognormvariate(-0.5 * sigma * sigma, sigma))
        weight_total = sum(noisy_weights)
        increments = tuple(ultimate * weight / weight_total for weight in noisy_weights)
        records.append(
            OriginRecord(
                origin_index=origin_index,
                origin_month=month_label(origin_index),
                member_months=member_months,
                seasonal_index=seasonal_index,
                ultimate_paid=ultimate,
                increments=increments,
            )
        )
    return tuple(records)


def build_triangles(
    origins: Iterable[OriginRecord], valuation_index: int, development_months: int
) -> tuple[dict[str, dict[int, float]], dict[str, dict[int, float]]]:
    incremental: dict[str, dict[int, float]] = {}
    cumulative: dict[str, dict[int, float]] = {}
    for record in origins:
        max_observed = min(development_months, valuation_index - record.origin_index)
        running = 0.0
        incremental[record.origin_month] = {}
        cumulative[record.origin_month] = {}
        for dev in range(max_observed + 1):
            value = record.increments[dev]
            running += value
            incremental[record.origin_month][dev] = value
            cumulative[record.origin_month][dev] = running
    return incremental, cumulative


def calculate_factors(
    cumulative: dict[str, dict[int, float]], development_months: int
) -> tuple[dict[str, float | int | str], ...]:
    rows: list[dict[str, float | int | str]] = []
    for dev in range(development_months):
        pairs = [
            (values[dev], values[dev + 1])
            for values in cumulative.values()
            if dev in values and dev + 1 in values
        ]
        denominator = sum(left for left, _ in pairs)
        numerator = sum(right for _, right in pairs)
        factor = numerator / denominator
        ratios = [right / left for left, right in pairs]
        ratio_cv = statistics.stdev(ratios) / statistics.mean(ratios) if len(ratios) > 1 else 0.0
        count = len(pairs)
        if count >= DEMO_FACTOR_THRESHOLD:
            status = "adecuado_demo"
        elif count >= 12:
            status = "precaucion_demo"
        else:
            status = "insuficiente_demo"
        rows.append(
            {
                "development_from": dev,
                "development_to": dev + 1,
                "factor": factor,
                "observations": count,
                "ratio_cv": ratio_cv,
                "status": status,
            }
        )

    cdf = 1.0
    for row in reversed(rows):
        cdf *= float(row["factor"])
        row["cdf_to_24"] = cdf
    return tuple(rows)


def calculate_estimates(
    origins: Iterable[OriginRecord],
    cumulative: dict[str, dict[int, float]],
    factors: tuple[dict[str, float | int | str], ...],
    development_months: int,
) -> tuple[dict[str, float | int | str], ...]:
    factor_values = {int(row["development_from"]): float(row["factor"]) for row in factors}
    rows: list[dict[str, float | int | str]] = []
    for record in origins:
        observed = cumulative[record.origin_month]
        latest_age = max(observed)
        latest_paid = observed[latest_age]
        cdf = math.prod(factor_values[dev] for dev in range(latest_age, development_months))
        estimated_ultimate = latest_paid * cdf
        ibnr = max(0.0, estimated_ultimate - latest_paid)
        error = estimated_ultimate - record.ultimate_paid
        rows.append(
            {
                "origin_month": record.origin_month,
                "latest_development_month": latest_age,
                "latest_cumulative_paid": latest_paid,
                "cdf_to_24": cdf,
                "estimated_ultimate": estimated_ultimate,
                "estimated_ibnr": ibnr,
                "simulated_true_ultimate": record.ultimate_paid,
                "ultimate_error": error,
                "ultimate_error_pct": error / record.ultimate_paid,
            }
        )
    return tuple(rows)


def build_demo(
    valuation_index: int,
    origin_months: int,
    development_months: int,
    seed: int,
) -> DemoResult:
    validate_parameters(origin_months, development_months)
    origins = simulate_origins(valuation_index, origin_months, development_months, seed)
    incremental, cumulative = build_triangles(origins, valuation_index, development_months)
    factors = calculate_factors(cumulative, development_months)
    estimates = calculate_estimates(origins, cumulative, factors, development_months)
    observed_cells = sum(len(values) for values in cumulative.values())
    complete_origins = sum(development_months in values for values in cumulative.values())
    total_ibnr = sum(float(row["estimated_ibnr"]) for row in estimates)
    result = DemoResult(
        valuation_index=valuation_index,
        origins=origins,
        incremental=incremental,
        cumulative=cumulative,
        factors=factors,
        estimates=estimates,
        observed_cells=observed_cells,
        complete_origins=complete_origins,
        total_ibnr=total_ibnr,
    )
    validate_result(result, origin_months, development_months)
    return result


def validate_result(result: DemoResult, origin_months: int, development_months: int) -> None:
    expected_cells = sum(
        min(development_months, age) + 1 for age in range(origin_months - 1, -1, -1)
    )
    if len(result.origins) != origin_months:
        raise RuntimeError("Origin-month count does not reconcile")
    if result.observed_cells != expected_cells:
        raise RuntimeError("Observed-cell count does not reconcile")
    for record in result.origins:
        values = result.cumulative[record.origin_month]
        running = 0.0
        for dev in sorted(values):
            running += result.incremental[record.origin_month][dev]
            if not math.isclose(running, values[dev], rel_tol=1e-12, abs_tol=0.01):
                raise RuntimeError(f"Incremental/cumulative mismatch for {record.origin_month}")
        if not math.isclose(sum(record.increments), record.ultimate_paid, rel_tol=1e-12):
            raise RuntimeError(f"Simulated ultimate mismatch for {record.origin_month}")
    if min(int(row["observations"]) for row in result.factors) != result.complete_origins:
        raise RuntimeError("The longest-link observation count does not reconcile")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def triangle_rows(
    triangle: dict[str, dict[int, float]], development_months: int, origin_key: str
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for origin, values in triangle.items():
        row: dict[str, object] = {origin_key: origin}
        row.update(
            {
                f"dev_{dev}": round(values[dev], 2) if dev in values else ""
                for dev in range(development_months + 1)
            }
        )
        rows.append(row)
    return rows


def write_language_data(
    result: DemoResult,
    repo_root: Path,
    language: str,
    development_months: int,
    seed: int,
) -> None:
    labels = LABELS[language]
    data_dir = repo_root / "data" / labels["data_dir"]
    data_dir.mkdir(parents=True, exist_ok=True)
    origin_key = "mes_origen" if language == "es" else "origin_month"

    long_rows: list[dict[str, object]] = []
    record_map = {record.origin_month: record for record in result.origins}
    for origin, values in result.incremental.items():
        record = record_map[origin]
        for dev, incremental_value in values.items():
            payment_index = record.origin_index + dev
            if language == "es":
                row = {
                    "mes_origen": origin,
                    "mes_pago": month_label(payment_index),
                    "mes_desarrollo": dev,
                    "miembros_mes": record.member_months,
                    "indice_estacional": round(record.seasonal_index, 6),
                    "pago_incremental": round(incremental_value, 2),
                    "pago_acumulado": round(result.cumulative[origin][dev], 2),
                }
            else:
                row = {
                    "origin_month": origin,
                    "payment_month": month_label(payment_index),
                    "development_month": dev,
                    "member_months": record.member_months,
                    "seasonal_index": round(record.seasonal_index, 6),
                    "incremental_paid": round(incremental_value, 2),
                    "cumulative_paid": round(result.cumulative[origin][dev], 2),
                }
            long_rows.append(row)
    write_csv(data_dir / labels["long"], list(long_rows[0]), long_rows)

    dev_fields = [f"dev_{dev}" for dev in range(development_months + 1)]
    write_csv(
        data_dir / labels["incremental"],
        [origin_key, *dev_fields],
        triangle_rows(result.incremental, development_months, origin_key),
    )
    write_csv(
        data_dir / labels["cumulative"],
        [origin_key, *dev_fields],
        triangle_rows(result.cumulative, development_months, origin_key),
    )

    if language == "es":
        factor_rows = [
            {
                "desarrollo_desde": row["development_from"],
                "desarrollo_hasta": row["development_to"],
                "factor_edad_a_edad": f"{float(row['factor']):.8f}",
                "observaciones": row["observations"],
                "cv_ratios_individuales": f"{float(row['ratio_cv']):.8f}",
                "cdf_hasta_24": f"{float(row['cdf_to_24']):.8f}",
                "estado_heuristica_demo": row["status"],
            }
            for row in result.factors
        ]
        estimate_rows = [
            {
                "mes_origen": row["origin_month"],
                "ultimo_mes_desarrollo": row["latest_development_month"],
                "pagado_acumulado_observado": f"{float(row['latest_cumulative_paid']):.2f}",
                "cdf_hasta_24": f"{float(row['cdf_to_24']):.8f}",
                "ultimate_estimado": f"{float(row['estimated_ultimate']):.2f}",
                "ibnr_estimado": f"{float(row['estimated_ibnr']):.2f}",
                "ultimate_real_simulado": f"{float(row['simulated_true_ultimate']):.2f}",
                "error_ultimate": f"{float(row['ultimate_error']):.2f}",
                "error_ultimate_pct": f"{float(row['ultimate_error_pct']):.8f}",
            }
            for row in result.estimates
        ]
    else:
        factor_rows = [
            {
                "development_from": row["development_from"],
                "development_to": row["development_to"],
                "age_to_age_factor": f"{float(row['factor']):.8f}",
                "observations": row["observations"],
                "individual_ratio_cv": f"{float(row['ratio_cv']):.8f}",
                "cdf_to_24": f"{float(row['cdf_to_24']):.8f}",
                "demo_heuristic_status": str(row["status"])
                .replace("adecuado", "adequate")
                .replace("precaucion", "caution")
                .replace("insuficiente", "insufficient"),
            }
            for row in result.factors
        ]
        estimate_rows = [
            {
                "origin_month": row["origin_month"],
                "latest_development_month": row["latest_development_month"],
                "latest_cumulative_paid": f"{float(row['latest_cumulative_paid']):.2f}",
                "cdf_to_24": f"{float(row['cdf_to_24']):.8f}",
                "estimated_ultimate": f"{float(row['estimated_ultimate']):.2f}",
                "estimated_ibnr": f"{float(row['estimated_ibnr']):.2f}",
                "simulated_true_ultimate": f"{float(row['simulated_true_ultimate']):.2f}",
                "ultimate_error": f"{float(row['ultimate_error']):.2f}",
                "ultimate_error_pct": f"{float(row['ultimate_error_pct']):.8f}",
            }
            for row in result.estimates
        ]
    write_csv(data_dir / labels["factors"], list(factor_rows[0]), factor_rows)
    write_csv(data_dir / labels["results"], list(estimate_rows[0]), estimate_rows)

    prior_rows: list[dict[str, object]] = []
    for position, record in enumerate(result.origins):
        expected_cost = 215_000 * (1.0060**position) * record.seasonal_index
        if language == "es":
            prior_row = {
                "mes_origen": record.origin_month,
                "miembros_mes": record.member_months,
                "costo_esperado_por_miembro": f"{expected_cost:.6f}",
                "ultimate_esperado": f"{record.member_months * expected_cost:.2f}",
            }
        else:
            prior_row = {
                "origin_month": record.origin_month,
                "member_months": record.member_months,
                "expected_cost_per_member": f"{expected_cost:.6f}",
                "expected_ultimate": f"{record.member_months * expected_cost:.2f}",
            }
        prior_rows.append(prior_row)
    write_csv(data_dir / labels["bf_prior"], list(prior_rows[0]), prior_rows)

    minimum_observations = min(int(row["observations"]) for row in result.factors)
    diagnostic_rows = [
        {
            ("indicador" if language == "es" else "metric"): key,
            ("valor" if language == "es" else "value"): value,
            ("lectura" if language == "es" else "interpretation"): interpretation,
        }
        for key, value, interpretation in (
            (
                "meses_origen" if language == "es" else "origin_months",
                len(result.origins),
                "Cinco años; permite observar estacionalidad anual repetida."
                if language == "es"
                else "Five years; supports repeated annual-seasonality review.",
            ),
            (
                "horizonte_desarrollo" if language == "es" else "development_horizon",
                development_months,
                "Punto de partida para reclamaciones de salud de maduración rápida o media."
                if language == "es"
                else "Starting point for fast- or medium-maturing health claims.",
            ),
            (
                "origenes_completos" if language == "es" else "complete_origins",
                result.complete_origins,
                "Meses con observación completa hasta el desarrollo 24."
                if language == "es"
                else "Origin months fully observed through development 24.",
            ),
            (
                "min_observaciones_factor" if language == "es" else "minimum_factor_observations",
                minimum_observations,
                "Supera el umbral didáctico de 24; no es un mínimo actuarial universal."
                if language == "es"
                else "Above the 24-observation teaching threshold; not a universal actuarial minimum.",
            ),
        )
    ]
    write_csv(data_dir / labels["diagnostics"], list(diagnostic_rows[0]), diagnostic_rows)

    valuation = month_label(result.valuation_index)
    if language == "es":
        summary = (
            "=== Demo de triángulos mensuales pagados de salud ===\n"
            f"Mes de valuación: {valuation}\n"
            f"Meses de origen: {len(result.origins)}\n"
            f"Meses de desarrollo: 0-{development_months}\n"
            f"Celdas observadas: {result.observed_cells}\n"
            f"Orígenes completos: {result.complete_origins}\n"
            f"Mínimo de observaciones por factor: {minimum_observations}\n"
            f"IBNR total Chain Ladder: {result.total_ibnr:,.2f}\n"
            f"Semilla: {seed}\n"
            "Nota: 60/24 es una configuración didáctica defendible, no un mínimo universal.\n"
        )
        readme = f"""# Datos del demo de triángulos mensuales\n\nDatos enteramente sintéticos para {len(result.origins)} meses de origen y edades de desarrollo 0–{development_months}.\n\n## Reproducción\n\n```bash\npython scripts/generate_demo_monthly_triangles.py --language es\n```\n\n## Archivos\n\n- `{labels["long"]}`: datos observados en formato largo.\n- `{labels["incremental"]}` y `{labels["cumulative"]}`: triángulos tradicionales.\n- `{labels["factors"]}`: factores mensuales y número de observaciones.\n- `{labels["results"]}`: ultimate, IBNR y comparación con la verdad simulada.\n- `{labels["diagnostics"]}`: controles de suficiencia del diseño.\n\nLos datos no representan experiencia de una entidad ni una metodología prescrita.\n"""
    else:
        summary = (
            "=== Monthly simulated health paid-triangle demo ===\n"
            f"Valuation month: {valuation}\n"
            f"Origin months: {len(result.origins)}\n"
            f"Development months: 0-{development_months}\n"
            f"Observed cells: {result.observed_cells}\n"
            f"Complete origins: {result.complete_origins}\n"
            f"Minimum observations per factor: {minimum_observations}\n"
            f"Total Chain Ladder IBNR: {result.total_ibnr:,.2f}\n"
            f"Seed: {seed}\n"
            "Note: 60/24 is a defensible teaching design, not a universal minimum.\n"
        )
        readme = f"""# Monthly triangle demo data\n\nEntirely synthetic data for {len(result.origins)} origin months and development ages 0–{development_months}.\n\n## Reproduction\n\n```bash\npython scripts/generate_demo_monthly_triangles.py --language en\n```\n\n## Files\n\n- `{labels["long"]}`: observed long-format data.\n- `{labels["incremental"]}` and `{labels["cumulative"]}`: traditional triangles.\n- `{labels["factors"]}`: monthly factors and observation counts.\n- `{labels["results"]}`: ultimate, IBNR and comparison with simulated truth.\n- `{labels["diagnostics"]}`: design-sufficiency controls.\n\nThe data do not represent any entity's experience or a prescribed method.\n"""
    diagnostics_line = (
        f"- `{labels['diagnostics']}`: controles de suficiencia del diseño."
        if language == "es"
        else f"- `{labels['diagnostics']}`: design-sufficiency controls."
    )
    prior_line = (
        f"- `{labels['bf_prior']}`: exposición y costo esperado sintéticos para "
        "Bornhuetter-Ferguson."
        if language == "es"
        else f"- `{labels['bf_prior']}`: synthetic exposure and expected cost for "
        "Bornhuetter-Ferguson."
    )
    readme = readme.replace(diagnostics_line, f"{prior_line}\n{diagnostics_line}")
    (data_dir / labels["summary"]).write_text(summary, encoding="utf-8", newline="\n")
    (data_dir / "README.md").write_text(readme, encoding="utf-8", newline="\n")


def svg_escape(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_svg(path: Path, width: int, height: int, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">
<rect width="{width}" height="{height}" fill="#ffffff"/>
<style>
text {{ font-family: Inter, Arial, sans-serif; fill: #1f2937; }}
.title {{ font-size: 24px; font-weight: 700; }}
.subtitle {{ font-size: 13px; fill: #52606d; }}
.label {{ font-size: 10px; }}
.value {{ font-size: 8px; font-family: Menlo, Consolas, monospace; }}
</style>
{body}
</svg>
"""
    path.write_text(svg, encoding="utf-8", newline="\n")


def write_triangle_svg(
    result: DemoResult, path: Path, language: str, development_months: int
) -> None:
    cell_w, cell_h = 50, 17
    left, top = 100, 105
    width = left + (development_months + 1) * cell_w + 35
    height = top + len(result.origins) * cell_h + 55
    title = (
        "Triángulo mensual pagado acumulado"
        if language == "es"
        else "Monthly cumulative paid triangle"
    )
    subtitle = (
        "COP millones · 60 meses de origen · desarrollo 0–24 · diagonal en amarillo"
        if language == "es"
        else "COP millions · 60 origin months · development 0–24 · diagonal highlighted in gold"
    )
    parts = [
        f'<text x="28" y="38" class="title">{title}</text>',
        f'<text x="28" y="62" class="subtitle">{subtitle}</text>',
        f'<text x="88" y="88" class="label" text-anchor="end">{"Mes origen" if language == "es" else "Origin"}</text>',
    ]
    for dev in range(development_months + 1):
        x = left + dev * cell_w + cell_w / 2
        parts.append(f'<text x="{x}" y="88" class="label" text-anchor="middle">{dev}</text>')
    for row_index, record in enumerate(result.origins):
        y = top + row_index * cell_h
        parts.append(
            f'<text x="88" y="{y + 12}" class="label" text-anchor="end">{record.origin_month}</text>'
        )
        values = result.cumulative[record.origin_month]
        latest = max(values)
        for dev in range(development_months + 1):
            x = left + dev * cell_w
            if dev in values:
                fill = "#f6d365" if dev == latest else "#edf4ff"
                stroke = "#a66f00" if dev == latest else "#cbd8ea"
                text_value = f"{values[dev] / 1_000_000:,.0f}"
            else:
                fill, stroke, text_value = "#fafafa", "#e5e7eb", ""
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="{stroke}" stroke-width="0.7"/>'
            )
            if text_value:
                parts.append(
                    f'<text x="{x + cell_w - 3}" y="{y + 11.5}" class="value" text-anchor="end">{svg_escape(text_value)}</text>'
                )
    write_svg(path, width, height, "\n".join(parts))


def empirical_maturity(result: DemoResult, development_months: int) -> list[float]:
    complete = [values for values in result.cumulative.values() if development_months in values]
    return [
        statistics.mean(values[dev] / values[development_months] for values in complete)
        for dev in range(development_months + 1)
    ]


def write_curve_svg(result: DemoResult, path: Path, language: str, development_months: int) -> None:
    width, height = 920, 500
    left, right, top, bottom = 85, 35, 100, 70
    plot_w, plot_h = width - left - right, height - top - bottom
    values = empirical_maturity(result, development_months)
    points = []
    for dev, value in enumerate(values):
        x = left + dev / development_months * plot_w
        y = top + (1.0 - value) * plot_h
        points.append(f"{x:.1f},{y:.1f}")
    title = (
        "Curva de maduración mensual pagada" if language == "es" else "Monthly paid maturity curve"
    )
    subtitle = (
        f"Promedio empírico de {result.complete_origins} meses completos · porcentaje acumulado del ultimate a 24 meses"
        if language == "es"
        else f"Empirical average of {result.complete_origins} complete months · cumulative share of 24-month ultimate"
    )
    parts = [
        f'<text x="28" y="38" class="title">{title}</text>',
        f'<text x="28" y="62" class="subtitle">{subtitle}</text>',
    ]
    for pct in (0.2, 0.4, 0.6, 0.8, 1.0):
        y = top + (1.0 - pct) * plot_h
        parts.append(f'<line x1="{left}" y1="{y}" x2="{width - right}" y2="{y}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{left - 12}" y="{y + 4}" class="label" text-anchor="end">{pct:.0%}</text>'
        )
    parts.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#374151"/>')
    parts.append(
        f'<line x1="{left}" y1="{top + plot_h}" x2="{width - right}" y2="{top + plot_h}" stroke="#374151"/>'
    )
    for dev in range(0, development_months + 1, 3):
        x = left + dev / development_months * plot_w
        parts.append(
            f'<text x="{x}" y="{top + plot_h + 25}" class="label" text-anchor="middle">{dev}</text>'
        )
    parts.append(
        f'<polyline points="{" ".join(points)}" fill="none" stroke="#3659a7" stroke-width="3"/>'
    )
    for dev in (0, 3, 6, 12, 18, 24):
        x = left + dev / development_months * plot_w
        y = top + (1.0 - values[dev]) * plot_h
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="4" fill="#ffffff" stroke="#3659a7" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{x}" y="{y - 10}" class="label" text-anchor="middle">{values[dev]:.1%}</text>'
        )
    axis = "Mes de desarrollo" if language == "es" else "Development month"
    parts.append(
        f'<text x="{left + plot_w / 2}" y="{height - 18}" class="subtitle" text-anchor="middle">{axis}</text>'
    )
    write_svg(path, width, height, "\n".join(parts))


def write_observations_svg(result: DemoResult, path: Path, language: str) -> None:
    width, height = 920, 500
    left, right, top, bottom = 85, 35, 105, 70
    plot_w, plot_h = width - left - right, height - top - bottom
    counts = [int(row["observations"]) for row in result.factors]
    max_y = max(counts) + 5
    bar_space = plot_w / len(counts)
    title = (
        "Observaciones disponibles por factor mensual"
        if language == "es"
        else "Available observations per monthly factor"
    )
    subtitle = (
        "La muestra cae con el desarrollo · línea punteada = heurística didáctica de 24 observaciones"
        if language == "es"
        else "Sample size declines with development · dashed line = 24-observation teaching heuristic"
    )
    parts = [
        f'<text x="28" y="38" class="title">{title}</text>',
        f'<text x="28" y="62" class="subtitle">{subtitle}</text>',
    ]
    for tick in range(0, max_y + 1, 10):
        y = top + (1.0 - tick / max_y) * plot_h
        parts.append(f'<line x1="{left}" y1="{y}" x2="{width - right}" y2="{y}" stroke="#e5e7eb"/>')
        parts.append(
            f'<text x="{left - 12}" y="{y + 4}" class="label" text-anchor="end">{tick}</text>'
        )
    threshold_y = top + (1.0 - DEMO_FACTOR_THRESHOLD / max_y) * plot_h
    parts.append(
        f'<line x1="{left}" y1="{threshold_y}" x2="{width - right}" y2="{threshold_y}" stroke="#a66f00" stroke-width="2" stroke-dasharray="6 5"/>'
    )
    for dev, count in enumerate(counts):
        bar_h = count / max_y * plot_h
        x = left + dev * bar_space + 3
        y = top + plot_h - bar_h
        fill = "#3659a7" if count >= DEMO_FACTOR_THRESHOLD else "#d97706"
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_space - 6:.1f}" height="{bar_h:.1f}" fill="{fill}" stroke="#27447f"/>'
        )
        if dev % 3 == 0 or dev == len(counts) - 1:
            parts.append(
                f'<text x="{x + (bar_space - 6) / 2:.1f}" y="{top + plot_h + 23}" class="label" text-anchor="middle">{dev}→{dev + 1}</text>'
            )
            parts.append(
                f'<text x="{x + (bar_space - 6) / 2:.1f}" y="{y - 6:.1f}" class="label" text-anchor="middle">{count}</text>'
            )
    axis = "Factor de desarrollo" if language == "es" else "Development factor"
    parts.append(
        f'<text x="{left + plot_w / 2}" y="{height - 18}" class="subtitle" text-anchor="middle">{axis}</text>'
    )
    write_svg(path, width, height, "\n".join(parts))


def write_language_assets(
    result: DemoResult, repo_root: Path, language: str, development_months: int
) -> None:
    labels = LABELS[language]
    asset_dir = repo_root / "docs" / "assets" / labels["asset_dir"]
    write_triangle_svg(result, asset_dir / labels["triangle_svg"], language, development_months)
    write_curve_svg(result, asset_dir / labels["curve_svg"], language, development_months)
    write_observations_svg(result, asset_dir / labels["observations_svg"], language)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=("es", "en", "both"), default="both")
    parser.add_argument("--valuation-month", default=DEFAULT_VALUATION_MONTH)
    parser.add_argument("--origin-months", type=int, default=DEFAULT_ORIGIN_MONTHS)
    parser.add_argument("--development-months", type=int, default=DEFAULT_DEVELOPMENT_MONTHS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root; defaults to the parent of scripts/.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    valuation_index = parse_month(args.valuation_month)
    repo_root = args.repo_root.resolve()
    result = build_demo(
        valuation_index=valuation_index,
        origin_months=args.origin_months,
        development_months=args.development_months,
        seed=args.seed,
    )
    languages = ("es", "en") if args.language == "both" else (args.language,)
    for language in languages:
        write_language_data(result, repo_root, language, args.development_months, args.seed)
        write_language_assets(result, repo_root, language, args.development_months)

    minimum_observations = min(int(row["observations"]) for row in result.factors)
    print("=== Demo mensual bilingüe de triángulos pagados de salud ===")
    print(f"Repo root: {repo_root}")
    print(f"Valuation month / Mes de valuación: {month_label(valuation_index)}")
    print(f"Origin months / Meses de origen: {len(result.origins)}")
    print(f"Development months / Meses de desarrollo: 0-{args.development_months}")
    print(f"Observed cells / Celdas observadas: {result.observed_cells}")
    print(f"Complete origins / Orígenes completos: {result.complete_origins}")
    print(f"Minimum factor observations / Mínimo por factor: {minimum_observations}")
    print(f"Total Chain Ladder IBNR: {result.total_ibnr:,.2f}")
    print("OK: monthly demo files generated / archivos del demo mensual generados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
