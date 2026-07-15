#!/usr/bin/env python3
"""Generate bilingual simulated health claims triangles.

Default behavior generates both:

- Spanish output in `data/demo_triangulos`
- English output in `data/demo_triangles`

No external Python dependencies are required.

Usage:
    python scripts/generate_demo_triangles.py
    python scripts/generate_demo_triangles.py --language es
    python scripts/generate_demo_triangles.py --language en
    python scripts/generate_demo_triangles.py --language both
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


Language = Literal["es", "en"]

DEFAULT_ORIGIN_START = 2016
DEFAULT_ORIGIN_END = 2025
DEFAULT_VALUATION_YEAR = 2025
DEFAULT_MAX_DEV_AGE = 9


@dataclass(frozen=True)
class ObservedClaimCell:
    origin_year: int
    development_age: int
    payment_year: int
    exposure_member_months: int
    simulated_ultimate_paid: float
    paid_amount: float
    claim_count: int


TRANSLATIONS = {
    "es": {
        "output_dir": "data/demo_triangulos",
        "long_file": "reclamaciones_pagadas_largo.csv",
        "incremental_file": "triangulo_pagado_incremental.csv",
        "cumulative_file": "triangulo_pagado_acumulado.csv",
        "factors_file": "factores_edad_a_edad.csv",
        "results_file": "resultados_chain_ladder.csv",
        "summary_file": "resumen_ejecucion.txt",
        "console_title": "=== Demo de triángulos pagados simulados de salud ===",
        "ok": "OK: archivos del demo generados.",
        "observed_cells": "Celdas observadas",
        "origin_years": "Años de origen",
        "valuation_year": "Año de valuación",
        "total_ibnr": "IBNR total Chain Ladder",
        "fields_long": {
            "origin_year": "anio_origen",
            "development_age": "edad_desarrollo",
            "payment_year": "anio_pago",
            "exposure_member_months": "exposicion_meses_miembro",
            "simulated_ultimate_paid": "ultimo_pagado_simulado",
            "paid_amount": "monto_pagado",
            "claim_count": "numero_reclamaciones",
        },
        "fields_factors": {
            "development_age_from": "edad_desarrollo_desde",
            "development_age_to": "edad_desarrollo_hasta",
            "origins_used": "anios_origen_usados",
            "volume_weighted_factor": "factor_ponderado_por_volumen",
        },
        "fields_results": {
            "origin_year": "anio_origen",
            "latest_observed_development_age": "ultima_edad_desarrollo_observada",
            "latest_cumulative_paid": "pagado_acumulado_observado",
            "selected_cdf_to_ultimate": "cdf_seleccionado_a_ultimate",
            "chain_ladder_ultimate_paid": "ultimate_pagado_chain_ladder",
            "chain_ladder_ibnr": "ibnr_chain_ladder",
        },
    },
    "en": {
        "output_dir": "data/demo_triangles",
        "long_file": "demo_health_paid_claims_long.csv",
        "incremental_file": "paid_incremental_triangle.csv",
        "cumulative_file": "paid_cumulative_triangle.csv",
        "factors_file": "age_to_age_factors.csv",
        "results_file": "chain_ladder_results.csv",
        "summary_file": "run_summary.txt",
        "console_title": "=== Simulated health paid triangle demo ===",
        "ok": "OK: demo files generated.",
        "observed_cells": "Observed cells",
        "origin_years": "Origin years",
        "valuation_year": "Valuation year",
        "total_ibnr": "Total Chain Ladder IBNR",
        "fields_long": {
            "origin_year": "origin_year",
            "development_age": "development_age",
            "payment_year": "payment_year",
            "exposure_member_months": "exposure_member_months",
            "simulated_ultimate_paid": "simulated_ultimate_paid",
            "paid_amount": "paid_amount",
            "claim_count": "claim_count",
        },
        "fields_factors": {
            "development_age_from": "development_age_from",
            "development_age_to": "development_age_to",
            "origins_used": "origins_used",
            "volume_weighted_factor": "volume_weighted_factor",
        },
        "fields_results": {
            "origin_year": "origin_year",
            "latest_observed_development_age": "latest_observed_development_age",
            "latest_cumulative_paid": "latest_cumulative_paid",
            "selected_cdf_to_ultimate": "selected_cdf_to_ultimate",
            "chain_ladder_ultimate_paid": "chain_ladder_ultimate_paid",
            "chain_ladder_ibnr": "chain_ladder_ibnr",
        },
    },
}


def payment_pattern(max_dev_age: int) -> list[float]:
    base = [0.38, 0.61, 0.75, 0.84, 0.90, 0.94, 0.965, 0.982, 0.993, 1.0]
    if max_dev_age + 1 <= len(base):
        return base[: max_dev_age + 1]
    return base + [1.0] * (max_dev_age + 1 - len(base))


def incremental_pattern(cumulative_pattern: list[float]) -> list[float]:
    increments: list[float] = []
    previous = 0.0
    for value in cumulative_pattern:
        increments.append(max(value - previous, 0.0))
        previous = value
    return increments


def calendar_shock(payment_year: int) -> float:
    shocks = {
        2020: 0.93,
        2021: 1.08,
        2022: 1.05,
        2024: 1.03,
    }
    return shocks.get(payment_year, 1.0)


def simulate_observed_cells(
    *,
    seed: int,
    origin_start: int,
    origin_end: int,
    valuation_year: int,
    max_dev_age: int,
) -> list[ObservedClaimCell]:
    rng = random.Random(seed)
    incremental = incremental_pattern(payment_pattern(max_dev_age))
    rows: list[ObservedClaimCell] = []

    for index, origin_year in enumerate(range(origin_start, origin_end + 1)):
        exposure = int(
            780_000
            * (1.035**index)
            * rng.lognormvariate(mu=-0.5 * 0.035**2, sigma=0.035)
        )

        medical_trend = 0.072
        utilization_drift = 0.018
        morbidity_mix = 1.0 + 0.012 * math.sin(index / 2.0)

        base_frequency = 145.0 * (1 + utilization_drift) ** index
        average_paid_per_claim = 128_000.0 * (1 + medical_trend) ** index

        ultimate_claim_count = exposure / 1_000.0 * base_frequency * morbidity_mix
        ultimate_paid = ultimate_claim_count * average_paid_per_claim
        ultimate_paid *= rng.lognormvariate(mu=-0.5 * 0.045**2, sigma=0.045)

        for development_age, emergence_share in enumerate(incremental):
            payment_year = origin_year + development_age
            if payment_year > valuation_year:
                continue

            volatility = 0.13 if development_age <= 1 else 0.08
            noise = rng.lognormvariate(mu=-0.5 * volatility**2, sigma=volatility)
            paid_amount = ultimate_paid * emergence_share * calendar_shock(payment_year) * noise

            count_noise = rng.lognormvariate(mu=-0.5 * 0.08**2, sigma=0.08)
            claim_count = int(max(1, round(ultimate_claim_count * emergence_share * count_noise)))

            rows.append(
                ObservedClaimCell(
                    origin_year=origin_year,
                    development_age=development_age,
                    payment_year=payment_year,
                    exposure_member_months=exposure,
                    simulated_ultimate_paid=ultimate_paid,
                    paid_amount=max(paid_amount, 0.0),
                    claim_count=claim_count,
                )
            )

    return rows


def build_incremental_triangle(
    rows: list[ObservedClaimCell],
    origin_years: list[int],
    max_dev_age: int,
) -> dict[int, dict[int, float | None]]:
    triangle: dict[int, dict[int, float | None]] = {
        origin: {age: None for age in range(max_dev_age + 1)} for origin in origin_years
    }
    for row in rows:
        current = triangle[row.origin_year][row.development_age]
        triangle[row.origin_year][row.development_age] = (current or 0.0) + row.paid_amount
    return triangle


def build_cumulative_triangle(
    incremental: dict[int, dict[int, float | None]],
    max_dev_age: int,
) -> dict[int, dict[int, float | None]]:
    cumulative: dict[int, dict[int, float | None]] = {}
    for origin_year, values in incremental.items():
        running = 0.0
        cumulative[origin_year] = {}
        for age in range(max_dev_age + 1):
            value = values.get(age)
            if value is None:
                cumulative[origin_year][age] = None
            else:
                running += value
                cumulative[origin_year][age] = running
    return cumulative


def selected_age_to_age_factors(
    cumulative: dict[int, dict[int, float | None]],
    max_dev_age: int,
) -> list[dict[str, float | int]]:
    factors: list[dict[str, float | int]] = []
    for age in range(max_dev_age):
        numerator = 0.0
        denominator = 0.0
        origins_used = 0

        for values in cumulative.values():
            current = values.get(age)
            next_value = values.get(age + 1)
            if current is None or next_value is None or current <= 0:
                continue
            numerator += next_value
            denominator += current
            origins_used += 1

        factor = numerator / denominator if denominator else 1.0
        factors.append(
            {
                "development_age_from": age,
                "development_age_to": age + 1,
                "origins_used": origins_used,
                "volume_weighted_factor": factor,
            }
        )
    return factors


def cumulative_development_factor(
    factors: list[dict[str, float | int]],
    latest_age: int,
    max_dev_age: int,
) -> float:
    cdf = 1.0
    for item in factors:
        age_from = int(item["development_age_from"])
        if latest_age <= age_from < max_dev_age:
            cdf *= float(item["volume_weighted_factor"])
    return cdf


def latest_observed_age(values: dict[int, float | None]) -> int | None:
    ages = [age for age, value in values.items() if value is not None]
    return max(ages) if ages else None


def chain_ladder_results(
    cumulative: dict[int, dict[int, float | None]],
    factors: list[dict[str, float | int]],
    max_dev_age: int,
) -> list[dict[str, float | int]]:
    results: list[dict[str, float | int]] = []
    for origin_year, values in sorted(cumulative.items()):
        latest_age = latest_observed_age(values)
        if latest_age is None:
            continue
        latest_paid = float(values[latest_age] or 0.0)
        cdf = cumulative_development_factor(factors, latest_age, max_dev_age)
        ultimate = latest_paid * cdf
        ibnr = ultimate - latest_paid
        results.append(
            {
                "origin_year": origin_year,
                "latest_observed_development_age": latest_age,
                "latest_cumulative_paid": latest_paid,
                "selected_cdf_to_ultimate": cdf,
                "chain_ladder_ultimate_paid": ultimate,
                "chain_ladder_ibnr": ibnr,
            }
        )
    return results


def localized_fields(language: Language, group: str) -> dict[str, str]:
    return TRANSLATIONS[language][group]  # type: ignore[return-value]


def format_value(value: float | int | str | None, *, factor: bool = False) -> str | int | float:
    if value is None:
        return ""
    if isinstance(value, float):
        return round(value, 6) if factor else round(value, 2)
    return value


def write_long_claims(path: Path, rows: list[ObservedClaimCell], language: Language) -> None:
    fields = localized_fields(language, "fields_long")
    fieldnames = list(fields.values())

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    fields["origin_year"]: row.origin_year,
                    fields["development_age"]: row.development_age,
                    fields["payment_year"]: row.payment_year,
                    fields["exposure_member_months"]: row.exposure_member_months,
                    fields["simulated_ultimate_paid"]: round(row.simulated_ultimate_paid, 2),
                    fields["paid_amount"]: round(row.paid_amount, 2),
                    fields["claim_count"]: row.claim_count,
                }
            )


def write_triangle(
    path: Path,
    triangle: dict[int, dict[int, float | None]],
    max_dev_age: int,
    language: Language,
) -> None:
    origin_field = "anio_origen" if language == "es" else "origin_year"
    fieldnames = [origin_field] + [f"dev_{age}" for age in range(max_dev_age + 1)]

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for origin_year, values in sorted(triangle.items()):
            row: dict[str, str | int | float] = {origin_field: origin_year}
            for age in range(max_dev_age + 1):
                value = values.get(age)
                row[f"dev_{age}"] = "" if value is None else round(value, 2)
            writer.writerow(row)


def write_dict_rows(
    path: Path,
    rows: list[dict[str, float | int]],
    language: Language,
    group: str,
) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fields = localized_fields(language, group)
    fieldnames = [fields[key] for key in rows[0].keys()]

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in rows:
            output = {}
            for key, value in item.items():
                output[fields[key]] = format_value(
                    value,
                    factor=("factor" in key or "cdf" in key),
                )
            writer.writerow(output)


def write_summary(
    path: Path,
    *,
    language: Language,
    seed: int,
    origin_start: int,
    origin_end: int,
    valuation_year: int,
    max_dev_age: int,
    rows: list[ObservedClaimCell],
    results: list[dict[str, float | int]],
) -> None:
    total_latest_paid = sum(float(row["latest_cumulative_paid"]) for row in results)
    total_ultimate = sum(float(row["chain_ladder_ultimate_paid"]) for row in results)
    total_ibnr = sum(float(row["chain_ladder_ibnr"]) for row in results)

    if language == "es":
        text = f"""Resumen de ejecución del demo de triángulos
============================================

Semilla: {seed}
Años de origen: {origin_start}-{origin_end}
Año de valuación: {valuation_year}
Edad máxima de desarrollo: {max_dev_age}
Celdas observadas: {len(rows)}

Pagado acumulado observado total: {total_latest_paid:,.2f}
Ultimate pagado Chain Ladder total: {total_ultimate:,.2f}
IBNR Chain Ladder total: {total_ibnr:,.2f}

Interpretación:
- Los datos son sintéticos y reproducibles.
- Los montos son unidades monetarias nominales simuladas.
- El resultado es una demostración determinística de Chain Ladder, no un modelo productivo de reservas.
- Extensiones futuras pueden incorporar triángulos incurridos, bootstrap, GLM, efectos calendario, glosas, auditoría y estados administrativos.
"""
    else:
        text = f"""Demo triangles run summary
==========================

Seed: {seed}
Origin years: {origin_start}-{origin_end}
Valuation year: {valuation_year}
Maximum development age: {max_dev_age}
Observed cells: {len(rows)}

Total latest cumulative paid: {total_latest_paid:,.2f}
Total Chain Ladder ultimate paid: {total_ultimate:,.2f}
Total Chain Ladder IBNR: {total_ibnr:,.2f}

Interpretation:
- The data are synthetic and reproducible.
- Amounts are nominal simulated currency units.
- The result is a deterministic Chain Ladder demonstration, not a production reserving model.
- Future extensions can add incurred triangles, bootstrap uncertainty, GLMs, calendar effects, claim audit, disputes, and administrative states.
"""

    path.write_text(text, encoding="utf-8")


def write_data_readme(path: Path, language: Language) -> None:
    if language == "es":
        text = """# Datos demo: triángulos simulados de reclamaciones pagadas de salud

Esta carpeta contiene datos sintéticos reproducibles generados con:

```bash
python scripts/generate_demo_triangles.py --language es
```

Archivos:

- `reclamaciones_pagadas_largo.csv`: pagos sintéticos observados por año de origen y edad de desarrollo.
- `triangulo_pagado_incremental.csv`: triángulo pagado incremental.
- `triangulo_pagado_acumulado.csv`: triángulo pagado acumulado.
- `factores_edad_a_edad.csv`: factores de desarrollo seleccionados, ponderados por volumen.
- `resultados_chain_ladder.csv`: pagado observado, CDF seleccionado, ultimate e IBNR por año de origen.
- `resumen_ejecucion.txt`: resumen de ejecución.

Los datos son sintéticos y no deben interpretarse como experiencia real de un portafolio.
"""
    else:
        text = """# Demo data: simulated health paid claims triangles

This folder contains reproducible synthetic data generated with:

```bash
python scripts/generate_demo_triangles.py --language en
```

Files:

- `demo_health_paid_claims_long.csv`: observed synthetic claim payments by origin year and development age.
- `paid_incremental_triangle.csv`: paid incremental triangle.
- `paid_cumulative_triangle.csv`: paid cumulative triangle.
- `age_to_age_factors.csv`: selected volume-weighted development factors.
- `chain_ladder_results.csv`: latest paid, selected CDF, ultimate and IBNR by origin year.
- `run_summary.txt`: concise run summary.

The data are synthetic and must not be interpreted as real portfolio experience.
"""

    path.write_text(text, encoding="utf-8")


def write_outputs(
    *,
    language: Language,
    rows: list[ObservedClaimCell],
    incremental: dict[int, dict[int, float | None]],
    cumulative: dict[int, dict[int, float | None]],
    factors: list[dict[str, float | int]],
    results: list[dict[str, float | int]],
    seed: int,
    origin_start: int,
    origin_end: int,
    valuation_year: int,
    max_dev_age: int,
    output_dir: Path | None,
) -> Path:
    config = TRANSLATIONS[language]
    base_dir = output_dir or Path(str(config["output_dir"]))
    base_dir.mkdir(parents=True, exist_ok=True)

    write_long_claims(base_dir / str(config["long_file"]), rows, language)
    write_triangle(base_dir / str(config["incremental_file"]), incremental, max_dev_age, language)
    write_triangle(base_dir / str(config["cumulative_file"]), cumulative, max_dev_age, language)
    write_dict_rows(base_dir / str(config["factors_file"]), factors, language, "fields_factors")
    write_dict_rows(base_dir / str(config["results_file"]), results, language, "fields_results")
    write_summary(
        base_dir / str(config["summary_file"]),
        language=language,
        seed=seed,
        origin_start=origin_start,
        origin_end=origin_end,
        valuation_year=valuation_year,
        max_dev_age=max_dev_age,
        rows=rows,
        results=results,
    )
    write_data_readme(base_dir / "README.md", language)

    return base_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--origin-start", type=int, default=DEFAULT_ORIGIN_START)
    parser.add_argument("--origin-end", type=int, default=DEFAULT_ORIGIN_END)
    parser.add_argument("--valuation-year", type=int, default=DEFAULT_VALUATION_YEAR)
    parser.add_argument("--max-dev-age", type=int, default=DEFAULT_MAX_DEV_AGE)
    parser.add_argument(
        "--language",
        choices=["es", "en", "both"],
        default="both",
        help="Output language. Default generates Spanish and English outputs.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional output directory. Only valid when --language is es or en.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.output_dir and args.language == "both":
        raise ValueError("--output-dir can only be used with --language es or --language en")

    if args.origin_end < args.origin_start:
        raise ValueError("--origin-end must be greater than or equal to --origin-start")

    if args.max_dev_age < 1:
        raise ValueError("--max-dev-age must be at least 1")

    origin_years = list(range(args.origin_start, args.origin_end + 1))
    rows = simulate_observed_cells(
        seed=args.seed,
        origin_start=args.origin_start,
        origin_end=args.origin_end,
        valuation_year=args.valuation_year,
        max_dev_age=args.max_dev_age,
    )
    incremental = build_incremental_triangle(rows, origin_years, args.max_dev_age)
    cumulative = build_cumulative_triangle(incremental, args.max_dev_age)
    factors = selected_age_to_age_factors(cumulative, args.max_dev_age)
    results = chain_ladder_results(cumulative, factors, args.max_dev_age)

    languages: list[Language] = ["es", "en"] if args.language == "both" else [args.language]

    generated_dirs: list[Path] = []
    for language in languages:
        generated_dirs.append(
            write_outputs(
                language=language,
                rows=rows,
                incremental=incremental,
                cumulative=cumulative,
                factors=factors,
                results=results,
                seed=args.seed,
                origin_start=args.origin_start,
                origin_end=args.origin_end,
                valuation_year=args.valuation_year,
                max_dev_age=args.max_dev_age,
                output_dir=Path(args.output_dir) if args.output_dir else None,
            )
        )

    total_ibnr = sum(float(row["chain_ladder_ibnr"]) for row in results)
    print("=== Demo bilingüe de triángulos pagados simulados de salud ===")
    for directory in generated_dirs:
        print(f"Output directory: {directory}")
    print(f"Celdas observadas / Observed cells: {len(rows)}")
    print(f"Años de origen / Origin years: {args.origin_start}-{args.origin_end}")
    print(f"Año de valuación / Valuation year: {args.valuation_year}")
    print(f"IBNR total Chain Ladder / Total Chain Ladder IBNR: {total_ibnr:,.2f}")
    print("OK: archivos del demo generados / demo files generated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

