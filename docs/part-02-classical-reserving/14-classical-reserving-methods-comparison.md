---
title: "Classical Reserving Methods Comparison"
part: "Parte II · Métodos clásicos"
chapter: 14
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

14-comparison-of-classical-reserving-methods.md
---
title: Comparison of Classical Reserving Methods
subtitle: A Comprehensive Framework for Selecting Deterministic Reserving Methodologies
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 14
status: Draft
last_updated: 2026-07-13
---

# Comparison of Classical Reserving Methods

> *"No reserving method is universally superior. The appropriate method depends on portfolio maturity, data credibility, business context, and actuarial objectives."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Compare all major deterministic reserving methods.
- Understand the assumptions behind each methodology.
- Identify strengths and weaknesses.
- Select the most appropriate reserving method.
- Understand the maturity continuum.
- Build a practical actuarial decision framework.

---

## Table of Contents

1. Introduction
2. The Reserving Continuum
3. Method Overview
4. Mathematical Comparison
5. Data Requirements
6. Sensitivity Analysis
7. Credibility Framework
8. Decision Matrix
9. Health Insurance Applications
10. Case Study
11. Practical Workflow
12. Best Practices
13. Summary

---

## 1. Introduction

The actuarial literature presents several deterministic reserving methods.

Although they appear different,

they are closely related.

Each method answers the same fundamental question:

> **What is the ultimate cost of claims that have already occurred?**

The difference lies in

how much confidence is assigned to

- historical development,
- prior expectations,
- exposure,
- actuarial judgment.

---

## 2. The Reserving Continuum

The methods can be arranged according to increasing reliance on observed experience.

```text
Expected Loss

↓

Bornhuetter-Ferguson

↓

Benktander

↓

Cape Cod

↓

Chain Ladder

↓

Observed Development
```

This continuum represents increasing credibility assigned to observed claims.

---

## 3. Comparison Philosophy

The methods differ in how they answer one question:

**How should future development be estimated?**

| Method | Uses Historical Development | Uses Prior Information |
|----------|----------------------------|------------------------|
| Chain Ladder | ✓ | ✘ |
| Bornhuetter-Ferguson | Partial | ✓ |
| Benktander | Partial | ✓ |
| Cape Cod | Partial | Estimated |
| Mack | ✓ | ✘ |
| Bootstrap | ✓ | ✘ |

---

## 4. Chain Ladder

## Principle

Historical development fully predicts future development.

Ultimate

$$
Ultimate

=

Reported

×

CDF
$$

---

## Strengths

- Very simple.
- Transparent.
- Easy to audit.
- Fast.
- Standard industry benchmark.

---

## Weaknesses

- Sensitive to immature years.
- Sensitive to operational changes.
- Assumes stable development.

---

## 5. Bornhuetter-Ferguson

## Principle

Future development depends on expected ultimate losses rather than observed emergence.

Ultimate

$$
Ultimate

=

Reported

+

ExpectedUltimate

×

PercentUnreported
$$

---

## Strengths

- Stable.
- Suitable for immature portfolios.
- Incorporates pricing assumptions.

---

## Weaknesses

- Depends heavily on ELR quality.
- Sensitive to pricing assumptions.

---

## 6. Benktander

## Principle

Iteratively increases credibility assigned to observed claims.

Bornhuetter-Ferguson

↓

Iteration

↓

Chain Ladder

---

## Strengths

- Flexible.
- Credibility-based.
- Smooth transition.
- Stable.

---

## Weaknesses

- Requires Expected Ultimate.
- Iteration choice is subjective.

---

## 7. Cape Cod

## Principle

Estimate Expected Loss Ratio directly from portfolio experience.

Ultimate

=

Premium

×

Estimated ELR

---

## Strengths

- Objective ELR.
- Less subjective.
- Uses exposure.

---

## Weaknesses

- Requires reliable premium.
- Assumes stable pricing.

---

## 8. Mack

## Principle

Quantifies reserve uncertainty analytically.

Produces

- Standard Error
- MSEP
- CV
- Prediction Interval

---

## 9. Bootstrap

## Principle

Quantifies reserve uncertainty by simulation.

Produces

- Full reserve distribution
- VaR
- TVaR
- Percentiles

---

## 10. Mathematical Comparison

| Feature | CL | BF | Benktander | Cape Cod |
|-----------|----|----|------------|-----------|
| Uses Reported Claims | ✓ | ✓ | ✓ | ✓ |
| Uses Premium | ✘ | ✓ | ✓ | ✓ |
| Uses ELR | ✘ | External | External | Estimated |
| Uses Development Factors | ✓ | ✓ | ✓ | ✓ |
| Uses Credibility | Implicit | Explicit | Iterative | Exposure-based |

---

## 11. Required Inputs

| Input | CL | BF | Benktander | Cape Cod |
|--------|----|----|------------|----------|
| Triangle | ✓ | ✓ | ✓ | ✓ |
| Premium | ✘ | ✓ | ✓ | ✓ |
| ELR | ✘ | ✓ | ✓ | Estimated |
| Exposure | ✘ | Optional | Optional | ✓ |

---

## 12. Portfolio Maturity

```text
Immature ---------------- Mature

BF ---- Benktander ---- Cape Cod ---- Chain Ladder
```

---

## Interpretation

Immature portfolios

↓

Prior information dominates.

---

Mature portfolios

↓

Observed experience dominates.

---

## 13. Sensitivity to Data Quality

| Method | Sensitivity |
|----------|------------|
| Chain Ladder | High |
| BF | Moderate |
| Benktander | Moderate |
| Cape Cod | Moderate |
| Mack | High |
| Bootstrap | High |

---

## 14. Sensitivity to ELR

| Method | Depends on ELR |
|----------|---------------|
| Chain Ladder | No |
| BF | Very High |
| Benktander | High |
| Cape Cod | Low |

---

## 15. Sensitivity to Development Factors

| Method | Depends on LDF |
|----------|---------------|
| Chain Ladder | Very High |
| BF | Moderate |
| Benktander | Moderate |
| Cape Cod | Moderate |

---

## 16. Statistical Perspective

| Method | Statistical Interpretation |
|----------|---------------------------|
| Chain Ladder | Historical estimator |
| BF | Credibility estimator |
| Benktander | Iterative credibility |
| Cape Cod | Empirical credibility |
| Mack | Analytical uncertainty |
| Bootstrap | Simulation uncertainty |

---

## 17. Health Insurance Considerations

Health Insurance introduces

- enrollment growth
- provider contracts
- pharmacy claims
- retro eligibility
- encounter submissions
- seasonality
- benefit redesign

These factors affect the choice of reserving methodology.

---

## Medicare Advantage

Recommended

- BF
- Cape Cod
- Mack

---

## Medicaid

Recommended

- Cape Cod
- Benktander

---

## ACA Individual Market

Recommended

- BF
- Cape Cod

---

## Mature Commercial Portfolio

Recommended

- Chain Ladder
- Mack
- Bootstrap

---

## 18. Case Study

Suppose

Observed

100

Premium

150

ELR

70%

CDF

1.40

---

Chain Ladder

Ultimate

140

---

Bornhuetter-Ferguson

Ultimate

130

---

Benktander

Ultimate

135

---

Cape Cod

Ultimate

132

---

The four estimates differ because

they assign credibility differently.

---

## 19. Decision Tree

```text
Portfolio Mature?

│

├── YES

│      │

│      ├── Stable?

│      │      │

│      │      ├── YES → Chain Ladder

│      │      └── NO → Mack

│      │

│      └── High Capital Requirements?

│              │

│              └── Bootstrap

│

└── NO

       │

       ├── Reliable ELR?

       │

       ├── YES → BF

       │

       └── NO

              │

              ├── Reliable Premium?

              │

              ├── YES → Cape Cod

              │

              └── Benktander
```

---

## 20. Practical Reserving Workflow

Modern actuarial practice rarely relies on one method.

Recommended workflow

```text
Data Validation

↓

Triangle Construction

↓

Chain Ladder

↓

Bornhuetter-Ferguson

↓

Benktander

↓

Cape Cod

↓

Mack

↓

Bootstrap

↓

Compare Results

↓

Professional Judgment

↓

Final Reserve
```

---

## 21. Common Mistakes

Using only one reserving method.

Ignoring pricing changes.

Ignoring operational changes.

Applying Chain Ladder to immature years.

Using outdated ELRs.

Ignoring diagnostics.

Confusing precision with accuracy.

---

## 22. Best Practices

Always

- compare multiple methods,
- reconcile differences,
- investigate material deviations,
- document assumptions,
- explain method selection,
- perform sensitivity analysis,
- quantify uncertainty.

Professional judgment should always accompany quantitative analysis.

---

## 23. Summary Comparison

| Characteristic | CL | BF | Benktander | Cape Cod | Mack | Bootstrap |
|---------------|----|----|------------|----------|------|-----------|
| Deterministic | ✓ | ✓ | ✓ | ✓ | ✘ | ✘ |
| Stochastic | ✘ | ✘ | ✘ | ✘ | ✓ | ✓ |
| Uses Prior | ✘ | ✓ | ✓ | Estimated | ✘ | ✘ |
| Uses Simulation | ✘ | ✘ | ✘ | ✘ | ✘ | ✓ |
| Produces Distribution | ✘ | ✘ | ✘ | ✘ | Approximate | ✓ |
| Best for Immature Years | ✘ | ✓ | ✓ | ✓ | ✘ | Depends |
| Best for Mature Years | ✓ | Moderate | Moderate | Moderate | ✓ | ✓ |

---

## Key Takeaways

No reserving method is universally optimal.

Method selection depends on

- portfolio maturity,
- credibility,
- pricing information,
- operational stability,
- business objectives.

Modern actuarial practice uses multiple methods,

compares their results,

and relies on professional judgment to determine the final reserve.

---

## References

- Mack, T. (1993, 1999).
- England, P. & Verrall, R. (2002).
- Friedland, J. *Estimating Unpaid Claims Using Basic Techniques.*
- Wüthrich, M. & Merz, M. (2008).
- Taylor, G. *Loss Reserving.*
- CAS Monograph on Stochastic Loss Reserving.
- ASOP No. 5 – Incurred Health and Disability Claims.
- ASOP No. 23 – Data Quality.
- ASOP No. 41 – Actuarial Communications.
- ASOP No. 56 – Modeling.

---

## Next Chapter

➡️ **15-generalized-linear-models-for-reserving.md**