---
title: "GLM for Loss Reserving"
part: "Parte IV · Modelos estadísticos"
chapter: 15
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

15-generalized-linear-models-for-reserving.md
---
title: Generalized Linear Models (GLM) for Loss Reserving
subtitle: Statistical Modeling of Incremental Claims Development
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 15
status: Draft
last_updated: 2026-07-13
---

# Generalized Linear Models (GLM) for Loss Reserving

> *"Classical reserving methods extrapolate historical patterns. Generalized Linear Models explain why those patterns occur."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand why GLMs represent a major advancement over traditional reserving methods.
- Derive the GLM formulation for claims reserving.
- Model incremental claims using exponential family distributions.
- Select appropriate link functions.
- Estimate model parameters using Maximum Likelihood Estimation (MLE).
- Evaluate model fit using statistical diagnostics.
- Apply GLMs to Health Insurance reserving.
- Compare GLMs with Chain Ladder and credibility methods.

---

## Table of Contents

1. Introduction
2. Why Move Beyond Chain Ladder?
3. Statistical Foundations
4. The Exponential Family
5. Components of a GLM
6. The Reserving Model
7. Choice of Distribution
8. Link Functions
9. Parameter Estimation
10. Model Diagnostics
11. Practical Example
12. Health Insurance Applications
13. Advantages and Limitations
14. Best Practices
15. Summary

---

## 1. Introduction

Traditional reserving techniques rely almost exclusively on historical development factors.

Generalized Linear Models (GLMs) provide a statistical framework capable of modeling claim development while simultaneously incorporating explanatory variables.

Rather than asking

> "How did claims develop historically?"

GLMs ask

> "Which factors explain claim development?"

This represents a fundamental shift from empirical extrapolation toward statistical inference.

---

## 2. Why Move Beyond Chain Ladder?

Chain Ladder assumes

- stable development,
- homogeneous portfolios,
- proportional growth.

However, modern Health Insurance portfolios often exhibit

- provider mix changes,
- inflation,
- benefit redesign,
- geographic heterogeneity,
- regulatory changes,
- coding changes,
- enrollment growth.

These factors cannot be modeled directly using deterministic methods.

GLMs can incorporate them explicitly.

---

## 3. Statistical Foundations

A GLM extends ordinary linear regression by allowing:

- Non-normal response distributions.
- Non-linear relationships between predictors and the mean.
- Variance structures consistent with insurance data.

The framework consists of three components:

1. Random Component
2. Systematic Component
3. Link Function

---

## 4. The Exponential Family

A response variable \(Y\) belongs to the exponential family if its density can be written as

$$
f(y;\theta,\phi)
=
\exp\left(
\frac{y\theta-b(\theta)}{a(\phi)}
+c(y,\phi)
\right)
$$

where

- \(\theta\) = canonical parameter,
- \(\phi\) = dispersion parameter.

Common reserving distributions include:

| Distribution | Typical Use |
|--------------|-------------|
| Poisson | Claim Counts |
| Gamma | Severity |
| Inverse Gaussian | Heavy-tailed Severity |
| Tweedie | Aggregate Losses |
| Negative Binomial | Overdispersed Counts |

---

## 5. Random Component

Suppose

$$
Y_{ij}
$$

represents incremental paid losses.

Assume

$$
Y_{ij}
\sim
Gamma(\mu_{ij},\phi)
$$

or

$$
Y_{ij}
\sim
Tweedie(\mu_{ij},\phi,p)
$$

depending on portfolio characteristics.

---

## 6. Systematic Component

The expected claim amount is modeled as

$$
\eta_{ij}
=
X_{ij}\beta
$$

where

- \(X\) = design matrix,
- \(\beta\) = parameter vector.

Potential predictors include

- Accident Year
- Development Period
- Calendar Year
- Line of Business
- Region
- Provider Type
- Product
- Inflation Index

---

## 7. Link Function

The link function connects the expected value

$$
\mu
=
E(Y)
$$

with the linear predictor.

General form

$$
g(\mu)=X\beta
$$

Common choices

| Link | Formula |
|-------|----------|
| Identity | \(g(\mu)=\mu\) |
| Log | \(g(\mu)=\log(\mu)\) |
| Logit | \(g(\mu)=\log(\mu/(1-\mu))\) |

The log link is most common in reserving because claim amounts are strictly positive.

---

## 8. Reserving GLM

One common specification is

$$
\log(\mu_{ij})
=
\alpha_i
+
\beta_j
$$

where

- \(\alpha_i\) represents Accident Year effects.
- \(\beta_j\) represents Development Period effects.

Extensions include

$$
\log(\mu_{ij})
=
\alpha_i
+
\beta_j
+
\gamma_k
+
\delta X
$$

where

- \(\gamma_k\) = Calendar effects,
- \(X\) = additional covariates.

---

## 9. Maximum Likelihood Estimation

Parameters are estimated by maximizing

$$
L(\beta)
=
\prod_i
f(y_i|\beta)
$$

or equivalently

$$
\ell(\beta)
=
\sum_i
\log
f(y_i|\beta)
$$

Numerical optimization methods include

- Newton-Raphson,
- Fisher Scoring,
- Iteratively Reweighted Least Squares (IRLS).

---

## 10. Model Diagnostics

A fitted GLM should always be evaluated using:

### Residual Analysis

- Pearson Residuals
- Deviance Residuals
- Anscombe Residuals

### Goodness-of-Fit

- Deviance
- AIC
- BIC
- Log-Likelihood

### Predictive Performance

- RMSE
- MAE
- MAPE

---

## 11. Practical Example

Suppose the following incremental payments:

| AY | Dev | Incremental |
|----|-----|-------------|
|2022|12|120|
|2022|24|45|
|2023|12|150|
|2023|24|60|

Model

$$
\log(\mu)
=
\beta_0
+
\beta_{AY}
+
\beta_{Dev}
$$

Estimated coefficients

| Parameter | Estimate |
|------------|---------:|
|Intercept|4.52|
|AY2023|0.18|
|Dev24|-0.94|

Interpretation:

- AY2023 has approximately \(e^{0.18}-1 \approx 19.7\%\) higher expected incremental losses than AY2022, all else equal.
- Development month 24 has substantially lower expected incremental losses than development month 12.

---

## 12. Python Example

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

model = smf.glm(
    formula="incremental ~ C(accident_year) + C(development)",
    data=df,
    family=sm.families.Gamma(
        link=sm.families.links.Log()
    )
)

results = model.fit()

print(results.summary())
```

---

## 13. R Example

```r
glm_fit <- glm(

incremental ~

factor(accident_year)+

factor(development),

family=Gamma(link="log"),

data=df

)

summary(glm_fit)
```

---

## 14. SQL Preparation

Although model estimation typically occurs in R or Python,

SQL is frequently used to prepare the design matrix.

```sql
SELECT

accident_year,

development,

calendar_year,

product,

provider,

SUM(incremental_paid) AS incremental

FROM claims

GROUP BY

accident_year,

development,

calendar_year,

product,

provider;
```

---

## 15. Health Insurance Applications

GLMs are particularly effective for modeling:

- Medical claims.
- Pharmacy claims.
- Provider-specific development.
- Geographic variation.
- Benefit design changes.
- Inflation adjustments.
- Risk adjustment effects.
- Medicare Advantage.
- Medicaid Managed Care.

Unlike deterministic methods,

GLMs allow explicit adjustment for operational and business drivers.

---

## 16. Comparison with Classical Methods

| Feature | Chain Ladder | GLM |
|----------|--------------|-----|
| Historical Development | ✓ | ✓ |
| Covariates | ✘ | ✓ |
| Statistical Inference | Limited | ✓ |
| Confidence Intervals | Limited | ✓ |
| Hypothesis Testing | ✘ | ✓ |
| Model Selection | ✘ | ✓ |
| Calendar Effects | Limited | ✓ |

---

## 17. Advantages

- Flexible.
- Statistically rigorous.
- Handles multiple explanatory variables.
- Easily extended.
- Suitable for predictive analytics.
- Integrates with modern machine learning workflows.

---

## 18. Limitations

- Greater computational complexity.
- Requires statistical expertise.
- Sensitive to model specification.
- Requires sufficient data volume.
- Interpretation becomes more difficult as model complexity increases.

---

## 19. Best Practices

- Begin with exploratory data analysis.
- Validate triangle construction.
- Compare several distributions.
- Evaluate alternative link functions.
- Check residual diagnostics.
- Assess overdispersion.
- Compare with Chain Ladder.
- Document model assumptions and selection criteria.
- Perform out-of-sample validation.

---

## 20. Key Takeaways

Generalized Linear Models extend classical reserving by modeling incremental claims as realizations from an exponential family distribution.

Unlike Chain Ladder,

GLMs incorporate explanatory variables, allow formal statistical inference, and provide a unified framework for testing hypotheses, estimating uncertainty, and improving predictive accuracy.

For modern Health Insurance reserving,

GLMs represent the natural transition from deterministic actuarial methods to statistical and predictive modeling.

---

## References

- McCullagh, P. & Nelder, J. A. (1989). *Generalized Linear Models.*
- England, P. & Verrall, R. (2002). *Stochastic Claims Reserving in General Insurance.*
- Wüthrich, M. & Merz, M. (2008). *Stochastic Claims Reserving Methods in Insurance.*
- Taylor, G. *Loss Reserving.*
- Friedland, J. *Estimating Unpaid Claims Using Basic Techniques.*
- ASOP No. 5 – Incurred Health and Disability Claims.
- ASOP No. 23 – Data Quality.
- ASOP No. 41 – Actuarial Communications.
- ASOP No. 56 – Modeling.

---

## Next Chapter

➡️ **16-generalized-additive-models-gam.md**