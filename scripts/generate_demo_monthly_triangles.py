#!/usr/bin/env python3
"""Generate the bilingual monthly paid-triangle demo using only stdlib.

The r2 default uses a 72 x 36 estimation basis (72 origin months and
development ages 0--35), publishes a traditional 36 x 36 view, and simulates
runoff through age 48 so the tail assumption can be tested explicitly.
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
DEFAULT_ORIGIN_MONTHS = 72
DEFAULT_DEVELOPMENT_MONTHS = 35
DEFAULT_RUNOFF_MONTHS = 48
DEFAULT_SEED = 20260714
TRADITIONAL_VIEW_SIZE = 36
DEMO_FACTOR_THRESHOLD = 24


def cumulative_paid_pattern(age: int, runoff_months: int = DEFAULT_RUNOFF_MONTHS) -> float:
    """Synthetic cumulative paid share, normalized to one at the runoff age."""

    def raw(month: int) -> float:
        return (
            0.72 * (1.0 - math.exp(-0.40 * (month + 1)))
            + 0.23 * (1.0 - math.exp(-0.14 * (month + 1)))
            + 0.05 * (1.0 - math.exp(-0.05 * (month + 1)))
        )

    return raw(age) / raw(runoff_months)


@dataclass(frozen=True)
class OriginRecord:
    origin_index: int
    origin_month: str
    member_months: int
    seasonal_index: float
    simulated_final_cost: float
    increments: tuple[float, ...]

    @property
    def ultimate_paid(self) -> float:
        """Compatibility alias retained for tests/notebooks before r2."""

        return self.simulated_final_cost


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
    terminal_age: int
    runoff_age: int
    synthetic_tail_factor: float
    total_unpaid_claim_liability: float

    @property
    def total_ibnr(self) -> float:
        """Deprecated compatibility alias; this is not pure IBNR."""

        return self.total_unpaid_claim_liability


LABELS = {
    "es": {
        "data_dir": "demo_triangulos_mensuales",
        "asset_dir": "demo_triangulos_mensuales",
        "long": "reclamaciones_pagadas_mensuales_largo.csv",
        "incremental": "triangulo_pagado_mensual_incremental.csv",
        "cumulative": "triangulo_pagado_mensual_acumulado.csv",
        "square": "vista_tradicional_36x36.csv",
        "factors": "factores_mensuales_edad_a_edad.csv",
        "results": "resultados_proyeccion_pasivo_no_pagado.csv",
        "diagnostics": "diagnostico_suficiencia.csv",
        "prior": "prior_bornhuetter_ferguson_mensual.csv",
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
        "square": "traditional_36x36_view.csv",
        "factors": "monthly_age_to_age_factors.csv",
        "results": "unpaid_claim_liability_projection_results.csv",
        "diagnostics": "data_sufficiency_diagnostics.csv",
        "prior": "monthly_bornhuetter_ferguson_prior.csv",
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


def validate_parameters(origin_months: int, development_months: int, runoff_months: int) -> None:
    if development_months != DEFAULT_DEVELOPMENT_MONTHS:
        raise ValueError(
            "This documented r2 demo supports exactly ages 0-35. Change the pattern, "
            "tail validation, tests and documentation before using another horizon."
        )
    if runoff_months <= development_months:
        raise ValueError("The simulated runoff age must be later than the visible terminal age")
    if origin_months < development_months + 24:
        raise ValueError(
            "Use at least development_months + 24 origins so the longest visible link "
            "has a meaningful teaching sample."
        )


def simulate_origins(
    valuation_index: int,
    origin_months: int,
    runoff_months: int,
    seed: int,
) -> tuple[OriginRecord, ...]:
    rng = random.Random(seed)
    start = valuation_index - origin_months + 1
    cumulative_pattern = [cumulative_paid_pattern(age, runoff_months) for age in range(runoff_months + 1)]
    base_increments = [cumulative_pattern[0]]
    base_increments.extend(
        cumulative_pattern[age] - cumulative_pattern[age - 1]
        for age in range(1, runoff_months + 1)
    )
    records: list[OriginRecord] = []

    for position, origin_index in enumerate(range(start, valuation_index + 1)):
        _, zero_based_month = divmod(origin_index, 12)
        angle = 2.0 * math.pi * zero_based_month / 12.0
        seasonal_index = 1.0 + 0.085 * math.cos(angle) + 0.025 * math.sin(angle)
        member_months = round(82_000 * (1.0022 ** position) * rng.uniform(0.985, 1.015))
        monthly_trend = 1.0060 ** position
        morbidity = rng.lognormvariate(0.0, 0.025)
        cost_per_member = 215_000 * monthly_trend * seasonal_index * morbidity
        final_cost = member_months * cost_per_member

        noisy_weights: list[float] = []
        for age, base_weight in enumerate(base_increments):
            sigma = 0.030 + 0.0020 * age
            noisy_weights.append(base_weight * rng.lognormvariate(-0.5 * sigma * sigma, sigma))
        total_weight = sum(noisy_weights)
        increments = tuple(final_cost * weight / total_weight for weight in noisy_weights)
        records.append(
            OriginRecord(
                origin_index=origin_index,
                origin_month=month_label(origin_index),
                member_months=member_months,
                seasonal_index=seasonal_index,
                simulated_final_cost=final_cost,
                increments=increments,
            )
        )
    return tuple(records)


def build_triangles(
    origins: Iterable[OriginRecord], valuation_index: int, terminal_age: int
) -> tuple[dict[str, dict[int, float]], dict[str, dict[int, float]]]:
    incremental: dict[str, dict[int, float]] = {}
    cumulative: dict[str, dict[int, float]] = {}
    for record in origins:
        max_observed = min(terminal_age, valuation_index - record.origin_index)
        running = 0.0
        incremental[record.origin_month] = {}
        cumulative[record.origin_month] = {}
        for age in range(max_observed + 1):
            value = record.increments[age]
            running += value
            incremental[record.origin_month][age] = value
            cumulative[record.origin_month][age] = running
    return incremental, cumulative


def calculate_factors(
    cumulative: dict[str, dict[int, float]], terminal_age: int
) -> tuple[dict[str, float | int | str], ...]:
    rows: list[dict[str, float | int | str]] = []
    for age in range(terminal_age):
        pairs = [
            (values[age], values[age + 1])
            for values in cumulative.values()
            if age in values and age + 1 in values
        ]
        denominator = sum(left for left, _ in pairs)
        numerator = sum(right for _, right in pairs)
        factor = numerator / denominator
        ratios = [right / left for left, right in pairs]
        ratio_cv = statistics.stdev(ratios) / statistics.mean(ratios) if len(ratios) > 1 else 0.0
        count = len(pairs)
        status = (
            "adecuado_demo"
            if count >= DEMO_FACTOR_THRESHOLD
            else "precaucion_demo"
            if count >= 12
            else "insuficiente_demo"
        )
        rows.append(
            {
                "development_from": age,
                "development_to": age + 1,
                "factor": factor,
                "observations": count,
                "ratio_cv": ratio_cv,
                "status": status,
            }
        )

    cdf = 1.0
    for row in reversed(rows):
        cdf *= float(row["factor"])
        row["cdf_to_terminal_age"] = cdf
    return tuple(rows)


def calculate_estimates(
    origins: Iterable[OriginRecord],
    cumulative: dict[str, dict[int, float]],
    factors: tuple[dict[str, float | int | str], ...],
    terminal_age: int,
    tail_factor: float,
) -> tuple[dict[str, float | int | str], ...]:
    factor_values = {int(row["development_from"]): float(row["factor"]) for row in factors}
    rows: list[dict[str, float | int | str]] = []
    for record in origins:
        observed = cumulative[record.origin_month]
        latest_age = max(observed)
        latest_paid = observed[latest_age]
        cdf_to_terminal = math.prod(factor_values[age] for age in range(latest_age, terminal_age))
        projected_terminal = latest_paid * cdf_to_terminal
        estimated_final_cost = projected_terminal * tail_factor
        unpaid_liability = estimated_final_cost - latest_paid
        error = estimated_final_cost - record.simulated_final_cost
        rows.append(
            {
                "origin_month": record.origin_month,
                "latest_development_month": latest_age,
                "latest_cumulative_paid": latest_paid,
                "cdf_to_terminal_age": cdf_to_terminal,
                "synthetic_tail_factor": tail_factor,
                "projected_terminal_cumulative": projected_terminal,
                "estimated_final_cost_with_tail": estimated_final_cost,
                "estimated_unpaid_claim_liability": unpaid_liability,
                "tail_provision": estimated_final_cost - projected_terminal,
                "simulated_true_final_cost": record.simulated_final_cost,
                "final_cost_error": error,
                "final_cost_error_pct": error / record.simulated_final_cost,
            }
        )
    return tuple(rows)


def build_demo(
    valuation_index: int,
    origin_months: int = DEFAULT_ORIGIN_MONTHS,
    development_months: int = DEFAULT_DEVELOPMENT_MONTHS,
    seed: int = DEFAULT_SEED,
    runoff_months: int = DEFAULT_RUNOFF_MONTHS,
) -> DemoResult:
    validate_parameters(origin_months, development_months, runoff_months)
    origins = simulate_origins(valuation_index, origin_months, runoff_months, seed)
    incremental, cumulative = build_triangles(origins, valuation_index, development_months)
    factors = calculate_factors(cumulative, development_months)
    tail_factor = 1.0 / cumulative_paid_pattern(development_months, runoff_months)
    estimates = calculate_estimates(origins, cumulative, factors, development_months, tail_factor)
    result = DemoResult(
        valuation_index=valuation_index,
        origins=origins,
        incremental=incremental,
        cumulative=cumulative,
        factors=factors,
        estimates=estimates,
        observed_cells=sum(len(values) for values in cumulative.values()),
        complete_origins=sum(development_months in values for values in cumulative.values()),
        terminal_age=development_months,
        runoff_age=runoff_months,
        synthetic_tail_factor=tail_factor,
        total_unpaid_claim_liability=sum(
            float(row["estimated_unpaid_claim_liability"]) for row in estimates
        ),
    )
    validate_result(result, origin_months)
    return result


def validate_result(result: DemoResult, origin_months: int) -> None:
    expected_cells = sum(
        min(result.terminal_age, age) + 1 for age in range(origin_months - 1, -1, -1)
    )
    if len(result.origins) != origin_months or result.observed_cells != expected_cells:
        raise RuntimeError("Triangle dimensions do not reconcile")
    for record in result.origins:
        running = 0.0
        for age, value in result.incremental[record.origin_month].items():
            running += value
            if not math.isclose(running, result.cumulative[record.origin_month][age], rel_tol=1e-12, abs_tol=0.01):
                raise RuntimeError(f"Incremental/cumulative mismatch for {record.origin_month}")
        if not math.isclose(sum(record.increments), record.simulated_final_cost, rel_tol=1e-12):
            raise RuntimeError(f"Full runoff does not reconcile for {record.origin_month}")
    if min(int(row["observations"]) for row in result.factors) != result.complete_origins:
        raise RuntimeError("The longest-link observation count does not reconcile")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def triangle_rows(
    triangle: dict[str, dict[int, float]], terminal_age: int, origin_key: str,
    origins: Iterable[str] | None = None,
) -> list[dict[str, object]]:
    selected = list(origins) if origins is not None else list(triangle)
    rows: list[dict[str, object]] = []
    for origin in selected:
        values = triangle[origin]
        row: dict[str, object] = {origin_key: origin}
        row.update(
            {f"dev_{age}": round(values[age], 2) if age in values else "" for age in range(terminal_age + 1)}
        )
        rows.append(row)
    return rows


def traditional_view_origins(result: DemoResult) -> list[str]:
    """Return the latest 36 origins, which form a traditional 36 x 36 triangle."""

    return [record.origin_month for record in result.origins[-TRADITIONAL_VIEW_SIZE:]]


def write_language_data(result: DemoResult, repo_root: Path, language: str, seed: int) -> None:
    labels = LABELS[language]
    data_dir = repo_root / "data" / labels["data_dir"]
    data_dir.mkdir(parents=True, exist_ok=True)
    origin_key = "mes_origen" if language == "es" else "origin_month"
    terminal_age = result.terminal_age
    record_map = {record.origin_month: record for record in result.origins}

    long_rows: list[dict[str, object]] = []
    for origin, values in result.incremental.items():
        record = record_map[origin]
        for age, incremental_value in values.items():
            common = {
                "mes_origen" if language == "es" else "origin_month": origin,
                "mes_pago" if language == "es" else "payment_month": month_label(record.origin_index + age),
                "mes_desarrollo" if language == "es" else "development_month": age,
                "miembros_mes" if language == "es" else "member_months": record.member_months,
                "indice_estacional" if language == "es" else "seasonal_index": round(record.seasonal_index, 6),
                "pago_incremental" if language == "es" else "incremental_paid": round(incremental_value, 2),
                "pago_acumulado" if language == "es" else "cumulative_paid": round(result.cumulative[origin][age], 2),
            }
            long_rows.append(common)
    write_csv(data_dir / labels["long"], list(long_rows[0]), long_rows)

    fields = [origin_key, *(f"dev_{age}" for age in range(terminal_age + 1))]
    write_csv(data_dir / labels["incremental"], fields, triangle_rows(result.incremental, terminal_age, origin_key))
    write_csv(data_dir / labels["cumulative"], fields, triangle_rows(result.cumulative, terminal_age, origin_key))
    write_csv(
        data_dir / labels["square"],
        fields,
        triangle_rows(result.cumulative, terminal_age, origin_key, traditional_view_origins(result)),
    )

    if language == "es":
        factor_rows = [
            {
                "desarrollo_desde": row["development_from"],
                "desarrollo_hasta": row["development_to"],
                "factor_edad_a_edad": f"{float(row['factor']):.8f}",
                "observaciones": row["observations"],
                "cv_ratios_individuales": f"{float(row['ratio_cv']):.8f}",
                "cdf_hasta_edad_35": f"{float(row['cdf_to_terminal_age']):.8f}",
                "estado_heuristica_demo": row["status"],
            }
            for row in result.factors
        ]
        estimate_rows = [
            {
                "mes_origen": row["origin_month"],
                "ultima_edad_observada": row["latest_development_month"],
                "pagado_acumulado_observado": f"{float(row['latest_cumulative_paid']):.2f}",
                "cdf_hasta_edad_35": f"{float(row['cdf_to_terminal_age']):.8f}",
                "factor_cola_sintetico_35_a_48": f"{float(row['synthetic_tail_factor']):.8f}",
                "acumulado_proyectado_edad_35": f"{float(row['projected_terminal_cumulative']):.2f}",
                "costo_final_estimado_con_cola": f"{float(row['estimated_final_cost_with_tail']):.2f}",
                "pasivo_no_pagado_estimado": f"{float(row['estimated_unpaid_claim_liability']):.2f}",
                "provision_cola": f"{float(row['tail_provision']):.2f}",
                "costo_final_real_simulado": f"{float(row['simulated_true_final_cost']):.2f}",
                "error_costo_final": f"{float(row['final_cost_error']):.2f}",
                "error_costo_final_pct": f"{float(row['final_cost_error_pct']):.8f}",
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
                "cdf_to_age_35": f"{float(row['cdf_to_terminal_age']):.8f}",
                "demo_heuristic_status": str(row["status"]).replace("adecuado", "adequate").replace("precaucion", "caution").replace("insuficiente", "insufficient"),
            }
            for row in result.factors
        ]
        estimate_rows = [
            {
                "origin_month": row["origin_month"],
                "latest_observed_age": row["latest_development_month"],
                "latest_cumulative_paid": f"{float(row['latest_cumulative_paid']):.2f}",
                "cdf_to_age_35": f"{float(row['cdf_to_terminal_age']):.8f}",
                "synthetic_tail_factor_35_to_48": f"{float(row['synthetic_tail_factor']):.8f}",
                "projected_cumulative_at_age_35": f"{float(row['projected_terminal_cumulative']):.2f}",
                "estimated_final_cost_with_tail": f"{float(row['estimated_final_cost_with_tail']):.2f}",
                "estimated_unpaid_claim_liability": f"{float(row['estimated_unpaid_claim_liability']):.2f}",
                "tail_provision": f"{float(row['tail_provision']):.2f}",
                "simulated_true_final_cost": f"{float(row['simulated_true_final_cost']):.2f}",
                "final_cost_error": f"{float(row['final_cost_error']):.2f}",
                "final_cost_error_pct": f"{float(row['final_cost_error_pct']):.8f}",
            }
            for row in result.estimates
        ]
    write_csv(data_dir / labels["factors"], list(factor_rows[0]), factor_rows)
    write_csv(data_dir / labels["results"], list(estimate_rows[0]), estimate_rows)

    prior_rows = []
    for record in result.origins:
        expected_rate = record.simulated_final_cost / record.member_months * 0.985
        if language == "es":
            prior_rows.append({
                "mes_origen": record.origin_month,
                "miembros_mes": record.member_months,
                "costo_esperado_por_miembro": f"{expected_rate:.6f}",
                "costo_final_esperado_prior": f"{record.member_months * expected_rate:.2f}",
                "ultimate_esperado": f"{record.member_months * expected_rate:.2f}",
            })
        else:
            prior_rows.append({
                "origin_month": record.origin_month,
                "member_months": record.member_months,
                "expected_cost_per_member": f"{expected_rate:.6f}",
                "expected_final_cost_prior": f"{record.member_months * expected_rate:.2f}",
                "expected_ultimate": f"{record.member_months * expected_rate:.2f}",
            })
    write_csv(data_dir / labels["prior"], list(prior_rows[0]), prior_rows)

    minimum_observations = min(int(row["observations"]) for row in result.factors)
    diagnostic_items = (
        ("meses_origen" if language == "es" else "origin_months", len(result.origins), "Seis años para estimar patrones y revisar estacionalidad." if language == "es" else "Six years for pattern estimation and seasonality review."),
        ("columnas_desarrollo" if language == "es" else "development_columns", terminal_age + 1, "Edades 0–35: 36 columnas." if language == "es" else "Ages 0–35: 36 columns."),
        ("vista_tradicional" if language == "es" else "traditional_view", "36x36", "Últimos 36 orígenes; presentación, no base completa de estimación." if language == "es" else "Latest 36 origins; a display, not the full estimation basis."),
        ("origenes_completos" if language == "es" else "complete_origins", result.complete_origins, "Orígenes observados hasta edad 35." if language == "es" else "Origins observed through age 35."),
        ("min_observaciones_factor" if language == "es" else "minimum_factor_observations", minimum_observations, "El enlace 34→35 conserva 37 observaciones." if language == "es" else "Link 34→35 retains 37 observations."),
        ("edad_runoff_simulado" if language == "es" else "simulated_runoff_age", result.runoff_age, "Permite validar una cola sintética 35→48." if language == "es" else "Supports validation of a synthetic 35→48 tail."),
    )
    diagnostic_rows = [
        {
            "indicador" if language == "es" else "metric": key,
            "valor" if language == "es" else "value": value,
            "lectura" if language == "es" else "interpretation": interpretation,
        }
        for key, value, interpretation in diagnostic_items
    ]
    write_csv(data_dir / labels["diagnostics"], list(diagnostic_rows[0]), diagnostic_rows)

    if language == "es":
        summary = f"""=== Demo mensual de triángulos pagados de salud r2 ===
Mes de valuación: {month_label(result.valuation_index)}
Base de estimación: {len(result.origins)} x {terminal_age + 1} (orígenes x edades 0-{terminal_age})
Vista actuarial tradicional: 36 x 36
Celdas observadas: {result.observed_cells}
Orígenes completos a edad {terminal_age}: {result.complete_origins}
Mínimo de observaciones por factor: {minimum_observations}
Runoff real simulado: 0-{result.runoff_age}
Factor de cola sintético {terminal_age}->{result.runoff_age}: {result.synthetic_tail_factor:.8f}
Pasivo no pagado estimado total: {result.total_unpaid_claim_liability:,.2f}
Semilla: {seed}
Advertencia: el residual pagado no identifica IBNR puro, RBNS ni IBNER por separado.
"""
        readme = f"""# Datos del demo mensual r2

Datos sintéticos con una base de estimación de **{len(result.origins)} x {terminal_age + 1}** y una vista tradicional **36 x 36**. El runoff completo se simula hasta edad {result.runoff_age}; la cola {terminal_age}->{result.runoff_age} es una hipótesis conocida del generador.

- `{labels['cumulative']}`: base completa para estimación.
- `{labels['square']}`: últimos 36 orígenes, presentación tradicional 36 x 36.
- `{labels['factors']}`: factores y observaciones por enlace.
- `{labels['results']}`: costo proyectado, cola y pasivo no pagado estimado.
- `{labels['prior']}`: prior sintético para BF/Benktander.

**Alcance:** con un triángulo agregado exclusivamente pagado no se separan IBNR puro, RBNS e IBNER. El resultado es educativo y no constituye una reserva contable.
"""
    else:
        summary = f"""=== Monthly paid-triangle demo r2 ===
Valuation month: {month_label(result.valuation_index)}
Estimation basis: {len(result.origins)} x {terminal_age + 1} (origins x ages 0-{terminal_age})
Traditional actuarial view: 36 x 36
Observed cells: {result.observed_cells}
Complete origins at age {terminal_age}: {result.complete_origins}
Minimum observations per factor: {minimum_observations}
Simulated true runoff: 0-{result.runoff_age}
Synthetic tail factor {terminal_age}->{result.runoff_age}: {result.synthetic_tail_factor:.8f}
Total estimated unpaid claim liability: {result.total_unpaid_claim_liability:,.2f}
Seed: {seed}
Warning: the paid residual does not identify pure IBNR, RBNS or IBNER separately.
"""
        readme = f"""# Monthly demo data r2

Synthetic data with a **{len(result.origins)} x {terminal_age + 1}** estimation basis and a traditional **36 x 36** view. Full runoff is simulated through age {result.runoff_age}; the {terminal_age}->{result.runoff_age} tail is a known generator assumption.

- `{labels['cumulative']}`: full estimation basis.
- `{labels['square']}`: latest 36 origins, traditional 36 x 36 presentation.
- `{labels['factors']}`: factors and observations per link.
- `{labels['results']}`: projected cost, tail and estimated unpaid claim liability.
- `{labels['prior']}`: synthetic BF/Benktander prior.

**Scope:** an aggregate paid-only triangle cannot split pure IBNR, RBNS and IBNER. This is an educational result, not a booked reserve.
"""
    (data_dir / labels["summary"]).write_text(summary, encoding="utf-8", newline="\n")
    (data_dir / "README.md").write_text(readme, encoding="utf-8", newline="\n")


def svg_escape(value: object) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_svg(path: Path, width: int, height: int, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">
<rect width="{width}" height="{height}" fill="#ffffff"/>
<style>text {{ font-family: Inter, Arial, sans-serif; fill:#1f2937; }} .title {{ font-size:24px;font-weight:700; }} .subtitle {{ font-size:13px;fill:#52606d; }} .label {{ font-size:9px; }} .value {{ font-size:7px;font-family:Menlo,monospace; }}</style>
{body}
</svg>
''',
        encoding="utf-8",
        newline="\n",
    )


def write_triangle_svg(result: DemoResult, path: Path, language: str) -> None:
    origins = traditional_view_origins(result)
    cell_w, cell_h, left, top = 42, 17, 100, 108
    width = left + TRADITIONAL_VIEW_SIZE * cell_w + 30
    height = top + TRADITIONAL_VIEW_SIZE * cell_h + 55
    title = "Vista actuarial tradicional 36 x 36" if language == "es" else "Traditional actuarial 36 x 36 view"
    subtitle = (
        "COP millones · últimos 36 orígenes · edades 0–35 · diagonal observada en amarillo"
        if language == "es"
        else "COP millions · latest 36 origins · ages 0–35 · observed diagonal in gold"
    )
    parts = [f'<text x="28" y="38" class="title">{title}</text>', f'<text x="28" y="62" class="subtitle">{subtitle}</text>']
    for age in range(TRADITIONAL_VIEW_SIZE):
        x = left + age * cell_w + cell_w / 2
        parts.append(f'<text x="{x}" y="91" class="label" text-anchor="middle">{age}</text>')
    for row_index, origin in enumerate(origins):
        y = top + row_index * cell_h
        parts.append(f'<text x="90" y="{y+12}" class="label" text-anchor="end">{origin}</text>')
        values = result.cumulative[origin]
        latest = max(values)
        for age in range(TRADITIONAL_VIEW_SIZE):
            x = left + age * cell_w
            if age in values:
                fill, stroke = ("#f6d365", "#a66f00") if age == latest else ("#edf4ff", "#cbd8ea")
                label = f"{values[age]/1_000_000:,.0f}"
            else:
                fill, stroke, label = "#fafafa", "#e5e7eb", ""
            parts.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="{stroke}" stroke-width=".7"/>')
            if label:
                parts.append(f'<text x="{x+cell_w-2}" y="{y+11.5}" class="value" text-anchor="end">{svg_escape(label)}</text>')
    write_svg(path, width, height, "\n".join(parts))


def empirical_maturity(result: DemoResult) -> list[float]:
    record_map = {record.origin_month: record for record in result.origins}
    complete = [origin for origin, values in result.cumulative.items() if result.terminal_age in values]
    return [
        statistics.mean(result.cumulative[origin][age] / record_map[origin].simulated_final_cost for origin in complete)
        for age in range(result.terminal_age + 1)
    ]


def write_curve_svg(result: DemoResult, path: Path, language: str) -> None:
    width, height, left, right, top, bottom = 920, 500, 85, 35, 100, 70
    plot_w, plot_h = width - left - right, height - top - bottom
    values = empirical_maturity(result)
    points = [
        f"{left+age/result.terminal_age*plot_w:.1f},{top+(1-value)*plot_h:.1f}"
        for age, value in enumerate(values)
    ]
    title = "Maduración pagada y cola sintética" if language == "es" else "Paid maturity and synthetic tail"
    subtitle = (
        f"Participación del costo final simulado · edad 35={values[-1]:.2%} · runoff final=48"
        if language == "es"
        else f"Share of simulated final cost · age 35={values[-1]:.2%} · final runoff=48"
    )
    parts = [f'<text x="28" y="38" class="title">{title}</text>', f'<text x="28" y="62" class="subtitle">{subtitle}</text>']
    for pct in (0.2, 0.4, 0.6, 0.8, 1.0):
        y = top + (1-pct)*plot_h
        parts.extend([f'<line x1="{left}" y1="{y}" x2="{width-right}" y2="{y}" stroke="#e5e7eb"/>', f'<text x="{left-12}" y="{y+4}" class="label" text-anchor="end">{pct:.0%}</text>'])
    parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#3659a7" stroke-width="3"/>')
    for age in (0, 3, 6, 12, 18, 24, 30, 35):
        x, y = left + age/result.terminal_age*plot_w, top + (1-values[age])*plot_h
        parts.extend([f'<circle cx="{x}" cy="{y}" r="4" fill="#fff" stroke="#3659a7" stroke-width="2"/>', f'<text x="{x}" y="{y-10}" class="label" text-anchor="middle">{values[age]:.1%}</text>'])
    write_svg(path, width, height, "\n".join(parts))


def write_observations_svg(result: DemoResult, path: Path, language: str) -> None:
    width, height, left, right, top, bottom = 920, 500, 85, 35, 105, 70
    plot_w, plot_h = width-left-right, height-top-bottom
    counts = [int(row["observations"]) for row in result.factors]
    max_y = max(counts) + 5
    bar_space = plot_w / len(counts)
    title = "Observaciones por factor mensual" if language == "es" else "Observations per monthly factor"
    subtitle = (
        "Base 72 x 36: el enlace 34→35 conserva 37 observaciones"
        if language == "es"
        else "72 x 36 basis: link 34→35 retains 37 observations"
    )
    parts = [f'<text x="28" y="38" class="title">{title}</text>', f'<text x="28" y="62" class="subtitle">{subtitle}</text>']
    threshold_y = top + (1-DEMO_FACTOR_THRESHOLD/max_y)*plot_h
    parts.append(f'<line x1="{left}" y1="{threshold_y}" x2="{width-right}" y2="{threshold_y}" stroke="#a66f00" stroke-width="2" stroke-dasharray="6 5"/>')
    for age, count in enumerate(counts):
        bar_h = count/max_y*plot_h
        x, y = left+age*bar_space+2, top+plot_h-bar_h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_space-4:.1f}" height="{bar_h:.1f}" fill="#3659a7"/>')
        if age % 5 == 0 or age == len(counts)-1:
            parts.append(f'<text x="{x+(bar_space-4)/2:.1f}" y="{top+plot_h+23}" class="label" text-anchor="middle">{age}→{age+1}</text>')
            parts.append(f'<text x="{x+(bar_space-4)/2:.1f}" y="{y-5}" class="label" text-anchor="middle">{count}</text>')
    write_svg(path, width, height, "\n".join(parts))


def write_language_assets(result: DemoResult, repo_root: Path, language: str) -> None:
    labels = LABELS[language]
    asset_dir = repo_root / "docs" / "assets" / labels["asset_dir"]
    write_triangle_svg(result, asset_dir / labels["triangle_svg"], language)
    write_curve_svg(result, asset_dir / labels["curve_svg"], language)
    write_observations_svg(result, asset_dir / labels["observations_svg"], language)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=("es", "en", "both"), default="both")
    parser.add_argument("--valuation-month", default=DEFAULT_VALUATION_MONTH)
    parser.add_argument("--origin-months", type=int, default=DEFAULT_ORIGIN_MONTHS)
    parser.add_argument("--development-months", type=int, default=DEFAULT_DEVELOPMENT_MONTHS)
    parser.add_argument("--runoff-months", type=int, default=DEFAULT_RUNOFF_MONTHS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    result = build_demo(
        valuation_index=parse_month(args.valuation_month),
        origin_months=args.origin_months,
        development_months=args.development_months,
        runoff_months=args.runoff_months,
        seed=args.seed,
    )
    for language in (("es", "en") if args.language == "both" else (args.language,)):
        write_language_data(result, repo_root, language, args.seed)
        write_language_assets(result, repo_root, language)
    print("=== Demo mensual r2: proyección de pasivo no pagado ===")
    print(f"Base / Basis: {len(result.origins)} x {result.terminal_age + 1}")
    print("Vista tradicional / Traditional view: 36 x 36")
    print(f"Runoff simulado / Simulated runoff: 0-{result.runoff_age}")
    print(f"Factor de cola sintético / Synthetic tail: {result.synthetic_tail_factor:.8f}")
    print(f"Pasivo no pagado estimado / Estimated unpaid claim liability: {result.total_unpaid_claim_liability:,.2f}")
    print("Nota: el resultado no identifica IBNR puro, RBNS ni IBNER por separado.")
    print("OK: monthly r2 files generated / archivos mensuales r2 generados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
