---
title: "Chain Ladder Diagnostics"
part: "Parte II · Métodos clásicos"
chapter: 7
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

07-chain-ladder-diagnostics-and-assumption-testing.md
---
title: Chain Ladder Diagnostics and Assumption Testing
subtitle: Validating Development Patterns Before Reserving
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 07
status: Draft
last_updated: 2026-07-13
---

# Chain Ladder Diagnostics and Assumption Testing

> *"The largest reserving errors rarely come from mathematics. They come from using the wrong triangle."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand every assumption behind Chain Ladder.
- Diagnose unstable development factors.
- Detect structural breaks.
- Identify calendar effects.
- Detect operational changes.
- Validate triangle maturity.
- Decide whether Chain Ladder is appropriate.

---

## Table of Contents

1. Why Diagnostics Matter
2. Assumptions of Chain Ladder
3. Stability of Development Factors
4. Triangle Maturity
5. Calendar Effects
6. Operational Changes
7. Inflation Effects
8. Outlier Detection
9. Residual Diagnostics
10. Sensitivity Analysis
11. Health Insurance Diagnostics
12. Practical Validation Workflow
13. Best Practices
14. Summary

---

## 1. Why Diagnostics Matter

Chain Ladder assumes that historical development predicts future development.

If this assumption fails,

every projection becomes biased.

Therefore,

diagnostics should always precede estimation.

---

## 2. Chain Ladder Assumptions

The method relies on several assumptions:

## Stable development

Historical development patterns remain valid.

---

## Independent accident periods

One accident year does not influence another.

---

## Homogeneous portfolio

The underlying risk characteristics remain comparable.

---

## Consistent claims handling

Operational processes remain stable.

---

## No structural changes

Examples include:

- legislation
- reimbursement rules
- benefit redesign
- provider contracts
- adjudication systems

---

## 3. Stability of Link Ratios

The first diagnostic is the historical evolution of age-to-age factors.

Example

| Accident Year | 12→24 |
|--------------|--------|
|2019|1.18|
|2020|1.19|
|2021|1.21|
|2022|1.20|
|2023|1.82|

Clearly,

2023 deserves investigation.

---

## Coefficient of Variation

Measure

$$
CV=\frac{\sigma}{\mu}
$$

Low CV indicates stable development.

High CV suggests unreliable LDFs.

---

## Range Analysis

Review

Minimum

Maximum

Median

Interquartile Range

Large dispersion indicates instability.

---

## 4. Triangle Maturity

Recent accident periods contain less information.

Example

| Accident | Maximum Development |
|----------|---------------------|
|2020|48|
|2021|36|
|2022|24|
|2023|12|
|2024|6|

Immature years rely heavily on assumptions.

---

## Maturity Ratio

For accident year \(i\),

$$
M_i=\frac{\text{Observed Development}}
{\text{Maximum Development}}
$$

Interpretation

| Ratio | Interpretation |
|--------|----------------|
| > 90% | Mature |
| 60–90% | Moderately mature |
| < 60% | Immature |

---

## 5. Calendar Effects

Development should depend on development age,

not calendar year.

However,

calendar effects arise from

- inflation
- pandemics
- payment delays
- operational changes
- regulation

Visualize the triangle diagonally.

Diagonal trends often indicate calendar effects.

---

Example

```text
Accident →

2020 120 140 150

2021 115 138

2022 110

↓

Calendar diagonals
```

Unexpected diagonal increases require investigation.

---

## 6. Operational Changes

Operational events frequently alter development.

Examples

- new claims system
- outsourcing
- provider payment redesign
- adjudication automation
- staffing changes

These changes can invalidate historical LDFs.

---

## 7. Inflation Effects

Medical inflation affects

calendar time,

not development time.

Failure to adjust inflation

biases Chain Ladder.

Review

- unit cost inflation
- utilization
- coding intensity

separately.

---

## 8. Outlier Detection

Outliers may arise from

- catastrophic claims
- data errors
- mergers
- accounting corrections

Methods

- Boxplots
- Z-scores
- Robust MAD
- Influence analysis

Do not remove outliers automatically.

Always investigate.

---

## 9. Link Ratio Heatmap

A useful visualization

| AY |12→24|24→36|36→48|
|----|------|------|------|
|2020|1.18|1.06|1.01|
|2021|1.19|1.05|1.01|
|2022|1.45|1.08| |

Abrupt changes become immediately visible.

---

## 10. Residual Diagnostics

After projecting,

compute

Residual

$$
e_i=
Observed_i-
Predicted_i
$$

Review

- mean
- variance
- autocorrelation
- trend

Residuals should not exhibit systematic structure.

---

## 11. Sensitivity Analysis

Evaluate

- removing one accident year
- removing one development period
- excluding large claims
- excluding COVID years

Stable models should not change dramatically.

---

## Leave-One-Year-Out Analysis

Procedure

Repeat Chain Ladder

excluding

each accident year.

Large changes indicate instability.

---

## 12. Health Insurance Diagnostics

Health insurance requires additional review.

Examples

Provider payment delays

↓

Artificial development

---

Retroactive eligibility

↓

Claim reopening

---

Pharmacy reversals

↓

Negative incremental values

---

Benefit redesign

↓

Structural break

---

Coding changes

↓

Artificial morbidity shifts

---

## 13. Diagnostic Dashboard

A production model should include

✓ Link Ratio Stability

✓ Triangle Completeness

✓ Calendar Heatmap

✓ Development Curves

✓ Inflation Monitoring

✓ Large Claim Monitoring

✓ Operational Events Timeline

✓ Portfolio Mix Changes

---

## 14. Validation Checklist

Before approving Chain Ladder

□ Triangle reconciled

□ Stable LDFs

□ No structural breaks

□ Calendar effects reviewed

□ Inflation assessed

□ Outliers investigated

□ Maturity adequate

□ Residuals reviewed

□ Assumptions documented

---

## 15. Python Example

```python
import seaborn as sns

sns.heatmap(ldf_matrix,
            annot=True,
            cmap="viridis")
```

---

Coefficient of Variation

```python
cv = ldf.std() / ldf.mean()
```

---

## 16. R Example

```r
boxplot(ldf)

heatmap(as.matrix(ldf))
```

---

## 17. SQL Example

Compute average LDF

```sql
SELECT

development,

AVG(link_ratio),

STDDEV(link_ratio)

FROM ldf

GROUP BY development;
```

---

## 18. Best Practices

Never estimate reserves

before validating

the triangle.

Document

every adjustment.

Maintain

a diagnostics report

for every reserving cycle.

Diagnostics should be reproducible.

---

## Common Pitfalls

- Ignoring calendar effects.
- Averaging unstable link ratios.
- Including immature accident years without justification.
- Failing to document operational changes.
- Assuming Chain Ladder is always appropriate.

---

## Key Takeaways

Chain Ladder is only as reliable as the assumptions supporting it.

Diagnostics are not optional.

Stable development,

credible data,

and documented assumptions

are prerequisites for actuarial reserving.

---

## References

- Mack (1993)
- England & Verrall (2002)
- Friedland – Estimating Unpaid Claims Using Basic Techniques
- Wüthrich & Merz (2008)
- Taylor – Loss Reserving
- ASOP No. 23 – Data Quality
- ASOP No. 41 – Actuarial Communications
- ASOP No. 56 – Modeling

---

## Next Chapter

➡️ **08-mack-chain-ladder.md**