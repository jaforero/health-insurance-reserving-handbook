---
title: "GAM for Loss Reserving"
part: "Parte IV · Modelos estadísticos"
chapter: 16
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

16-generalized-additive-models-gam.md
---
title: Generalized Additive Models (GAM) for Loss Reserving
subtitle: Nonlinear Statistical Modeling for Modern Health Insurance Reserving
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 16
status: Draft
last_updated: 2026-07-13
---

# Generalized Additive Models (GAM)

> *"Generalized Linear Models assume relationships are linear on the transformed scale. Generalized Additive Models allow the data to determine the shape of those relationships."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand why GAMs extend GLMs.
- Explain smooth functions and penalized splines.
- Model nonlinear development patterns.
- Select smoothing parameters.
- Prevent overfitting.
- Interpret GAM effects.
- Apply GAMs to Health Insurance reserving.
- Compare GAMs with GLMs and classical reserving methods.

---

## Table of Contents

1. Introduction
2. Motivation
3. From GLM to GAM
4. Mathematical Foundations
5. Basis Functions
6. Penalized Splines
7. Smoothing Parameter Selection
8. Model Estimation
9. Diagnostics
10. Practical Example
11. Health Insurance Applications
12. Comparison with GLM
13. Advantages
14. Limitations
15. Best Practices
16. Summary

---

## 1. Introduction

Generalized Linear Models assume

that each predictor contributes linearly on the transformed scale.

In practice,

insurance data rarely behave linearly.

Examples include

- claim development
- medical inflation
- age effects
- provider efficiency
- utilization
- seasonality

Generalized Additive Models (GAMs)

replace linear effects

with smooth functions estimated directly from the data.

---

## 2. Motivation

Suppose development follows

```
Month

↓

Rapid Growth

↓

Plateau

↓

Slow Tail
```

A GLM forces

one coefficient

for each development period.

A GAM estimates

a smooth development curve.

This often produces

more stable predictions.

---

## 3. From GLM to GAM

GLM

$$
g(\mu)=X\beta
$$

GAM

$$
g(\mu)

=

\beta_0

+

\sum_j

f_j(x_j)
$$

where

$$
f_j(\cdot)
$$

are smooth functions estimated from the data.

---

## Interpretation

Instead of estimating

one coefficient

per predictor,

the model estimates

one smooth curve

per predictor.

---

## 4. Why Smooth Functions?

Suppose

Medical Inflation

affects reserves.

True relationship

```
Reserve

▲

│

│      ****

│    **

│  **

│**

└────────────► Inflation
```

GLM

fits

straight lines.

GAM

fits

smooth curves.

---

## 5. Mathematical Formulation

Suppose

Incremental Loss

$$
Y_i
$$

Then

$$
Y_i

\sim

Gamma(\mu_i,\phi)
$$

or

Tweedie.

The model becomes

$$
g(\mu_i)

=

\beta_0

+

f_1(Development)

+

f_2(AccidentYear)

+

f_3(CalendarYear)

+

f_4(Age)

+
...
$$

---

## 6. Basis Functions

Smooth functions are represented as

linear combinations

of basis functions.

Example

$$
f(x)

=

\sum

\beta_k

B_k(x)
$$

where

$$
B_k(x)
$$

may be

- B-Splines
- Cubic Splines
- Thin Plate Splines
- Natural Splines

---

## 7. Penalized Splines

Without restriction,

smooth curves overfit.

Penalty term

$$
\lambda

\int

(f''(x))^2

dx
$$

controls complexity.

Interpretation

Large

$$
\lambda
$$

↓

Smooth curve

Small

$$
\lambda
$$

↓

Flexible curve

---

## 8. Effective Degrees of Freedom (EDF)

Unlike GLMs,

GAMs estimate

Effective Degrees of Freedom

rather than simply

number of coefficients.

Interpretation

EDF

≈1

↓

Almost linear.

EDF

≫1

↓

Highly nonlinear.

---

## 9. Choosing the Smoothing Parameter

Common methods

- Generalized Cross Validation (GCV)
- REML
- ML
- AIC
- UBRE

Modern actuarial software

typically uses

REML.

---

## 10. Model Estimation

Parameter estimation

alternates between

- likelihood maximization
- smoothing optimization

using

Penalized Iteratively Reweighted Least Squares

(P-IRLS).

---

## 11. Practical Example

Suppose

Incremental Claims

depend on

- Development
- Calendar Year
- Inflation

Model

$$
\log(\mu)

=

\beta_0

+

f_1(Development)

+

f_2(CalendarYear)

+

f_3(Inflation)
$$

Estimated EDF

| Variable | EDF |
|-----------|----:|
|Development|5.8|
|Calendar|2.4|
|Inflation|1.1|

Interpretation

Development exhibits

strong nonlinear behavior.

Inflation

is approximately linear.

---

## 12. Health Insurance Example

Medical utilization often follows

```
High

↓

Moderate

↓

Stable
```

rather than

a straight line.

Similarly,

provider reimbursement

may increase

nonlinearly

over time.

GAM captures these relationships naturally.

---

## 13. Python Example

```python
from pygam import GammaGAM, s

gam = GammaGAM(

s(0)+

s(1)+

s(2)

)

gam.fit(X,y)

gam.summary()
```

---

## 14. R Example

```r
library(mgcv)

fit <- gam(

incremental ~

s(development)+

s(calendar_year)+

s(inflation),

family=Gamma(link="log"),

data=df,

method="REML"

)

summary(fit)

plot(fit)
```

---

## 15. Interpretation of Smooth Functions

Unlike GLMs,

coefficients

are not interpreted directly.

Instead,

interpret

- shape
- trend
- turning points
- confidence bands

Plots become essential.

---

## 16. Diagnostics

Review

✓ Residuals

✓ Deviance

✓ EDF

✓ Concurvity

✓ AIC

✓ GCV

✓ QQ Plot

✓ Scale Parameter

---

## 17. Concurvity

GAM analogue

of multicollinearity.

Occurs when

smooth predictors

contain similar information.

High concurvity

reduces interpretability.

---

## 18. Comparison with GLM

| Feature | GLM | GAM |
|----------|-----|-----|
| Linear Effects | ✓ | ✓ |
| Nonlinear Effects | ✘ | ✓ |
| Splines | ✘ | ✓ |
| Smooth Functions | ✘ | ✓ |
| Automatic Curve Estimation | ✘ | ✓ |
| Interpretability | High | Moderate |

---

## 19. Health Insurance Applications

GAM performs particularly well for

- claim development
- seasonality
- provider behavior
- utilization curves
- inflation
- risk adjustment
- enrollment growth
- aging populations

---

## 20. Advantages

✔ Flexible

✔ Captures nonlinear relationships

✔ Excellent predictive performance

✔ Handles complex trends

✔ Automatic smoothing

✔ Interpretable visualization

---

## 21. Limitations

Requires

larger datasets.

Computationally intensive.

Less interpretable

than GLMs.

Sensitive to

smoothing parameter selection.

---

## 22. Production Workflow

```
Raw Claims

↓

Feature Engineering

↓

Train/Test Split

↓

GLM Benchmark

↓

GAM

↓

Residual Analysis

↓

Cross Validation

↓

Reserve Prediction

↓

Governance
```

---

## 23. Comparison with Classical Reserving

| Feature | Chain Ladder | GLM | GAM |
|----------|--------------|-----|-----|
| Development Factors | ✓ | Implicit | Implicit |
| Covariates | ✘ | ✓ | ✓ |
| Nonlinear Effects | ✘ | ✘ | ✓ |
| Statistical Tests | Limited | ✓ | ✓ |
| Smooth Curves | ✘ | ✘ | ✓ |
| Predictive Accuracy | Moderate | High | Very High |

---

## 24. Best Practices

Use

GLM

as baseline.

Fit

GAM

only

if diagnostics indicate

nonlinear relationships.

Avoid

overfitting

through

REML

or

cross-validation.

Compare

predictions

against

GLM

and

Chain Ladder.

Document

all smoothing decisions.

---

## Key Takeaways

Generalized Additive Models extend GLMs by replacing linear effects with smooth functions estimated directly from the data.

This flexibility allows GAMs to model complex nonlinear relationships frequently observed in Health Insurance reserving, such as claim development, inflation, provider behavior and seasonality.

When combined with appropriate diagnostics and regularization,

GAMs provide a powerful balance between predictive performance and statistical interpretability.

---

## References

- Hastie, T. & Tibshirani, R. (1990). *Generalized Additive Models.*
- Wood, S. (2017). *Generalized Additive Models: An Introduction with R.*
- McCullagh, P. & Nelder, J. *Generalized Linear Models.*
- England & Verrall (2002).
- Wüthrich & Merz (2008).
- Taylor, G. *Loss Reserving.*
- ASOP No. 23 – Data Quality.
- ASOP No. 41 – Actuarial Communications.
- ASOP No. 56 – Modeling.

---

## Next Chapter

➡️ **17-bayesian-loss-reserving.md**