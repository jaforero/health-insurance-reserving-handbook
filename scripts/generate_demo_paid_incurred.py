#!/usr/bin/env python3
"""Generate a bilingual paid vs. incurred reserving demo.

This script is intentionally dependency-free. It creates simulated health claims
data, paid and incurred triangles, Chain Ladder comparison tables, and SVG
visualizations suitable for MkDocs.
"""

from __future__ import annotations

import argparse
import csv
import html
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]

ORIGIN_YEARS = list(range(2016, 2026))
DEVELOPMENT_AGES = list(range(10))
VALUATION_YEAR = 2025
DEFAULT_SEED = 20260714

PAID_PATTERN = [0.31, 0.53, 0.68, 0.79, 0.86, 0.915, 0.955, 0.980, 0.994, 1.000]
INCURRED_PATTERN = [0.63, 0.81, 0.895, 0.940, 0.965, 0.982, 0.992, 0.997, 1.000, 1.000]


@dataclass(frozen=True)
class OutputSpec:
    language: str
    data_dir: Path
    asset_dir: Path
    origin_col: str
    dev_col: str
    valuation_col: str
    exposure_col: str
    paid_incremental_col: str
    paid_cumulative_col: str
    incurred_cumulative_col: str
    case_reserve_col: str
    observed_col: str
    long_file: str
    paid_triangle_file: str
    incurred_triangle_file: str
    case_reserve_triangle_file: str
    paid_factors_file: str
    incurred_factors_file: str
    results_file: str
    summary_file: str
    paid_triangle_svg: str
    incurred_triangle_svg: str
    latest_diagonal_svg: str
    readme_file: str = "README.md"


SPECS: tuple[OutputSpec, ...] = (
    OutputSpec(
        language="es",
        data_dir=ROOT / "data/demo_pagado_incurrido",
        asset_dir=ROOT / "docs/assets/demo_pagado_incurrido",
        origin_col="anio_origen",
        dev_col="edad_desarrollo",
        valuation_col="anio_valuacion",
        exposure_col="exposicion_meses_miembro",
        paid_incremental_col="pago_incremental",
        paid_cumulative_col="pago_acumulado",
        incurred_cumulative_col="incurrido_acumulado",
        case_reserve_col="reserva_caso",
        observed_col="observado",
        long_file="reclamaciones_pagadas_incurridas_largo.csv",
        paid_triangle_file="triangulo_pagado_acumulado.csv",
        incurred_triangle_file="triangulo_incurrido_acumulado.csv",
        case_reserve_triangle_file="triangulo_reserva_caso.csv",
        paid_factors_file="factores_pagado.csv",
        incurred_factors_file="factores_incurrido.csv",
        results_file="resultados_comparacion_chain_ladder.csv",
        summary_file="resumen_ejecucion.txt",
        paid_triangle_svg="triangulo_pagado_acumulado.svg",
        incurred_triangle_svg="triangulo_incurrido_acumulado.svg",
        latest_diagonal_svg="comparacion_ultima_diagonal.svg",
    ),
    OutputSpec(
        language="en",
        data_dir=ROOT / "data/demo_paid_incurred",
        asset_dir=ROOT / "docs/assets/demo_paid_incurred",
        origin_col="origin_year",
        dev_col="development_age",
        valuation_col="valuation_year",
        exposure_col="exposure_member_months",
        paid_incremental_col="paid_incremental",
        paid_cumulative_col="paid_cumulative",
        incurred_cumulative_col="incurred_cumulative",
        case_reserve_col="case_reserve",
        observed_col="observed",
        long_file="paid_incurred_claims_long.csv",
        paid_triangle_file="paid_cumulative_triangle.csv",
        incurred_triangle_file="incurred_cumulative_triangle.csv",
        case_reserve_triangle_file="case_reserve_triangle.csv",
        paid_factors_file="paid_age_to_age_factors.csv",
        incurred_factors_file="incurred_age_to_age_factors.csv",
        results_file="chain_ladder_comparison_results.csv",
        summary_file="run_summary.txt",
        paid_triangle_svg="paid_cumulative_triangle.svg",
        incurred_triangle_svg="incurred_cumulative_triangle.svg",
        latest_diagonal_svg="latest_diagonal_comparison.svg",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate simulated paid vs. incurred health reserving demo data."
    )
    parser.add_argument(
        "--language",
        choices=("es", "en", "both"),
        default="both",
        help="Output language. Default: both.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"Random seed. Default: {DEFAULT_SEED}.",
    )
    return parser.parse_args()


def selected_specs(language: str) -> Iterable[OutputSpec]:
    for spec in SPECS:
        if language == "both" or spec.language == language:
            yield spec


def observed_age(origin_year: int) -> int:
    return max(0, min(max(DEVELOPMENT_AGES), VALUATION_YEAR - origin_year))


def simulate(seed: int) -> list[dict[str, float | int | bool]]:
    rng = random.Random(seed)
    records: list[dict[str, float | int | bool]] = []

    for idx, origin_year in enumerate(ORIGIN_YEARS):
        exposure = 410_000 * (1.028**idx) * rng.uniform(0.94, 1.08)
        claim_cost = 118_000 * (1.067**idx)
        morbidity = rng.uniform(0.94, 1.11)
        shock = 1.0 + (0.045 if origin_year in (2020, 2021) else 0.0)
        true_ultimate = exposure * claim_cost * morbidity * shock

        previous_paid = 0.0
        previous_incurred = 0.0
        latest_age = observed_age(origin_year)

        for age in DEVELOPMENT_AGES:
            observed = age <= latest_age

            paid_noise = rng.uniform(0.985, 1.020)
            paid_cumulative = true_ultimate * PAID_PATTERN[age] * paid_noise
            paid_cumulative = min(true_ultimate * 1.005, max(previous_paid, paid_cumulative))
            paid_incremental = paid_cumulative - previous_paid

            # Incurred is paid plus case reserve. It is usually more mature than paid
            # but may carry early development reserve adequacy noise.
            reserve_adequacy = 1.0 + max(0, 5 - age) * 0.010 + rng.uniform(-0.012, 0.014)
            incurred_cumulative = true_ultimate * INCURRED_PATTERN[age] * reserve_adequacy
            incurred_cumulative = max(incurred_cumulative, paid_cumulative)
            incurred_cumulative = min(true_ultimate * 1.025, max(previous_incurred, incurred_cumulative))

            records.append(
                {
                    "origin_year": origin_year,
                    "development_age": age,
                    "valuation_year": origin_year + age,
                    "exposure_member_months": round(exposure, 0),
                    "true_ultimate": true_ultimate,
                    "paid_incremental": paid_incremental if observed else math.nan,
                    "paid_cumulative": paid_cumulative if observed else math.nan,
                    "incurred_cumulative": incurred_cumulative if observed else math.nan,
                    "case_reserve": (incurred_cumulative - paid_cumulative) if observed else math.nan,
                    "observed": observed,
                }
            )

            previous_paid = paid_cumulative
            previous_incurred = incurred_cumulative

    return records


def triangle(records: list[dict[str, float | int | bool]], value_key: str) -> dict[int, list[float | None]]:
    output: dict[int, list[float | None]] = {}
    for origin_year in ORIGIN_YEARS:
        row: list[float | None] = []
        for age in DEVELOPMENT_AGES:
            match = next(
                r for r in records if r["origin_year"] == origin_year and r["development_age"] == age
            )
            value = match[value_key]
            row.append(None if isinstance(value, float) and math.isnan(value) else float(value))
        output[origin_year] = row
    return output


def age_to_age_factors(tri: dict[int, list[float | None]]) -> list[dict[str, float | int | str]]:
    factors: list[dict[str, float | int | str]] = []
    for age in DEVELOPMENT_AGES[:-1]:
        numerator = 0.0
        denominator = 0.0
        count = 0
        for row in tri.values():
            current = row[age]
            nxt = row[age + 1]
            if current is not None and nxt is not None and current > 0:
                numerator += nxt
                denominator += current
                count += 1
        factor = numerator / denominator if denominator else 1.0
        factors.append(
            {
                "from_dev": age,
                "to_dev": age + 1,
                "selected_factor": factor,
                "observations": count,
                "method": "volume_weighted",
            }
        )
    return factors


def tail_factor(factors: list[dict[str, float | int | str]], latest_age: int) -> float:
    product = 1.0
    for item in factors:
        if int(item["from_dev"]) >= latest_age:
            product *= float(item["selected_factor"])
    return product


def latest_value(row: list[float | None]) -> tuple[int, float]:
    for age in range(len(row) - 1, -1, -1):
        if row[age] is not None:
            return age, row[age]
    raise ValueError("row has no observed values")


def comparison_results(
    paid_tri: dict[int, list[float | None]],
    incurred_tri: dict[int, list[float | None]],
    paid_factors: list[dict[str, float | int | str]],
    incurred_factors: list[dict[str, float | int | str]],
) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for origin_year in ORIGIN_YEARS:
        latest_age, paid_latest = latest_value(paid_tri[origin_year])
        incurred_latest = incurred_tri[origin_year][latest_age]
        if incurred_latest is None:
            raise ValueError(f"missing incurred latest for {origin_year}")

        case_reserve = max(0.0, incurred_latest - paid_latest)
        paid_tail = tail_factor(paid_factors, latest_age)
        incurred_tail = tail_factor(incurred_factors, latest_age)
        paid_ultimate = paid_latest * paid_tail
        incurred_ultimate = incurred_latest * incurred_tail
        paid_ibnr = max(0.0, paid_ultimate - paid_latest)
        incurred_ibnr = max(0.0, incurred_ultimate - incurred_latest)

        rows.append(
            {
                "origin_year": origin_year,
                "latest_observed_age": latest_age,
                "observed_paid_cumulative": paid_latest,
                "observed_incurred_cumulative": incurred_latest,
                "observed_case_reserve": case_reserve,
                "paid_tail_factor": paid_tail,
                "paid_chain_ladder_ultimate": paid_ultimate,
                "paid_chain_ladder_ibnr": paid_ibnr,
                "incurred_tail_factor": incurred_tail,
                "incurred_chain_ladder_ultimate": incurred_ultimate,
                "incurred_basis_ibnr": incurred_ibnr,
                "total_unpaid_on_incurred_basis": case_reserve + incurred_ibnr,
                "ultimate_difference_incurred_minus_paid": incurred_ultimate - paid_ultimate,
            }
        )
    return rows


def money(value: float | int | None) -> str:
    if value is None:
        return ""
    return f"{float(value):.2f}"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_triangle_csv(path: Path, spec: OutputSpec, tri: dict[int, list[float | None]]) -> None:
    fieldnames = [spec.origin_col] + [f"dev_{age}" for age in DEVELOPMENT_AGES]
    rows = []
    for origin_year, values in tri.items():
        row = {spec.origin_col: origin_year}
        for age, value in zip(DEVELOPMENT_AGES, values):
            row[f"dev_{age}"] = "" if value is None else money(value)
        rows.append(row)
    write_csv(path, rows, fieldnames)


def translated_long_records(
    records: list[dict[str, float | int | bool]], spec: OutputSpec
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in records:
        if not item["observed"]:
            continue
        rows.append(
            {
                spec.origin_col: item["origin_year"],
                spec.dev_col: item["development_age"],
                spec.valuation_col: item["valuation_year"],
                spec.exposure_col: int(float(item["exposure_member_months"])),
                spec.paid_incremental_col: money(float(item["paid_incremental"])),
                spec.paid_cumulative_col: money(float(item["paid_cumulative"])),
                spec.incurred_cumulative_col: money(float(item["incurred_cumulative"])),
                spec.case_reserve_col: money(float(item["case_reserve"])),
                spec.observed_col: "sí" if spec.language == "es" else "yes",
            }
        )
    return rows


def translated_factors(
    factors: list[dict[str, float | int | str]], language: str
) -> tuple[list[dict[str, object]], list[str]]:
    if language == "es":
        fieldnames = ["desde_dev", "hasta_dev", "factor_seleccionado", "observaciones", "metodo"]
        rows = [
            {
                "desde_dev": row["from_dev"],
                "hasta_dev": row["to_dev"],
                "factor_seleccionado": f"{float(row['selected_factor']):.6f}",
                "observaciones": row["observations"],
                "metodo": "ponderado_por_volumen",
            }
            for row in factors
        ]
    else:
        fieldnames = ["from_dev", "to_dev", "selected_factor", "observations", "method"]
        rows = [
            {
                "from_dev": row["from_dev"],
                "to_dev": row["to_dev"],
                "selected_factor": f"{float(row['selected_factor']):.6f}",
                "observations": row["observations"],
                "method": row["method"],
            }
            for row in factors
        ]
    return rows, fieldnames


def translated_results(
    rows: list[dict[str, float | int]], language: str
) -> tuple[list[dict[str, object]], list[str]]:
    if language == "es":
        mapping = {
            "origin_year": "anio_origen",
            "latest_observed_age": "edad_observada",
            "observed_paid_cumulative": "pagado_acumulado_observado",
            "observed_incurred_cumulative": "incurrido_acumulado_observado",
            "observed_case_reserve": "reserva_caso_observada",
            "paid_tail_factor": "factor_cola_pagado",
            "paid_chain_ladder_ultimate": "ultimate_pagado_chain_ladder",
            "paid_chain_ladder_ibnr": "ibnr_pagado_chain_ladder",
            "incurred_tail_factor": "factor_cola_incurrido",
            "incurred_chain_ladder_ultimate": "ultimate_incurrido_chain_ladder",
            "incurred_basis_ibnr": "ibnr_sobre_base_incurrida",
            "total_unpaid_on_incurred_basis": "no_pagado_total_base_incurrida",
            "ultimate_difference_incurred_minus_paid": "diferencia_ultimate_incurrido_menos_pagado",
        }
    else:
        mapping = {
            "origin_year": "origin_year",
            "latest_observed_age": "latest_observed_age",
            "observed_paid_cumulative": "observed_paid_cumulative",
            "observed_incurred_cumulative": "observed_incurred_cumulative",
            "observed_case_reserve": "observed_case_reserve",
            "paid_tail_factor": "paid_tail_factor",
            "paid_chain_ladder_ultimate": "paid_chain_ladder_ultimate",
            "paid_chain_ladder_ibnr": "paid_chain_ladder_ibnr",
            "incurred_tail_factor": "incurred_tail_factor",
            "incurred_chain_ladder_ultimate": "incurred_chain_ladder_ultimate",
            "incurred_basis_ibnr": "incurred_basis_ibnr",
            "total_unpaid_on_incurred_basis": "total_unpaid_on_incurred_basis",
            "ultimate_difference_incurred_minus_paid": "ultimate_difference_incurred_minus_paid",
        }

    fieldnames = list(mapping.values())
    translated: list[dict[str, object]] = []
    for row in rows:
        translated_row: dict[str, object] = {}
        for source, target in mapping.items():
            value = row[source]
            if "factor" in source:
                translated_row[target] = f"{float(value):.6f}"
            elif source in ("origin_year", "latest_observed_age"):
                translated_row[target] = int(value)
            else:
                translated_row[target] = money(value)
        translated.append(translated_row)
    return translated, fieldnames


def compact_billions(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value / 1_000_000_000:.1f}"


def latest_observed_index(values: list[float | None]) -> int | None:
    for index in range(len(values) - 1, -1, -1):
        if values[index] is not None:
            return index
    return None


def write_triangle_svg(
    path: Path,
    title: str,
    subtitle: str,
    origin_label: str,
    dev_label: str,
    tri: dict[int, list[float | None]],
    language: str,
) -> None:
    cell_width = 84
    cell_height = 42
    left_margin = 118
    top_margin = 132
    right_margin = 48
    bottom_margin = 76
    width = left_margin + len(DEVELOPMENT_AGES) * cell_width + right_margin
    height = top_margin + len(ORIGIN_YEARS) * cell_height + bottom_margin

    observed_fill = "#DBEAFE"
    diagonal_fill = "#BBF7D0"
    future_fill = "#F3F4F6"
    header_fill = "#EEF2FF"
    grid = "#CBD5E1"

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
        "<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.h{font-size:11px;font-weight:700;fill:#111827}.v{font-size:11px;fill:#111827}.m{font-size:11px;fill:#6B7280}.a{font-size:12px;font-weight:600;fill:#374151}</style>",
        '<rect x="0" y="0" width="100%" height="100%" fill="#FFFFFF"/>',
        f'<text x="24" y="34" font-size="20" font-weight="700" fill="#111827">{html.escape(title)}</text>',
        f'<text x="24" y="58" font-size="13" fill="#6B7280">{html.escape(subtitle)}</text>',
        f'<text x="24" y="80" font-size="12" fill="#6B7280">{"Valores en miles de millones" if language == "es" else "Values in billions"}</text>',
        f'<text x="{left_margin + (len(DEVELOPMENT_AGES) * cell_width) // 2}" y="{top_margin - 44}" class="a" text-anchor="middle">{html.escape(dev_label)}</text>',
        f'<text x="22" y="{top_margin + (len(ORIGIN_YEARS) * cell_height) // 2}" class="a" text-anchor="middle" transform="rotate(-90 22 {top_margin + (len(ORIGIN_YEARS) * cell_height) // 2})">{html.escape(origin_label)}</text>',
    ]

    for col_index, age in enumerate(DEVELOPMENT_AGES):
        x = left_margin + col_index * cell_width
        parts.append(f'<rect x="{x}" y="{top_margin - cell_height}" width="{cell_width}" height="{cell_height}" fill="{header_fill}" stroke="{grid}"/>')
        parts.append(f'<text x="{x + cell_width / 2:.0f}" y="{top_margin - 16}" class="h" text-anchor="middle">dev_{age}</text>')

    for row_index, origin_year in enumerate(ORIGIN_YEARS):
        y = top_margin + row_index * cell_height
        values = tri[origin_year]
        latest = latest_observed_index(values)
        parts.append(f'<rect x="{left_margin - 82}" y="{y}" width="82" height="{cell_height}" fill="{header_fill}" stroke="{grid}"/>')
        parts.append(f'<text x="{left_margin - 41}" y="{y + 26}" class="h" text-anchor="middle">{origin_year}</text>')
        for col_index, value in enumerate(values):
            x = left_margin + col_index * cell_width
            if value is None:
                fill, rendered, klass = future_fill, "—", "m"
            elif latest == col_index:
                fill, rendered, klass = diagonal_fill, compact_billions(value), "v"
            else:
                fill, rendered, klass = observed_fill, compact_billions(value), "v"
            parts.append(f'<rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="{fill}" stroke="{grid}"/>')
            parts.append(f'<text x="{x + cell_width / 2:.0f}" y="{y + 26}" class="{klass}" text-anchor="middle">{html.escape(rendered)}</text>')

    legend = [
        (observed_fill, "Observado" if language == "es" else "Observed"),
        (diagonal_fill, "Última diagonal" if language == "es" else "Latest diagonal"),
        (future_fill, "No observado" if language == "es" else "Unobserved"),
    ]
    legend_y = height - 42
    offset = 0
    for color, label in legend:
        parts.append(f'<rect x="{left_margin + offset}" y="{legend_y}" width="16" height="16" fill="{color}" stroke="{grid}"/>')
        parts.append(f'<text x="{left_margin + offset + 22}" y="{legend_y + 13}" font-size="11" fill="#111827">{html.escape(label)}</text>')
        offset += 180

    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts), encoding="utf-8")


def write_latest_diagonal_svg(path: Path, rows: list[dict[str, float | int]], language: str) -> None:
    width = 1040
    height = 560
    margin_left = 84
    margin_right = 40
    margin_top = 92
    margin_bottom = 92
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    max_value = max(float(row["observed_incurred_cumulative"]) for row in rows) * 1.08
    group_width = plot_width / len(rows)
    bar_width = min(22, group_width / 4)

    title = "Comparación última diagonal: pagado vs. incurrido" if language == "es" else "Latest diagonal comparison: paid vs. incurred"
    subtitle = "Valores observados por año de origen; reserva caso = incurrido - pagado" if language == "es" else "Observed values by origin year; case reserve = incurred - paid"
    y_label = "Miles de millones" if language == "es" else "Billions"
    paid_label = "Pagado" if language == "es" else "Paid"
    incurred_label = "Incurrido" if language == "es" else "Incurred"
    reserve_label = "Reserva caso" if language == "es" else "Case reserve"

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
        "<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.axis{font-size:11px;fill:#4B5563}.label{font-size:11px;fill:#111827}.legend{font-size:12px;fill:#111827}</style>",
        '<rect x="0" y="0" width="100%" height="100%" fill="#FFFFFF"/>',
        f'<text x="24" y="34" font-size="20" font-weight="700" fill="#111827">{html.escape(title)}</text>',
        f'<text x="24" y="58" font-size="13" fill="#6B7280">{html.escape(subtitle)}</text>',
    ]

    # Axes and grid.
    for tick in range(0, 6):
        value = max_value * tick / 5
        y = margin_top + plot_height - (value / max_value) * plot_height
        parts.append(f'<line x1="{margin_left}" x2="{width - margin_right}" y1="{y:.1f}" y2="{y:.1f}" stroke="#E5E7EB"/>')
        parts.append(f'<text x="{margin_left - 10}" y="{y + 4:.1f}" class="axis" text-anchor="end">{value / 1_000_000_000:.0f}</text>')

    parts.append(f'<line x1="{margin_left}" x2="{margin_left}" y1="{margin_top}" y2="{margin_top + plot_height}" stroke="#9CA3AF"/>')
    parts.append(f'<line x1="{margin_left}" x2="{width - margin_right}" y1="{margin_top + plot_height}" y2="{margin_top + plot_height}" stroke="#9CA3AF"/>')
    parts.append(f'<text x="24" y="{margin_top + 10}" class="axis">{html.escape(y_label)}</text>')

    paid_color = "#2563EB"
    incurred_color = "#059669"
    reserve_color = "#F59E0B"

    for index, row in enumerate(rows):
        group_center = margin_left + index * group_width + group_width / 2
        origin = int(row["origin_year"])
        paid = float(row["observed_paid_cumulative"])
        incurred = float(row["observed_incurred_cumulative"])
        reserve = float(row["observed_case_reserve"])
        values = [(paid, paid_color, -bar_width * 1.25), (incurred, incurred_color, 0), (reserve, reserve_color, bar_width * 1.25)]
        for value, color, offset in values:
            bar_height = (value / max_value) * plot_height
            x = group_center + offset - bar_width / 2
            y = margin_top + plot_height - bar_height
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width}" height="{bar_height:.1f}" fill="{color}" rx="2"/>')
        parts.append(f'<text x="{group_center:.1f}" y="{margin_top + plot_height + 22}" class="axis" text-anchor="middle">{origin}</text>')

    legend_y = height - 42
    legend_x = margin_left
    for label, color in [(paid_label, paid_color), (incurred_label, incurred_color), (reserve_label, reserve_color)]:
        parts.append(f'<rect x="{legend_x}" y="{legend_y}" width="16" height="16" fill="{color}" rx="2"/>')
        parts.append(f'<text x="{legend_x + 22}" y="{legend_y + 13}" class="legend">{html.escape(label)}</text>')
        legend_x += 150

    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts), encoding="utf-8")


def write_readme(spec: OutputSpec) -> None:
    if spec.language == "es":
        text = """# Demo pagado vs. incurrido

Datos sintéticos para comparar triángulos pagados e incurridos en reserving de salud.

Archivos principales:

- `reclamaciones_pagadas_incurridas_largo.csv`: datos observados en formato largo.
- `triangulo_pagado_acumulado.csv`: triángulo acumulado pagado.
- `triangulo_incurrido_acumulado.csv`: triángulo acumulado incurrido.
- `triangulo_reserva_caso.csv`: reserva caso observada, calculada como incurrido menos pagado.
- `factores_pagado.csv`: factores edad-a-edad sobre base pagada.
- `factores_incurrido.csv`: factores edad-a-edad sobre base incurrida.
- `resultados_comparacion_chain_ladder.csv`: comparación de ultimate e IBNR.

Los datos son simulados y no representan experiencia real de ninguna entidad.
"""
    else:
        text = """# Paid vs. incurred demo

Synthetic data to compare paid and incurred triangles in health reserving.

Main files:

- `paid_incurred_claims_long.csv`: observed long-format data.
- `paid_cumulative_triangle.csv`: cumulative paid triangle.
- `incurred_cumulative_triangle.csv`: cumulative incurred triangle.
- `case_reserve_triangle.csv`: observed case reserve, calculated as incurred minus paid.
- `paid_age_to_age_factors.csv`: age-to-age factors on paid basis.
- `incurred_age_to_age_factors.csv`: age-to-age factors on incurred basis.
- `chain_ladder_comparison_results.csv`: ultimate and IBNR comparison.

The data are simulated and do not represent real experience from any entity.
"""
    (spec.data_dir / spec.readme_file).write_text(text, encoding="utf-8")


def write_summary(
    spec: OutputSpec,
    records: list[dict[str, float | int | bool]],
    results: list[dict[str, float | int]],
) -> None:
    total_paid_ibnr = sum(float(row["paid_chain_ladder_ibnr"]) for row in results)
    total_case_reserve = sum(float(row["observed_case_reserve"]) for row in results)
    total_incurred_ibnr = sum(float(row["incurred_basis_ibnr"]) for row in results)
    total_unpaid = sum(float(row["total_unpaid_on_incurred_basis"]) for row in results)
    observed_count = sum(1 for row in records if row["observed"])

    if spec.language == "es":
        text = f"""=== Demo pagado vs. incurrido en salud ===
Directorio de salida: {spec.data_dir.relative_to(ROOT)}
Celdas observadas: {observed_count}
Años de origen: {ORIGIN_YEARS[0]}-{ORIGIN_YEARS[-1]}
Año de valuación: {VALUATION_YEAR}
IBNR total Chain Ladder base pagada: {total_paid_ibnr:,.2f}
Reserva caso observada total: {total_case_reserve:,.2f}
IBNR total sobre base incurrida: {total_incurred_ibnr:,.2f}
No pagado total sobre base incurrida: {total_unpaid:,.2f}
"""
    else:
        text = f"""=== Paid vs. incurred health demo ===
Output directory: {spec.data_dir.relative_to(ROOT)}
Observed cells: {observed_count}
Origin years: {ORIGIN_YEARS[0]}-{ORIGIN_YEARS[-1]}
Valuation year: {VALUATION_YEAR}
Total paid-basis Chain Ladder IBNR: {total_paid_ibnr:,.2f}
Total observed case reserve: {total_case_reserve:,.2f}
Total incurred-basis IBNR: {total_incurred_ibnr:,.2f}
Total unpaid on incurred basis: {total_unpaid:,.2f}
"""
    (spec.data_dir / spec.summary_file).write_text(text, encoding="utf-8")


def generate_for_spec(
    spec: OutputSpec,
    records: list[dict[str, float | int | bool]],
    paid_tri: dict[int, list[float | None]],
    incurred_tri: dict[int, list[float | None]],
    case_reserve_tri: dict[int, list[float | None]],
    paid_factors: list[dict[str, float | int | str]],
    incurred_factors: list[dict[str, float | int | str]],
    results: list[dict[str, float | int]],
) -> None:
    spec.data_dir.mkdir(parents=True, exist_ok=True)
    spec.asset_dir.mkdir(parents=True, exist_ok=True)

    long_rows = translated_long_records(records, spec)
    write_csv(
        spec.data_dir / spec.long_file,
        long_rows,
        [
            spec.origin_col,
            spec.dev_col,
            spec.valuation_col,
            spec.exposure_col,
            spec.paid_incremental_col,
            spec.paid_cumulative_col,
            spec.incurred_cumulative_col,
            spec.case_reserve_col,
            spec.observed_col,
        ],
    )

    write_triangle_csv(spec.data_dir / spec.paid_triangle_file, spec, paid_tri)
    write_triangle_csv(spec.data_dir / spec.incurred_triangle_file, spec, incurred_tri)
    write_triangle_csv(spec.data_dir / spec.case_reserve_triangle_file, spec, case_reserve_tri)

    paid_factor_rows, factor_fieldnames = translated_factors(paid_factors, spec.language)
    incurred_factor_rows, _ = translated_factors(incurred_factors, spec.language)
    write_csv(spec.data_dir / spec.paid_factors_file, paid_factor_rows, factor_fieldnames)
    write_csv(spec.data_dir / spec.incurred_factors_file, incurred_factor_rows, factor_fieldnames)

    translated_result_rows, result_fieldnames = translated_results(results, spec.language)
    write_csv(spec.data_dir / spec.results_file, translated_result_rows, result_fieldnames)

    if spec.language == "es":
        write_triangle_svg(
            spec.asset_dir / spec.paid_triangle_svg,
            "Triángulo pagado acumulado",
            "Base pagada: más lenta, más IBNR explícito en años inmaduros",
            "Año origen",
            "Edad de desarrollo",
            paid_tri,
            spec.language,
        )
        write_triangle_svg(
            spec.asset_dir / spec.incurred_triangle_svg,
            "Triángulo incurrido acumulado",
            "Base incurrida: incorpora reserva caso y suele madurar antes que el pago",
            "Año origen",
            "Edad de desarrollo",
            incurred_tri,
            spec.language,
        )
    else:
        write_triangle_svg(
            spec.asset_dir / spec.paid_triangle_svg,
            "Paid cumulative triangle",
            "Paid basis: slower emergence and more explicit IBNR in immature years",
            "Origin year",
            "Development age",
            paid_tri,
            spec.language,
        )
        write_triangle_svg(
            spec.asset_dir / spec.incurred_triangle_svg,
            "Incurred cumulative triangle",
            "Incurred basis: includes case reserves and usually matures faster than paid",
            "Origin year",
            "Development age",
            incurred_tri,
            spec.language,
        )

    write_latest_diagonal_svg(spec.asset_dir / spec.latest_diagonal_svg, results, spec.language)
    write_readme(spec)
    write_summary(spec, records, results)


def main() -> None:
    args = parse_args()
    records = simulate(args.seed)
    paid_tri = triangle(records, "paid_cumulative")
    incurred_tri = triangle(records, "incurred_cumulative")
    case_reserve_tri = triangle(records, "case_reserve")
    paid_factors = age_to_age_factors(paid_tri)
    incurred_factors = age_to_age_factors(incurred_tri)
    results = comparison_results(paid_tri, incurred_tri, paid_factors, incurred_factors)

    print("=== Demo pagado vs. incurrido / Paid vs. incurred demo ===")
    for spec in selected_specs(args.language):
        generate_for_spec(
            spec,
            records,
            paid_tri,
            incurred_tri,
            case_reserve_tri,
            paid_factors,
            incurred_factors,
            results,
        )
        print(f"Output directory: {spec.data_dir.relative_to(ROOT)}")
        print(f"Assets directory: {spec.asset_dir.relative_to(ROOT)}")

    observed_count = sum(1 for row in records if row["observed"])
    total_paid_ibnr = sum(float(row["paid_chain_ladder_ibnr"]) for row in results)
    total_case_reserve = sum(float(row["observed_case_reserve"]) for row in results)
    total_incurred_ibnr = sum(float(row["incurred_basis_ibnr"]) for row in results)
    print(f"Celdas observadas / Observed cells: {observed_count}")
    print(f"Años de origen / Origin years: {ORIGIN_YEARS[0]}-{ORIGIN_YEARS[-1]}")
    print(f"Año de valuación / Valuation year: {VALUATION_YEAR}")
    print(f"IBNR base pagada / Paid-basis IBNR: {total_paid_ibnr:,.2f}")
    print(f"Reserva caso / Case reserve: {total_case_reserve:,.2f}")
    print(f"IBNR base incurrida / Incurred-basis IBNR: {total_incurred_ibnr:,.2f}")
    print("OK: archivos del demo generados / demo files generated.")


if __name__ == "__main__":
    main()
