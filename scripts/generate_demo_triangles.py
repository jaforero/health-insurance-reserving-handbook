#!/usr/bin/env python3
"""Generate a reproducible demo of health insurance paid claims triangles.

The script creates synthetic health claims development data and converts it into:

- long-format observed paid claims by origin year and development age;
- incremental paid triangle;
- cumulative paid triangle;
- volume-weighted age-to-age factors;
- simple deterministic Chain Ladder ultimate and IBNR estimates.

No external Python dependencies are required.

Usage:
    python scripts/generate_demo_triangles.py

Optional:
    python scripts/generate_demo_triangles.py --seed 20260714 --output-dir data/demo_triangles
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path


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


def payment_pattern(max_dev_age: int) -> list[float]:
    """Return cumulative paid emergence percentages by development age.

    The pattern is intentionally plausible for a health portfolio with fast early
    reporting/payment and a modest tail from audit, glosas, disputes, coordination
    of benefits, late provider submissions, and reprocessing.
    """

    base = [
        0.38,
        0.61,
        0.75,
        0.84,
        0.90,
        0.94,
        0.965,
        0.982,
        0.993,
        1.000,
    ]

    if max_dev_age + 1 <= len(base):
        return base[: max_dev_age + 1]

    # Extend with a flat tail if a larger development horizon is requested.
    return base + [1.0] * (max_dev_age + 1 - len(base))


def incremental_pattern(cumulative_pattern: list[float]) -> list[float]:
    increments: list[float] = []
    previous = 0.0
    for value in cumulative_pattern:
        increments.append(max(value - previous, 0.0))
        previous = value
    return increments


def calendar_shock(payment_year: int) -> float:
    """Simple calendar effects to make the demo realistic but stable."""

    shocks = {
        2020: 0.93,  # lower elective utilization / payment disruption
        2021: 1.08,  # rebound and backlog
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
    cumulative = payment_pattern(max_dev_age)
    incremental = incremental_pattern(cumulative)
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

        base_frequency_per_1000_member_months = 145.0 * (1 + utilization_drift) ** index
        average_paid_per_claim = 128_000.0 * (1 + medical_trend) ** index

        ultimate_claim_count = (
            exposure / 1_000.0 * base_frequency_per_1000_member_months * morbidity_mix
        )
        ultimate_paid = ultimate_claim_count * average_paid_per_claim
        ultimate_paid *= rng.lognormvariate(mu=-0.5 * 0.045**2, sigma=0.045)

        for development_age, emergence_share in enumerate(incremental):
            payment_year = origin_year + development_age
            if payment_year > valuation_year:
                continue

            volatility = 0.13 if development_age <= 1 else 0.08
            noise = rng.lognormvariate(mu=-0.5 * volatility**2, sigma=volatility)

            paid_amount = ultimate_paid * emergence_share * calendar_shock(payment_year) * noise
            paid_amount = max(paid_amount, 0.0)

            count_noise = rng.lognormvariate(mu=-0.5 * 0.08**2, sigma=0.08)
            claim_count = int(max(1, round(ultimate_claim_count * emergence_share * count_noise)))

            rows.append(
                ObservedClaimCell(
                    origin_year=origin_year,
                    development_age=development_age,
                    payment_year=payment_year,
                    exposure_member_months=exposure,
                    simulated_ultimate_paid=ultimate_paid,
                    paid_amount=paid_amount,
                    claim_count=claim_count,
                )
            )

    return rows


def build_incremental_triangle(
    rows: list[ObservedClaimCell],
    origin_years: list[int],
    max_dev_age: int,
) -> dict[int, dict[int, float]]:
    triangle = {origin: {age: None for age in range(max_dev_age + 1)} for origin in origin_years}
    for row in rows:
        triangle[row.origin_year][row.development_age] = (
            triangle[row.origin_year].get(row.development_age) or 0.0
        ) + row.paid_amount
    return triangle


def build_cumulative_triangle(
    incremental: dict[int, dict[int, float]],
    max_dev_age: int,
) -> dict[int, dict[int, float]]:
    cumulative: dict[int, dict[int, float]] = {}
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
    cumulative: dict[int, dict[int, float]],
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


def latest_observed_age(values: dict[int, float]) -> int | None:
    ages = [age for age, value in values.items() if value is not None]
    return max(ages) if ages else None


def chain_ladder_results(
    cumulative: dict[int, dict[int, float]],
    factors: list[dict[str, float | int]],
    max_dev_age: int,
) -> list[dict[str, float | int]]:
    results: list[dict[str, float | int]] = []

    for origin_year, values in sorted(cumulative.items()):
        latest_age = latest_observed_age(values)
        if latest_age is None:
            continue

        latest_paid = float(values[latest_age])
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


def write_long_claims(path: Path, rows: list[ObservedClaimCell]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "origin_year",
                "development_age",
                "payment_year",
                "exposure_member_months",
                "simulated_ultimate_paid",
                "paid_amount",
                "claim_count",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "origin_year": row.origin_year,
                    "development_age": row.development_age,
                    "payment_year": row.payment_year,
                    "exposure_member_months": row.exposure_member_months,
                    "simulated_ultimate_paid": round(row.simulated_ultimate_paid, 2),
                    "paid_amount": round(row.paid_amount, 2),
                    "claim_count": row.claim_count,
                }
            )


def write_triangle(
    path: Path,
    triangle: dict[int, dict[int, float]],
    max_dev_age: int,
) -> None:
    fieldnames = ["origin_year"] + [f"dev_{age}" for age in range(max_dev_age + 1)]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for origin_year, values in sorted(triangle.items()):
            row = {"origin_year": origin_year}
            for age in range(max_dev_age + 1):
                value = values.get(age)
                row[f"dev_{age}"] = "" if value is None else round(value, 2)
            writer.writerow(row)


def write_dict_rows(path: Path, rows: list[dict[str, float | int]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for item in rows:
            formatted = {}
            for key, value in item.items():
                if isinstance(value, float):
                    formatted[key] = round(value, 6) if "factor" in key or "cdf" in key else round(value, 2)
                else:
                    formatted[key] = value
            writer.writerow(formatted)


def write_summary(
    path: Path,
    *,
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
- Future extensions can add incurred triangles, bootstrap uncertainty, GLMs, calendar effects, and health-specific claim adjudication states.
"""
    path.write_text(text, encoding="utf-8")


def write_data_readme(path: Path) -> None:
    text = """# Demo data: simulated health paid claims triangles

This folder contains reproducible synthetic data generated by:

```bash
python scripts/generate_demo_triangles.py
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--origin-start", type=int, default=DEFAULT_ORIGIN_START)
    parser.add_argument("--origin-end", type=int, default=DEFAULT_ORIGIN_END)
    parser.add_argument("--valuation-year", type=int, default=DEFAULT_VALUATION_YEAR)
    parser.add_argument("--max-dev-age", type=int, default=DEFAULT_MAX_DEV_AGE)
    parser.add_argument("--output-dir", default="data/demo_triangles")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.origin_end < args.origin_start:
        raise ValueError("--origin-end must be greater than or equal to --origin-start")

    if args.max_dev_age < 1:
        raise ValueError("--max-dev-age must be at least 1")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

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

    write_long_claims(output_dir / "demo_health_paid_claims_long.csv", rows)
    write_triangle(output_dir / "paid_incremental_triangle.csv", incremental, args.max_dev_age)
    write_triangle(output_dir / "paid_cumulative_triangle.csv", cumulative, args.max_dev_age)
    write_dict_rows(output_dir / "age_to_age_factors.csv", factors)
    write_dict_rows(output_dir / "chain_ladder_results.csv", results)
    write_summary(
        output_dir / "run_summary.txt",
        seed=args.seed,
        origin_start=args.origin_start,
        origin_end=args.origin_end,
        valuation_year=args.valuation_year,
        max_dev_age=args.max_dev_age,
        rows=rows,
        results=results,
    )
    write_data_readme(output_dir / "README.md")

    total_ibnr = sum(float(row["chain_ladder_ibnr"]) for row in results)
    print("=== Simulated health paid triangle demo ===")
    print(f"Output directory: {output_dir}")
    print(f"Observed cells: {len(rows)}")
    print(f"Origin years: {args.origin_start}-{args.origin_end}")
    print(f"Valuation year: {args.valuation_year}")
    print(f"Total Chain Ladder IBNR: {total_ibnr:,.2f}")
    print("OK: demo files generated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

