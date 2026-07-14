---
title: "Bornhuetter-Ferguson"
part: "Parte II · Métodos clásicos"
chapter: 11
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

11-bornhuetter-ferguson.md
---
title: Bornhuetter-Ferguson Method
subtitle: Credibility-Based Reserving Using Prior Expected Losses
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 11
status: Draft
last_updated: 2026-07-13
---

# Bornhuetter-Ferguson Method

> *"Chain Ladder assumes that history contains all the information. Bornhuetter-Ferguson assumes that history and expert expectations should both contribute to the reserve estimate."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand the motivation behind the Bornhuetter-Ferguson (BF) method.
- Derive the BF reserve formula from first principles.
- Explain the role of Expected Loss Ratios (ELR).
- Compute Expected Ultimate Losses.
- Calculate Percent Reported and Percent Unreported.
- Estimate IBNR using BF.
- Compare BF with Chain Ladder.
- Identify situations where BF is preferable.

---

## Table of Contents

1. Introduction
2. Historical Background
3. Motivation
4. Conceptual Framework
5. Mathematical Derivation
6. Expected Ultimate Loss
7. Percent Reported and Percent Unreported
8. Bornhuetter-Ferguson Formula
9. Numerical Example
10. Relationship to Chain Ladder
11. Advantages
12. Limitations
13. Health Insurance Applications
14. Implementation
15. Diagnostics
16. Best Practices
17. Summary

---

## 1. Introduction

The Bornhuetter-Ferguson (BF) method is one of the most widely used actuarial reserving techniques for immature portfolios.

Unlike Chain Ladder, which assumes historical development fully determines future development, BF combines:

- observed claims experience, and
- an independent estimate of expected ultimate losses.

This makes BF particularly valuable when historical data are limited or unstable.

---

## 2. Historical Background

The method was introduced by

- Ronald Born
- Ronald Ferguson

during the early 1970s.

It rapidly became one of the standard actuarial methods because it avoids excessive reliance on immature development data.

Today,

it remains a core reserving methodology in

- Property & Casualty
- Health Insurance
- Reinsurance

---

## 3. Motivation

Suppose

an accident year has only developed

20%

of its expected claims.

Chain Ladder projects the remaining

80%

using only observed development.

However,

those observations may be highly volatile.

BF instead asks

> What reserve would we expect if our prior estimate of ultimate losses is approximately correct?

---

## 4. Conceptual Framework

BF combines

Observed Development

+

Expected Future Development

where

Observed claims provide evidence,

while

Expected Ultimate Losses provide prior information.

Conceptually,

```
Ultimate

=

Reported

+

Expected Unreported
```

---

## 5. Expected Ultimate Loss

Suppose

Premium

=

100 million

Expected Loss Ratio (ELR)

=

80%

Then

Expected Ultimate Loss

$$
ExpectedUltimate

=

Premium

×

ELR
$$

Example

$$
100

×

0.80

=

80
$$

million.

---

## 6. Development Percentages

Suppose

the cumulative development factor is

2.50

Then

Percent Reported

is

$$
PercentReported

=

\frac1{CDF}
$$

Example

$$
1/2.5

=

40\%
$$

---

Percent Unreported

$$
PercentUnreported

=

1-

PercentReported
$$

Example

60%

---

## 7. Bornhuetter-Ferguson Formula

The reserve is

$$
IBNR

=

ExpectedUltimate

×

PercentUnreported
$$

The ultimate loss estimate becomes

$$
Ultimate

=

Reported

+

IBNR
$$

This is the defining equation of the BF method.

---

## 8. Numerical Example

Assume

Earned Premium

100 million

Expected Loss Ratio

75%

Current Reported Losses

20 million

CDF

2.50

---

Step 1

Expected Ultimate

$$
100

×

0.75

=

75
$$

---

Step 2

Percent Reported

$$
1/2.5

=

40\%
$$

---

Step 3

Percent Unreported

60%

---

Step 4

IBNR

$$
75

×

0.60

=

45
$$

million

---

Step 5

Ultimate

$$
20

+

45

=

65
$$

million

---

## Interpretation

Notice

the BF estimate is **below** the prior expected ultimate (75 million),

because reported losses already provide information.

The unreported portion is estimated from the prior expectation.

---

## 9. Comparison with Chain Ladder

Suppose

Reported

20

CDF

2.50

---

Chain Ladder

Ultimate

$$
20

×

2.50

=

50
$$

---

Bornhuetter-Ferguson

Ultimate

65

Difference

15

million

Why?

Chain Ladder assumes observed experience is fully credible.

BF assumes limited credibility.

---

## 10. Credibility Interpretation

BF is essentially

a credibility model.

Observed claims receive increasing credibility

as development progresses.

Immature years

↓

Prior dominates.

Mature years

↓

Observed data dominate.

---

## 11. Relationship to Bayesian Statistics

BF can be interpreted as

an empirical Bayesian estimator.

Prior

↓

Expected Ultimate

Likelihood

↓

Observed Claims

Posterior

↓

BF Estimate

This interpretation explains why BF performs well for immature accident years.

---

## 12. Advantages

✔ Stable for immature years

✔ Less sensitive to volatile development

✔ Incorporates actuarial judgment

✔ Easy to explain

✔ Widely accepted

✔ Excellent for pricing-reserving consistency

---

## 13. Limitations

Requires

Expected Loss Ratio

or

Expected Ultimate Loss.

Poor priors produce poor reserves.

If ELR is biased,

BF is biased.

---

## 14. Health Insurance Applications

BF is particularly useful for

- new products
- ACA markets
- Medicare Advantage
- Medicaid expansions
- recently acquired portfolios
- benefit redesign
- provider contract changes

where historical development is limited.

---

## 15. Python Example

```python
premium = 100_000_000

elr = 0.75

reported = 20_000_000

cdf = 2.50

expected_ultimate = premium * elr

percent_reported = 1 / cdf

percent_unreported = 1 - percent_reported

ibnr = expected_ultimate * percent_unreported

ultimate = reported + ibnr

print(ultimate)
```

---

## 16. R Example

```r
premium <- 100

elr <- 0.75

reported <- 20

cdf <- 2.5

expectedUltimate <- premium * elr

percentReported <- 1 / cdf

ibnr <- expectedUltimate * (1 - percentReported)

ultimate <- reported + ibnr

ultimate
```

---

## 17. SQL Example

```sql
SELECT

premium,

elr,

premium * elr AS expected_ultimate,

1.0 / cdf AS percent_reported,

1.0 - (1.0 / cdf) AS percent_unreported,

premium * elr * (1.0 - (1.0 / cdf)) AS ibnr

FROM reserving_input;
```

---

## 18. Diagnostics

Before using BF, verify

✓ ELR is current

✓ Premium is complete

✓ Exposure is appropriate

✓ Development factors are stable

✓ CDF is reasonable

✓ Product mix is consistent

✓ No material structural changes

---

## 19. Common Mistakes

Using outdated ELRs.

Ignoring pricing changes.

Applying BF to mature accident years.

Using premium instead of earned premium.

Using CDFs from a different portfolio.

Assuming BF eliminates the need for diagnostics.

---

## 20. Best Practices

Use BF

when

- accident years are immature,
- credibility is low,
- pricing assumptions are reliable,
- management requires stable reserve estimates.

Review ELRs annually.

Reconcile BF with Chain Ladder.

Investigate material differences.

Document the rationale for the selected prior.

---

## 21. Decision Framework

| Portfolio Characteristics | Recommended Method |
|---------------------------|--------------------|
| Mature, stable | Chain Ladder |
| Immature | Bornhuetter-Ferguson |
| Highly volatile | BF |
| New product | BF |
| Stable long history | Chain Ladder |
| Low credibility | BF |
| Capital modeling | Bootstrap + BF |

---

## 22. Key Takeaways

The Bornhuetter-Ferguson method combines observed claims with an independent estimate of expected ultimate losses.

Unlike Chain Ladder,

BF does not assume immature development is fully credible.

The method is particularly appropriate for

- new portfolios,
- rapidly changing products,
- Health Insurance markets with evolving experience.

Its effectiveness depends critically on the quality of the Expected Loss Ratio and the actuarial judgment supporting that estimate.

---

## References

- Born, R. & Ferguson, R. (1972). *The Actuary and IBNR.*
- Friedland, J. *Estimating Unpaid Claims Using Basic Techniques.*
- Mack, T. (1993).
- England & Verrall (2002).
- Wüthrich & Merz (2008).
- Taylor, G. *Loss Reserving.*
- ASOP No. 5 – Incurred Health and Disability Claims.
- ASOP No. 23 – Data Quality.
- ASOP No. 56 – Modeling.

---

## Next Chapter

➡️ **12-benktander-method.md**