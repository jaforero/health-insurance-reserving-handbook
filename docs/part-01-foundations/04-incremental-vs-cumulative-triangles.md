---
title: Incremental vs Cumulative Triangles
subtitle: Algebra, Properties and Transformations of Loss Development Triangles
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 04
status: Draft
last_updated: 2026-07-13
part: "Parte I · Fundamentos"
language: "es"
---

# Incremental vs Cumulative Triangles

> *"Incremental and cumulative triangles are not different datasets. They are two mathematical representations of exactly the same information."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand the mathematical relationship between incremental and cumulative triangles.
- Transform one representation into the other.
- Prove that the transformation is invertible.
- Understand why different reserving methods prefer different representations.
- Evaluate numerical stability.
- Select the appropriate representation for production models.

---

## Table of Contents

1. Introduction
2. Two Representations of the Same Process
3. Incremental Triangle
4. Cumulative Triangle
5. Transformation Operators
6. Matrix Representation
7. Mathematical Properties
8. Information Preservation
9. Practical Comparison
10. Health Insurance Considerations
11. Numerical Example
12. Computational Implementation
13. Validation
14. Best Practices
15. Summary

---

## 1. Introduction

Loss development is a stochastic process.

There are two equivalent ways to observe that process:

- Incremental payments
- Cumulative payments

Neither representation is "better."

Each serves a different actuarial purpose.

---

## 2. The Underlying Process

Suppose

$$
X_{ij}
$$

represents the payment made during development period **j**
for accident period **i**.

The collection

$$
\{X_{ij}\}
$$

defines the complete payment process.

Everything else is derived from it.

---

## 3. Incremental Triangle

An incremental triangle stores payments made **only during a single development period**.

Example

| Accident | Dev0 | Dev1 | Dev2 | Dev3 |
|----------|------|------|------|------|
| Jan |100|40|20|10|
| Feb |90|30|15| |
| Mar |120|35| | |

Interpretation

The value

```
40
```

means

> Forty monetary units were paid **during development month one**, not before.

---

## Mathematical Definition

Let

$$
X_{ij}\ge0
$$

be the incremental payment.

Each payment belongs to exactly one cell.

Therefore,

$$
X_{ij}
$$

is a partition of total payments.

---

## 4. Cumulative Triangle

The cumulative triangle stores the total amount paid **up to** each development period.

Example

| Accident | Dev0 | Dev1 | Dev2 | Dev3 |
|----------|------|------|------|------|
| Jan |100|140|160|170|
| Feb |90|120|135| |
| Mar |120|155| | |

---

Interpretation

```
160
```

means

Total paid from

Development 0

through

Development 2.

---

## 5. Accumulation Operator

Define the accumulation operator

$$
\mathcal A
$$

such that

$$
C_{ij}

=

\sum_{k=0}^{j}

X_{ik}
$$

where

- X = Incremental
- C = Cumulative

---

## Example

Incremental

| Dev | Payment |
|-----|---------|
|0|100|
|1|40|
|2|20|
|3|10|

Cumulative

| Dev | Payment |
|-----|---------|
|0|100|
|1|140|
|2|160|
|3|170|

---

## 6. Difference Operator

The inverse transformation is

$$
X_{ij}

=

C_{ij}

-

C_{i,j-1}
$$

with

$$
C_{i,-1}=0
$$

This operator is exact.

No information is lost.

---

## Proof of Invertibility

Applying accumulation

followed by differencing

returns the original triangle.

Likewise,

differencing followed by accumulation

also returns the original triangle.

Therefore

the two operators are inverses.

---

## 7. Matrix Representation

Suppose

```
x =
[100,40,20,10]
```

Then

```
c = A x
```

where

```
A=

1 0 0 0

1 1 0 0

1 1 1 0

1 1 1 1
```

Likewise

```
x=D c
```

where

```
D=

1 0 0 0

-1 1 0 0

0 -1 1 0

0 0 -1 1
```

Notice

```
DA=I

AD=I
```

Therefore

both representations contain identical information.

---

## 8. Information Preservation

The transformation

Incremental

↓

Cumulative

is

- deterministic
- exact
- invertible
- lossless

No statistical information disappears.

Only the representation changes.

---

## 9. Statistical Properties

Incremental observations are

approximately independent.

Cumulative observations are

strongly correlated.

Reason

Every cumulative value contains

all previous payments.

Example

```
C2

contains

C1

contains

C0
```

---

## 10. Advantages of Incremental Triangles

✔ Preserve original observations

✔ Better for GLM

✔ Better for GAM

✔ Better for Bayesian models

✔ Better for Machine Learning

✔ Better for frequency/severity decomposition

---

## 11. Advantages of Cumulative Triangles

✔ Simpler visualization

✔ Stable development factors

✔ Chain Ladder

✔ Mack

✔ Bootstrap

✔ Traditional reserving

---

## 12. Numerical Stability

Small errors in cumulative triangles propagate.

Incremental data isolate errors.

Therefore,

modern predictive models

usually start from incremental triangles.

---

## 13. Health Insurance Example

Medical claims frequently contain

- reversals
- adjustments
- corrected bills
- retroactive eligibility

Incremental representation preserves these operational events.

Cumulative representation smooths them.

Both should be retained.

---

## 14. Practical Example

Incremental

| Accident |0|1|2|3|
|-----------|--|--|--|--|
|Jan|100|40|20|10|
|Feb|90|30|15|0|

Apply accumulation

↓

Cumulative

| Accident |0|1|2|3|
|-----------|--|--|--|--|
|Jan|100|140|160|170|
|Feb|90|120|135|135|

Apply differencing

↓

Recover Incremental

Exactly.

---

## 15. Python Example

```python
incremental = triangle.copy()

cumulative = incremental.cumsum(axis=1)

recovered = cumulative.diff(axis=1).fillna(cumulative.iloc[:,0], axis=0)
```

---

## 16. R Example

```r
cumulative <- t(apply(incremental,1,cumsum))

incremental2 <- t(apply(cumulative,1,diff,lag=1))
```

---

## 17. SQL Example

Using window functions

```sql
SUM(paid_amount)

OVER(

PARTITION BY accident_month

ORDER BY development_month

)
```

produces cumulative triangles.

---

## 18. Validation Rules

A valid cumulative triangle satisfies

✓ monotonic increase

✓ no decreasing cells

✓ first column equals incremental

✓ last observed cumulative equals total paid

---

Incremental validation

✓ totals reconcile

✓ negatives investigated

✓ duplicates removed

✓ development complete

---

## 19. Common Errors

Converting already cumulative data.

Double accumulation.

Sorting development incorrectly.

Mixing payment dates.

Ignoring corrections.

Dropping zero developments.

---

## 20. Best Practices

Always store

both

representations.

Incremental

for modeling.

Cumulative

for classical reserving.

Never overwrite one with the other.

Transformation should always be reproducible.

---

## Key Takeaways

Incremental and cumulative triangles are mathematically equivalent.

The transformation is exact.

Incremental data preserve the original stochastic process.

Cumulative data simplify deterministic reserving.

Modern actuarial practice maintains both simultaneously.

---

## References

- Mack (1993)
- England & Verrall (2002)
- Wüthrich & Merz (2008)
- Friedland, *Estimating Unpaid Claims Using Basic Techniques*
- Taylor, *Loss Reserving*
- ASOP No. 23 – Data Quality
- ASOP No. 56 – Modeling

---

## Next Chapter

➡️ **05-age-to-age-development-factors.md**