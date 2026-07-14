---
title: "Benktander Method"
part: "Parte II · Métodos clásicos"
chapter: 12
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

12-benktander-method.md
---
title: Benktander Method
subtitle: Iterative Credibility Reserving Between Chain Ladder and Bornhuetter-Ferguson
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 12
status: Draft
last_updated: 2026-07-13
---

# Benktander Method

> *"Bornhuetter-Ferguson trusts the prior. Chain Ladder trusts the data. Benktander gradually shifts trust from the prior to the observed experience."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand the motivation behind the Benktander method.
- Explain why it is considered an iterative Bornhuetter-Ferguson model.
- Derive the Benktander equations.
- Implement multiple Benktander iterations.
- Understand the credibility interpretation.
- Compare Benktander with Chain Ladder and Bornhuetter-Ferguson.
- Apply the method to Health Insurance portfolios.

---

## Table of Contents

1. Introduction
2. Historical Background
3. Motivation
4. Conceptual Framework
5. Mathematical Derivation
6. First Iteration
7. General Iterative Form
8. Convergence
9. Practical Example
10. Comparison with Other Methods
11. Health Insurance Applications
12. Implementation
13. Diagnostics
14. Best Practices
15. Summary

---

## 1. Introduction

Benktander occupies the middle ground between

- Bornhuetter-Ferguson
- Chain Ladder

Instead of assuming

either

complete credibility

or

limited credibility,

it allows credibility to increase gradually.

The method therefore produces a sequence of reserve estimates that converge toward Chain Ladder as more credibility is assigned to observed development.

---

## 2. Historical Background

Gunnar Benktander introduced the method during the 1970s.

The objective was to reduce the dependence on the Expected Loss Ratio while avoiding the instability of pure Chain Ladder.

Today,

Benktander is frequently used for

- immature portfolios
- catastrophe business
- specialty insurance
- Health Insurance products undergoing rapid change

---

## 3. Motivation

Consider an accident year that has developed only 20%.

Chain Ladder assumes

the observed 20%

fully represents future development.

Bornhuetter-Ferguson assumes

the remaining 80%

should follow the expected ultimate.

Reality usually lies between these extremes.

Benktander provides that compromise.

---

## 4. Credibility Interpretation

Suppose

Current development

contains

some information,

but

not enough

to replace actuarial expectations.

Benktander updates the reserve iteratively.

Each iteration increases credibility assigned to observed experience.

Eventually,

the estimate converges toward Chain Ladder.

---

## 5. Relationship Among Methods

```
Expected Ultimate

↓

Bornhuetter-Ferguson

↓

Benktander

↓

Chain Ladder
```

This progression reflects increasing reliance on observed claim experience.

---

## 6. Bornhuetter-Ferguson Review

Recall

Expected Ultimate

$$
U_0
=
Premium
\times
ELR
$$

Reported

$$
R
$$

Percent Reported

$$
p
=
\frac1{CDF}
$$

Percent Unreported

$$
q
=
1-p
$$

Bornhuetter-Ferguson

$$
U_{BF}
=
R
+
qU_0
$$

---

## 7. First Benktander Iteration

The first Benktander estimate is

$$
U_1
=
R
+
qU_{BF}
$$

Replacing

\(U_{BF}\)

gives

$$
U_1
=
R
+
q(R+qU_0)
$$

Simplifying

$$
U_1
=
(1+q)R
+
q^2U_0
$$

Notice

the observed experience receives more weight than under BF.

---

## 8. General Iterative Form

The recursive equation is

$$
U_{k+1}
=
R
+
qU_k
$$

where

- \(U_k\) is the previous iteration.
- \(q\) is the unreported percentage.

Each iteration incorporates additional credibility.

---

## 9. Closed-Form Solution

Expanding the recursion,

$$
U_k
=
R
\sum_{i=0}^{k-1}
q^i
+
q^kU_0
$$

Since

$$
\sum_{i=0}^{k-1}
q^i
=
\frac{1-q^k}{1-q}
$$

we obtain

$$
U_k
=
R
\frac{1-q^k}{1-q}
+
q^kU_0
$$

---

## 10. Convergence

Because

$$
0<q<1
$$

then

$$
q^k
\rightarrow
0
$$

as

$$
k\rightarrow\infty
$$

Therefore

$$
U_k
\rightarrow
\frac{R}{1-q}
$$

Since

$$
1-q
=
p
=
\frac1{CDF}
$$

the limit becomes

$$
U_\infty
=
R
\times
CDF
$$

which is precisely the

Chain Ladder estimate.

---

## 11. Interpretation

Iteration

0

↓

Bornhuetter-Ferguson

Iteration

∞

↓

Chain Ladder

Benktander therefore forms a continuous bridge between the two methods.

---

## 12. Numerical Example

Suppose

Reported

40

Expected Ultimate

100

CDF

2.50

Then

Percent Reported

40%

Percent Unreported

60%

---

## Bornhuetter-Ferguson

IBNR

60

Ultimate

100

---

## First Benktander Iteration

$$
40
+
0.60(100)
=
100
$$

---

## Second Iteration

$$
40
+
0.60(100)
=
100
$$

Suppose instead

Expected Ultimate

80

Iteration sequence

|Iteration|Ultimate|
|----------|--------|
|BF|88.0|
|1|92.8|
|2|95.7|
|3|97.4|
|4|98.5|
|∞|100.0|

The estimate gradually approaches Chain Ladder.

---

## 13. Comparison with Chain Ladder

Chain Ladder

- Complete credibility.
- Fully data-driven.
- Sensitive to immature years.

Benktander

- Partial credibility.
- Stable.
- Iterative.
- Smooth transition toward observed development.

---

## 14. Comparison with Bornhuetter-Ferguson

Bornhuetter-Ferguson

- Single credibility level.

Benktander

- Increasing credibility.
- Multiple iterations.
- Flexible.

---

## 15. Health Insurance Applications

Benktander performs well when

- enrollment changes rapidly,
- provider contracts change,
- benefit redesign occurs,
- ACA markets mature,
- Medicaid programs expand,
- Medicare Advantage membership grows quickly.

These situations often invalidate pure Chain Ladder while making a fixed BF prior too restrictive.

---

## 16. Python Example

```python
reported = 40

expected = 80

cdf = 2.5

q = 1 - 1/cdf

ultimate = expected

for i in range(5):

    ultimate = reported + q * ultimate

    print(i + 1, ultimate)
```

---

## 17. R Example

```r
reported <- 40

expected <- 80

cdf <- 2.5

q <- 1 - 1/cdf

ultimate <- expected

for(i in 1:5){

 ultimate <- reported + q*ultimate

 print(ultimate)

}
```

---

## 18. SQL Example

Recursive Common Table Expression

```sql
WITH RECURSIVE benktander AS (

SELECT

1 AS iteration,

expected_ultimate AS reserve

UNION ALL

SELECT

iteration + 1,

reported + q * reserve

FROM benktander

WHERE iteration < 5

)

SELECT *

FROM benktander;
```

---

## 19. Diagnostics

Before applying Benktander,

review

✓ Expected Loss Ratio

✓ Premium adequacy

✓ Development factors

✓ Portfolio maturity

✓ Structural changes

✓ Product mix

✓ Credibility of prior assumptions

---

## 20. Advantages

✔ Stable.

✔ Less volatile than Chain Ladder.

✔ More adaptive than BF.

✔ Naturally incorporates credibility.

✔ Smooth convergence.

✔ Easy to explain.

---

## 21. Limitations

Requires

Expected Ultimate.

Choice of iteration number

is subjective.

Not appropriate

if

Expected Loss Ratio

is unreliable.

---

## 22. Decision Framework

| Portfolio | Preferred Method |
|------------|------------------|
| Mature | Chain Ladder |
| Immature | BF |
| Moderately Mature | Benktander |
| New Product | BF |
| Transitional Portfolio | Benktander |
| Highly Stable | Chain Ladder |

---

## 23. Best Practices

Run

Chain Ladder,

Bornhuetter-Ferguson,

and

Benktander

together.

Investigate material differences.

Document

the rationale

for selecting

the final reserve.

Treat Benktander

as a credibility model,

not merely another reserving algorithm.

---

## Key Takeaways

The Benktander method extends Bornhuetter-Ferguson by increasing the credibility assigned to observed claims through successive iterations.

The sequence converges mathematically to the Chain Ladder estimate, making Benktander a flexible bridge between prior expectations and empirical development.

Its primary strength lies in balancing actuarial judgment with observed experience, making it particularly valuable for moderately mature portfolios and evolving Health Insurance products.

---

## References

- Benktander, G. (1976). *An Approach to Credibility in Claims Reserving.*
- Born, R. & Ferguson, R. (1972).
- Mack, T. (1993).
- England & Verrall (2002).
- Friedland, J. *Estimating Unpaid Claims Using Basic Techniques.*
- Wüthrich & Merz (2008).
- Taylor, G. *Loss Reserving.*
- ASOP No. 5 – Incurred Health and Disability Claims.
- ASOP No. 23 – Data Quality.
- ASOP No. 56 – Modeling.

---

## Next Chapter

➡️ **13-cape-cod-method.md**