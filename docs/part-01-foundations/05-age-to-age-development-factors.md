---
title: "Age-to-Age Development Factors"
part: "Parte I · Fundamentos"
chapter: 5
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

05-age-to-age-development-factors.md
---
title: Age-to-Age Development Factors
subtitle: Theory, Estimation, Selection and Interpretation of Loss Development Factors
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 05
status: Draft
last_updated: 2026-07-13
---

# Age-to-Age Development Factors

> *"Loss Development Factors are empirical estimators of how claims mature over time."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand why development factors exist.
- Compute age-to-age factors correctly.
- Derive volume-weighted estimators.
- Compare arithmetic, geometric and weighted averages.
- Detect unstable factors.
- Select appropriate LDFs.
- Understand the relationship between LDFs and Ultimate Losses.

---

## Table of Contents

1. Introduction
2. Motivation
3. Definition
4. Individual Link Ratios
5. Aggregate Age-to-Age Factors
6. Estimation Methods
7. Selection of Factors
8. Tail Factors
9. Health Insurance Applications
10. Practical Example
11. Validation
12. Best Practices
13. Summary

---

## 1. Introduction

Claims rarely settle immediately.

Instead,

they develop progressively through time.

If we know how historical claims have developed,

we can estimate

how current claims are expected to develop.

Loss Development Factors (LDFs)

quantify that evolution.

---

## 2. Motivation

Suppose an accident year has accumulated

\$10 million

after twelve months.

Historical experience suggests

that after twenty-four months

similar accident years reached

\$12 million.

Development factor

```
12 / 10 = 1.20
```

Interpretation

Current claims are expected to grow

20%

before reaching ultimate.

---

## 3. Definition

For cumulative triangles,

the individual age-to-age factor is

$$
f_{ij}

=

\frac{C_{i,j+1}}

{C_{ij}}
$$

where

- \(C_{ij}\) = cumulative loss
- \(i\) = accident period
- \(j\) = development period

---

## Example

| Accident |12|24|
|-----------|---|---|
|2022|100|120|

Then

$$
f

=

120/100

=

1.20
$$

---

## Interpretation

A factor of

```
1.20
```

means

Claims have increased

20%

between development

12

and

24

months.

---

## 4. Individual Link Ratios

Example

| Accident |12|24|Factor|
|-----------|---|---|------|
|2020|100|120|1.20|
|2021|200|250|1.25|
|2022|300|345|1.15|

Each row produces

one observation.

---

## 5. Aggregate Development Factor

Multiple observations

must be combined.

This produces the selected LDF.

Several estimators exist.

---

## 6. Arithmetic Mean

The simplest estimator is

$$
\hat f

=

\frac1n

\sum f_i
$$

Advantages

Simple.

Disadvantages

Sensitive to outliers.

---

Example

Factors

```
1.20

1.25

1.15
```

Arithmetic Mean

```
1.20
```

---

## 7. Volume-Weighted Average

This is the standard actuarial estimator.

$$
\hat f

=

\frac

{\sum C_{i,j+1}}

{\sum C_{ij}}
$$

This estimator gives greater weight

to larger accident years.

---

Example

| Accident |12|24|
|-----------|---|---|
|2020|100|120|
|2021|200|250|
|2022|300|345|

Totals

```
715 / 600

=

1.1917
```

---

## Why Volume Weighting?

Large accident years

contain more information.

Therefore,

they receive greater statistical weight.

This is one reason why

volume-weighted averages dominate actuarial practice.

---

## 8. Geometric Mean

Sometimes

growth is multiplicative.

Estimator

$$
\hat f

=

\left(

\prod f_i

\right)^{1/n}
$$

Useful

when factors vary substantially.

---

## 9. Median

Robust against outliers.

Useful

for unstable portfolios.

---

## 10. Trimmed Mean

Extreme observations

are removed.

Example

```
1.10

1.15

1.18

1.20

2.30
```

Remove

2.30

Average remaining values.

---

## 11. Selecting Development Factors

Actuarial judgment

is required.

Selection considers

- credibility
- volatility
- portfolio changes
- inflation
- operational changes
- COVID
- provider contracts

No automatic rule exists.

---

## 12. Tail Factors

Observed development eventually ends.

However,

claims may continue developing.

Tail factors estimate

development beyond the observed triangle.

Example

```
120→Ultimate

1.03
```

Ultimate

```
120 × 1.03

=

123.6
```

---

## 13. Health Insurance Considerations

Development factors are influenced by

- payment cycles
- provider contracts
- retroactive eligibility
- pharmacy reversals
- payment corrections
- encounter processing
- coordination of benefits

Health Insurance

often exhibits

shorter tails

than Property & Casualty.

---

## 14. Practical Example

Cumulative Triangle

| Accident |12|24|36|
|-----------|---|---|---|
|2020|100|120|125|
|2021|200|250|260|
|2022|300|345| |

Individual Factors

12→24

```
1.20

1.25

1.15
```

24→36

```
1.0417

1.0400
```

Selected

12→24

Volume Weighted

```
715

/

600

=

1.1917
```

Selected

24→36

```
385

/

370

=

1.0405
```

---

## 15. Cumulative Development Factors (CDF)

Age-to-age factors

are multiplied.

$$
CDF_j

=

\prod_{k=j}^{n}

f_k
$$

Example

```
12→24

1.1917

24→36

1.0405
```

CDF

```
1.2399
```

Interpretation

Claims currently at

12 months

are expected to increase

23.99%

before ultimate.

---

## 16. Validation

Review

✓ negative factors

✓ factors below one

✓ calendar effects

✓ structural changes

✓ mergers

✓ operational changes

✓ claim reopening

---

## 17. Common Errors

Using incremental triangles.

Using immature accident years.

Ignoring inflation.

Ignoring operational changes.

Blindly averaging factors.

Using factors from another product.

---

## 18. Best Practices

Always inspect

individual link ratios.

Do not rely solely

on automatic averages.

Document

why

each selected factor

was chosen.

Maintain an audit trail.

---

## Key Takeaways

Loss Development Factors summarize historical claim emergence.

Volume-weighted averages are the actuarial standard.

Different estimators answer different statistical questions.

Professional judgment remains essential.

LDF selection is one of the most important actuarial decisions in reserving.

---

## References

- Mack (1993)
- England & Verrall (2002)
- Friedland – Estimating Unpaid Claims
- Wüthrich & Merz (2008)
- Taylor – Loss Reserving
- CAS Study Notes
- ASOP 23
- ASOP 56

---

## Next Chapter

➡️ **06-chain-ladder-method.md**