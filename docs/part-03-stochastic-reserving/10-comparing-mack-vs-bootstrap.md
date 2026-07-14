---
title: "Comparing Mack vs. Bootstrap"
part: "Parte III · Reserving estocástico"
chapter: 10
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

10–Comparing-Mack-vs-Bootstrap
---
title: Comparing Mack vs Bootstrap Chain Ladder
subtitle: Analytical versus Simulation-Based Estimation of Reserve Uncertainty
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 10
status: Draft
last_updated: 2026-07-13
---

# Comparing Mack vs Bootstrap Chain Ladder

> *"Mack estimates uncertainty analytically. Bootstrap estimates uncertainty empirically through simulation. Both answer the same actuarial question from different statistical perspectives."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand the conceptual differences between Mack and Bootstrap.
- Select the appropriate method for a reserving exercise.
- Compare assumptions.
- Compare outputs.
- Compare computational complexity.
- Explain differences to management and auditors.

---

## Table of Contents

1. Introduction
2. Why Compare Mack and Bootstrap?
3. Conceptual Differences
4. Mathematical Differences
5. Statistical Assumptions
6. Sources of Uncertainty
7. Prediction Intervals
8. Computational Complexity
9. Advantages
10. Limitations
11. Practical Example
12. Health Insurance Applications
13. Decision Framework
14. Best Practices
15. Summary

---

## 1. Introduction

Both Mack Chain Ladder and Bootstrap Chain Ladder attempt to answer the same actuarial question:

> **How uncertain is our reserve estimate?**

The difference lies in *how* they estimate uncertainty.

---

## 2. Deterministic Chain Ladder

Chain Ladder produces

```
One Reserve
```

Example

Reserve

```
150 M
```

No information is provided about

- variability
- confidence intervals
- downside risk

---

## 3. Mack Chain Ladder

Mack computes

```
Reserve

+

Standard Error

+

Prediction Interval
```

using analytical formulas.

No simulation is required.

---

## 4. Bootstrap Chain Ladder

Bootstrap repeatedly reconstructs

thousands of triangles

using simulated residuals.

Typical workflow

```
Observed Triangle

↓

Fit Chain Ladder

↓

Residuals

↓

Resampling

↓

10,000 Simulations

↓

Reserve Distribution
```

Unlike Mack,

Bootstrap estimates the entire distribution.

---

## 5. Philosophical Difference

Mack asks

> "What is the variance implied by this model?"

Bootstrap asks

> "What happens if history had been slightly different?"

One derives uncertainty.

The other simulates it.

---

## 6. Mathematical Comparison

## Mack

Uses

$$
MSEP
=
Process
+
Parameter
$$

Variance is derived analytically.

---

## Bootstrap

Approximates

$$
F(Reserve)
$$

through Monte Carlo simulation.

No closed-form solution is required.

---

## 7. Assumptions

| Assumption | Mack | Bootstrap |
|------------|------|-----------|
| Stable development | ✓ | ✓ |
| Chain Ladder valid | ✓ | ✓ |
| Independent accident years | ✓ | Usually |
| Distribution required | No | No (non-parametric) |
| Simulation required | No | Yes |

---

## 8. Output Comparison

## Mack

Produces

- Reserve
- Standard Error
- MSEP
- CV
- Prediction Interval

---

## Bootstrap

Produces

- Reserve
- Entire distribution
- Quantiles
- VaR
- TVaR
- Percentiles
- Tail probabilities

Bootstrap therefore supports enterprise risk management.

---

## 9. Prediction Intervals

Suppose

Reserve

100

Standard Error

8

---

## Mack

95%

```
100

±

1.96 × 8
```

Produces

```
84.3

115.7
```

assuming approximate normality.

---

## Bootstrap

95%

Obtained directly

from simulated percentiles.

No symmetry is required.

This is particularly useful for skewed reserve distributions.

---

## 10. Process Variance

Both methods estimate

process variance.

Difference

Mack

derives it analytically.

Bootstrap

estimates it empirically.

---

## 11. Parameter Risk

Mack estimates

parameter uncertainty

using asymptotic theory.

Bootstrap estimates

parameter uncertainty

through repeated sampling.

---

## 12. Distribution Shape

Mack

typically assumes

approximate normality

for interval construction.

Bootstrap

allows

- skewness
- heavy tails
- asymmetric distributions

This is a major advantage.

---

## 13. Computational Cost

| Method | Complexity |
|----------|------------|
| Mack | Very Low |
| Bootstrap | High |

Typical runtime

Mack

Seconds

Bootstrap

Minutes

depending on simulations.

---

## 14. Numerical Example

Observed Reserve

```
150
```

---

## Mack

Reserve

150

Standard Error

12

CV

8%

95%

126–174

---

## Bootstrap

Reserve

151

Median

149

P75

158

P95

181

P99

205

Notice

Bootstrap reveals

distribution asymmetry.

---

## 15. Health Insurance Example

Commercial Health

High volume

Low severity

↓

Mack often performs well.

---

Medicaid

Operational changes

↓

Bootstrap preferred.

---

Medicare Advantage

Risk adjustment changes

↓

Bootstrap frequently provides better uncertainty estimates.

---

COVID Period

Large structural shifts

↓

Neither method should be applied without adjustment.

---

## 16. Strengths

## Mack

✔ Fast

✔ Transparent

✔ Easy to explain

✔ Widely accepted

✔ No simulation

---

## Bootstrap

✔ Flexible

✔ Full reserve distribution

✔ Better tail estimation

✔ Supports capital modeling

✔ Supports ORSA

---

## 17. Weaknesses

## Mack

✘ Approximate intervals

✘ Less flexible

✘ Sensitive to assumptions

---

## Bootstrap

✘ Computationally intensive

✘ Requires simulation

✘ More implementation choices

✘ Harder to explain

---

## 18. Decision Matrix

| Situation | Preferred Method |
|------------|-----------------|
| Quarterly reserving | Mack |
| Fast reserve indication | Mack |
| Capital modeling | Bootstrap |
| Solvency analysis | Bootstrap |
| ORSA | Bootstrap |
| Risk appetite | Bootstrap |
| Regulatory review | Both |
| Board reporting | Both |

---

## 19. Recommended Workflow

Modern actuarial practice

should not choose

between Mack

or

Bootstrap.

Instead

use

```
Triangle

↓

Diagnostics

↓

Chain Ladder

↓

Mack

↓

Bootstrap

↓

Compare

↓

Professional Judgment

↓

Final Reserve
```

This workflow provides

both

speed

and

robustness.

---

## 20. Practical Recommendations

Always compare

- Point estimates
- CV
- Prediction intervals
- Tail risk
- Distribution shape

Large differences

deserve investigation.

---

## 21. Common Mistakes

Using Bootstrap

without validating

Chain Ladder assumptions.

Assuming

Bootstrap

automatically improves

poor data.

Reporting

only

point estimates.

Ignoring

prediction uncertainty.

---

## 22. Best Practices

Run

Mack

first.

Run

Bootstrap

second.

Explain

differences.

Document

assumptions.

Retain

both analyses

within

the reserving file.

---

## Key Takeaways

Mack and Bootstrap estimate the same underlying reserve uncertainty using different statistical approaches.

Mack is analytical, transparent and computationally efficient.

Bootstrap is simulation-based, flexible and capable of estimating the complete reserve distribution.

Modern actuarial practice benefits from using both methods together rather than treating them as competing alternatives.

---

## Comparison Summary

| Feature | Mack | Bootstrap |
|---------|------|-----------|
| Point Estimate | ✓ | ✓ |
| Standard Error | ✓ | ✓ |
| Reserve Distribution | ✘ | ✓ |
| VaR | ✘ | ✓ |
| TVaR | ✘ | ✓ |
| Computational Speed | Excellent | Moderate |
| Regulatory Acceptance | Excellent | Excellent |
| Capital Modeling | Limited | Excellent |
| Ease of Explanation | Excellent | Moderate |

---

## References

- Mack (1993)
- Mack (1999)
- England & Verrall (2002)
- Wüthrich & Merz (2008)
- Friedland – Estimating Unpaid Claims Using Basic Techniques
- Taylor – Loss Reserving
- CAS Monograph on Stochastic Loss Reserving
- ASOP No. 23 – Data Quality
- ASOP No. 56 – Modeling

---

## Next Chapter

➡️ **11-bornhuetter-ferguson.md**