---
title: "Cape Cod Method"
part: "Parte II · Métodos clásicos"
chapter: 13
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

13-cape-cod-method.md
---
title: Cape Cod Method
subtitle: Empirical Credibility Reserving Using Exposure-Based Expected Loss Ratios
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 13
status: Draft
last_updated: 2026-07-13
---

# Cape Cod Method

> *"Chain Ladder trusts history. Bornhuetter-Ferguson trusts actuarial expectations. Cape Cod estimates those expectations directly from historical experience."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand the actuarial motivation for the Cape Cod Method.
- Explain how Cape Cod differs from Bornhuetter-Ferguson.
- Estimate the Expected Loss Ratio (ELR) from observed data.
- Calculate Ultimate Losses using Cape Cod.
- Understand the statistical assumptions behind the method.
- Apply Cape Cod to Health Insurance portfolios.
- Compare Cape Cod with Chain Ladder and Bornhuetter-Ferguson.

---

## Table of Contents

1. Introduction
2. Historical Background
3. Why Cape Cod?
4. Conceptual Framework
5. Mathematical Formulation
6. Estimating the ELR
7. Estimating Ultimate Losses
8. Numerical Example
9. Relationship with Other Reserving Methods
10. Health Insurance Applications
11. Implementation
12. Diagnostics
13. Best Practices
14. Summary

---

## 1. Introduction

The Cape Cod Method is one of the most important credibility-based reserving techniques.

Conceptually,

it combines the philosophy of

- Chain Ladder
- Bornhuetter-Ferguson

while removing one important limitation:

the Expected Loss Ratio (ELR)

does **not** need to come from pricing or expert judgment.

Instead,

it is estimated directly from the portfolio.

---

## 2. Historical Background

The method was developed by actuaries at Cape Cod Associates.

Its principal innovation was estimating the expected loss ratio from historical exposure and observed losses rather than treating it as an external assumption.

Today,

Cape Cod is widely used in

- Property & Casualty
- Health Insurance
- Workers Compensation
- Reinsurance

---

## 3. Motivation

Suppose

a company launches

a relatively new product.

Chain Ladder may overreact because little development has emerged.

Bornhuetter-Ferguson requires an externally selected ELR.

Cape Cod instead estimates

the ELR directly from

- exposure,
- reported claims,
- development factors.

This reduces subjectivity.

---

## 4. Conceptual Framework

Cape Cod assumes

Ultimate Loss

=

Exposure

×

Estimated ELR

Unlike BF,

the ELR is estimated

from observed experience.

---

## 5. Inputs Required

Cape Cod requires

- Earned Premium
- Development Factors
- Reported Losses
- Exposure
- Accident Periods

Unlike Chain Ladder,

premium information is essential.

---

## 6. Mathematical Framework

Suppose

for accident year

*i*

Exposure

$$
E_i
$$

Observed Loss

$$
R_i
$$

CDF

$$
F_i
$$

Expected Ultimate

$$
U_i
=
E_i
\times
ELR
$$

---

## 7. Percent Reported

As in Bornhuetter-Ferguson,

the reported proportion is

$$
p_i
=
\frac1{CDF_i}
$$

The expected reported amount is

$$
E_i
\times
ELR
\times
p_i
$$

---

## 8. Estimating the ELR

Cape Cod estimates

the Expected Loss Ratio

using all accident years simultaneously.

The estimator is

$$
\widehat{ELR}
=
\frac
{\sum_i R_i}
{\sum_i E_i p_i}
$$

where

- numerator = reported losses
- denominator = adjusted earned exposure

This is one of the defining equations of the method.

---

## Interpretation

Older accident years

contribute more credibility,

because

their reported percentage

is close to

100%.

Immature years

receive less weight.

---

## 9. Estimating Ultimate Losses

After estimating

$$
\widehat{ELR}
$$

Ultimate losses become

$$
U_i
=
E_i
\times
\widehat{ELR}
$$

---

IBNR is

$$
IBNR_i
=
U_i
(1-p_i)
$$

---

Ultimate estimate

$$
Ultimate_i
=
Reported_i
+
IBNR_i
$$

---

## 10. Numerical Example

Suppose

| Accident | Premium | Reported | CDF |
|-----------|---------|----------|-----|
|2022|100|65|1.25|
|2023|110|50|1.60|
|2024|120|20|2.50|

---

## Step 1

Compute

Percent Reported

| Accident | Reported % |
|-----------|------------|
|2022|80%|
|2023|62.5%|
|2024|40%|

---

## Step 2

Adjusted Exposure

| Accident | Premium × Reported % |
|-----------|---------------------|
|2022|80|
|2023|68.75|
|2024|48|

Total

196.75

---

## Step 3

Observed Losses

65

+

50

+

20

=

135

---

## Step 4

Estimated ELR

$$
135

/

196.75

=

68.6\%
$$

---

## Step 5

Expected Ultimate

| Accident | Ultimate |
|-----------|----------|
|2022|68.6|
|2023|75.5|
|2024|82.3|

---

## Step 6

IBNR

2024

Expected Ultimate

82.3

Reported

20

IBNR

62.3

---

## 11. Statistical Interpretation

Cape Cod estimates

a common Expected Loss Ratio

using

Maximum Likelihood–type reasoning

under the assumption

that

historical reported losses

provide an unbiased estimate

of expected reported losses.

It therefore reduces

dependence on subjective pricing assumptions.

---

## 12. Relationship Among Methods

```
Chain Ladder

↓

Pure historical development

---------------------------

Bornhuetter-Ferguson

↓

External ELR

---------------------------

Cape Cod

↓

Estimated ELR

---------------------------

Benktander

↓

Iterative Credibility
```

---

## 13. Comparison

| Feature | Chain Ladder | BF | Cape Cod |
|----------|--------------|----|----------|
| Uses Premium | ✘ | ✔ | ✔ |
| Uses ELR | ✘ | External | Estimated |
| Credibility | High | Low | Moderate |
| Suitable for Immature Years | Limited | Excellent | Excellent |
| Requires Pricing Assumptions | No | Yes | No |

---

## 14. Health Insurance Applications

Cape Cod is particularly useful when

- premium information is reliable,
- enrollment is stable,
- benefit changes are moderate,
- actuarial pricing assumptions are unavailable.

Examples include

- ACA Individual Markets
- Medicaid Managed Care
- Medicare Advantage
- Employer Group Insurance

---

## 15. Python Example

```python
import pandas as pd

df["reported_pct"] = 1 / df["cdf"]

elr = (
    df["reported"].sum()
    /
    (df["premium"] * df["reported_pct"]).sum()
)

df["ultimate"] = df["premium"] * elr

df["ibnr"] = df["ultimate"] * (1 - df["reported_pct"])
```

---

## 16. R Example

```r
df$reportedPct <- 1 / df$cdf

elr <- sum(df$reported) /
       sum(df$premium * df$reportedPct)

df$ultimate <- df$premium * elr

df$ibnr <- df$ultimate * (1 - df$reportedPct)
```

---

## 17. SQL Example

```sql
SELECT

SUM(reported)

/

SUM(premium * (1.0 / cdf))

AS estimated_elr

FROM reserving;
```

---

## 18. Diagnostics

Before applying Cape Cod

verify

✓ Premium completeness

✓ Exposure consistency

✓ Stable development factors

✓ Homogeneous portfolio

✓ No material pricing changes

✓ No structural breaks

✓ Reasonable CDFs

---

## 19. Common Mistakes

Using written premium instead of earned premium.

Ignoring exposure changes.

Applying one ELR to heterogeneous products.

Ignoring changes in underwriting.

Using outdated development factors.

---

## 20. Advantages

✔ Objective ELR estimation.

✔ Stable for immature accident years.

✔ Less subjective than BF.

✔ Combines pricing and reserving.

✔ Easy to communicate.

✔ Well accepted in actuarial practice.

---

## 21. Limitations

Assumes

- homogeneous expected loss ratios,
- stable exposure,
- consistent pricing.

Not appropriate

if premium adequacy changes materially between accident years.

---

## 22. Practical Decision Framework

| Situation | Preferred Method |
|------------|------------------|
| Mature portfolio | Chain Ladder |
| New product | Bornhuetter-Ferguson |
| Reliable premium data | Cape Cod |
| Stable exposure | Cape Cod |
| Highly volatile pricing | BF |
| Low credibility | Cape Cod |

---

## 23. Best Practices

Estimate reserves using

- Chain Ladder
- Bornhuetter-Ferguson
- Cape Cod

Compare

Ultimate

IBNR

ELR

Prediction consistency

Document

why

the selected method

best reflects the portfolio.

Never rely on a single reserving technique.

---

## Key Takeaways

Cape Cod combines exposure information with historical development to estimate an Expected Loss Ratio directly from observed data.

Compared with Bornhuetter-Ferguson,

it reduces dependence on externally selected pricing assumptions.

Compared with Chain Ladder,

it provides greater stability for immature accident years.

For many Health Insurance portfolios,

Cape Cod offers an excellent compromise between empirical experience and actuarial credibility.

---

## References

- Bühlmann, H. *Credibility Theory.*
- Friedland, J. *Estimating Unpaid Claims Using Basic Techniques.*
- England, P. & Verrall, R. (2002).
- Mack, T. (1993).
- Wüthrich, M. & Merz, M. (2008).
- Taylor, G. *Loss Reserving.*
- CAS Study Notes.
- ASOP No. 5 – Incurred Health and Disability Claims.
- ASOP No. 23 – Data Quality.
- ASOP No. 56 – Modeling.

---

## Next Chapter

➡️ **14-comparison-of-classical-reserving-methods.md**