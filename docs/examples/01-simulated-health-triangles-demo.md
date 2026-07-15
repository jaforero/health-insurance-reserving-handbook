---
title: Practical demo of simulated health claims triangles
description: Reproducible Python example to build paid triangles, age-to-age factors, and a Chain Ladder IBNR estimate with simulated data.
status: draft
version: "0.1.2"
chapter: "example-01-en"
part: "examples"
language: "en"
last_updated: "2026-07-14"
---

# Practical demo of simulated health claims triangles

This demo turns development triangle theory into a reproducible exercise. The goal is for the repository to work not only as a conceptual handbook, but also as a practical base for running models, validating assumptions, and showing results.

The Spanish output is the primary version for the Colombian context. This English version is included for bilingual use, documentation, teaching, and collaboration.

## What the demo generates

The script generates:

- observed long-format paid claims by origin year and development age;
- paid incremental triangle;
- paid cumulative triangle;
- volume-weighted age-to-age factors;
- ultimate and IBNR estimates by origin year;
- execution summary.

The data are synthetic and do not represent real experience from any insurer, EPS, provider, benefit administrator, or specific portfolio.

## Recommended execution

From the repository root:

```bash
python scripts/generate_demo_triangles.py
```

By default, two outputs are generated:

```text
data/demo_triangulos/   # Spanish version
data/demo_triangles/    # English version
```

To generate only Spanish:

```bash
python scripts/generate_demo_triangles.py --language es
```

To generate only English:

```bash
python scripts/generate_demo_triangles.py --language en
```

## English output files

```text
data/demo_triangles/demo_health_paid_claims_long.csv
data/demo_triangles/paid_incremental_triangle.csv
data/demo_triangles/paid_cumulative_triangle.csv
data/demo_triangles/age_to_age_factors.csv
data/demo_triangles/chain_ladder_results.csv
data/demo_triangles/run_summary.txt
```

## Actuarial logic

The demo follows this flow:

1. Simulate origin years.
2. Assign exposure in member-months.
3. Simulate frequency, severity, medical trend, and morbidity mix.
4. Apply a cumulative paid emergence pattern.
5. Generate observed payments up to the valuation year.
6. Build incremental and cumulative triangles.
7. Calculate volume-weighted age-to-age factors.
8. Project ultimate using Chain Ladder.
9. Calculate IBNR as ultimate minus observed cumulative paid.

## Core formulas

For origin year \(i\) and development age \(j\), the selected age-to-age factor is:

$$
f_j =
\frac{\sum_i C_{i,j+1}}{\sum_i C_{i,j}}
$$

where:

- \(C_{i,j}\) is cumulative paid for origin year \(i\) at development age \(j\);
- the sum uses only origin years with available observations at both \(j\) and \(j+1\).

The cumulative development factor to ultimate for an origin year with latest observed age \(k\) is:

$$
CDF_k = \prod_{j=k}^{J-1} f_j
$$

Ultimate and IBNR are estimated as:

$$
Ultimate_i = C_{i,k} \cdot CDF_k
$$

$$
IBNR_i = Ultimate_i - C_{i,k}
$$

## Expected interpretation

Older origin years should be almost fully developed. More recent origin years should have a larger undeveloped share and, therefore, larger estimated IBNR.

This pattern demonstrates three core ideas:

- the observed diagonal limits available information;
- development factors transfer historical emergence into immature origin years;
- IBNR increases when an origin year has lower observed maturity.

## Limitations

This demo is intentionally simple:

- it does not estimate uncertainty;
- it does not calculate confidence intervals;
- it does not include bootstrap;
- it does not model denials, audit, recoveries, or administrative states;
- it does not separate paid and incurred triangles;
- it does not explicitly adjust for mix, contract, network, or regulatory changes.

These extensions remain open for future demos.

