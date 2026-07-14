---
title: IBNR and Health Insurance Reserving
subtitle: Foundations, Methodologies and Practical Implementation
author: Health Reserving Handbook Project
version: 1.0
status: Draft
last_updated: 2026-07-13
part: "Parte I · Fundamentos"
chapter: 1
language: "es"
---

# IBNR and Health Insurance Reserving

> "All reserving methods are approximations of an unknown stochastic process.
The purpose of actuarial reserving is not to predict the future perfectly, but
to quantify uncertainty using the best available information."

---

## Table of Contents

1. Introduction
2. What is Reserving?
3. What is IBNR?
4. Components of Total Reserves
5. Reserving Process
6. Mathematical Framework
7. Data Requirements
8. Development Triangles
9. Classical Methods
10. Stochastic Methods
11. Modern Reserving
12. Validation
13. Model Governance
14. Practical Recommendations
15. References

---

## 1 Introduction

Loss reserving is one of the core actuarial functions in every insurance company.

Its objective is to estimate the future financial obligation arising from insured events that have already occurred but whose ultimate cost is not yet fully known.

Unlike pricing, reserving concerns **past exposure** rather than future exposure.

The reserving process combines:

- actuarial science
- probability theory
- statistics
- financial reporting
- business judgment

---

## 2 What is IBNR?

IBNR stands for

**Incurred But Not Reported**

IBNR represents the expected cost associated with claims that have already occurred but have not yet been reported or completely recognized by the insurer.

Mathematically,

$$
IBNR = Ultimate - Reported
$$

where

- Ultimate = expected ultimate claim cost
- Reported = observed claims

---

## 3 Components of Total Reserves

The actuarial reserve can be decomposed as

$$
Reserve =
RBNS
+
IBNR
+
IBNER
+
ALAE
+
ULAE
$$

where

| Component | Description |
|------------|-------------|
| RBNS | Reported but Not Settled |
| IBNR | Incurred but Not Reported |
| IBNER | Incurred But Not Enough Reported |
| ALAE | Allocated Loss Adjustment Expenses |
| ULAE | Unallocated Loss Adjustment Expenses |

---

## 4 Reserving Process

```mermaid
flowchart LR

A[Raw Claims]

B[Data Validation]

C[Triangle Construction]

D[Development Factors]

E[Ultimate Estimation]

F[Reserve Estimation]

G[Financial Reporting]

A --> B

B --> C

C --> D

D --> E

E --> F

F --> G
```

---

## 5 Mathematical Framework

Let

$$
C_{ij}
$$

be the cumulative paid amount

where

- i = accident period

- j = development period

The observed triangle is

$$
\mathcal T =
\{
C_{ij}
:
i+j\le n
\}
$$

The prediction target is

$$
C_{i,n}
$$

for every incomplete accident period.

---

## 6 Incremental versus Cumulative Triangles

Incremental

$$
X_{ij}
$$

Cumulative

$$
C_{ij}
=
\sum_{k=0}^{j}
X_{ik}
$$

The transformation is invertible.

---

## 7 Sources of Uncertainty

Two independent sources exist.

## Process Risk

Random claim emergence.

## Parameter Risk

Estimated development factors.

Modern reserving quantifies both.

---

## 8 Data Required

Typical variables include

| Variable | Required |
|-----------|----------|
| Claim ID | ✓ |
| Accident Date | ✓ |
| Service Date | ✓ |
| Report Date | ✓ |
| Paid Date | ✓ |
| Payment Amount | ✓ |
| Case Reserve | ✓ |
| Product | ✓ |
| State | Optional |
| Provider | Optional |
| Diagnosis | Optional |

---

## 9 Triangle Construction

The development lag is

$$
Lag =
PaymentDate
-
AccidentDate
$$

expressed in months.

Incremental payments are aggregated by

- Accident Month
- Development Month

---

## 10 Classical Reserving Methods

The classical actuarial methods include

- Chain Ladder
- Bornhuetter-Ferguson
- Cape Cod
- Benktander
- Munich Chain Ladder
- Berquist Sherman

Each method will be covered in subsequent chapters.

---

## 11 Stochastic Methods

Modern actuarial reserving extends deterministic methods by introducing probability distributions.

Examples include

- Mack
- Bootstrap
- Bayesian Reserving
- GLM
- GAM

---

## 12 Health Insurance Considerations

Health insurance differs from P&C because of

- short development tails
- provider contracts
- seasonality
- medical inflation
- completion factors
- benefit changes
- coding effects

Traditional Chain Ladder frequently requires adjustments.

---

## 13 Validation

Every reserving exercise should include

- Backtesting
- Residual analysis
- Calendar effect analysis
- Sensitivity testing
- Scenario testing

---

## 14 Model Governance

A production reserving model should include

- version control
- peer review
- documentation
- reproducibility
- automated testing

---

## 15 Relationship with Other Chapters

This chapter provides the conceptual framework for

- Triangle Construction
- Chain Ladder
- Mack
- Bootstrap
- GLM
- Bayesian Reserving
- Health Insurance Applications

---

## Key Takeaways

- Reserving is fundamentally a stochastic estimation problem.
- IBNR is only one component of total reserves.
- Development triangles summarize historical claim emergence.
- Modern actuarial practice combines deterministic methods with stochastic validation.
- Professional judgment remains essential.

---

## Suggested Reading

- Mack (1993)
- England & Verrall (2002)
- Wüthrich & Merz (2008)
- Friedland (CAS)
- ASOP 5
- ASOP 23
- ASOP 41
- ASOP 56

---

## Exercises

1. Construct a paid triangle from claim-level data.

2. Convert incremental to cumulative.

3. Compute age-to-age factors.

4. Estimate ultimate losses.

5. Compute IBNR.

---

## Next Chapter

➡️ 02-triangle-construction.md