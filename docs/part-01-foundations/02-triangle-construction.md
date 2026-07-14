---
title: Triangle Construction
subtitle: Building Development Triangles from Raw Health Insurance Claims Data
author: Health Insurance Reserving Handbook
version: 1.0
status: Draft
last_updated: 2026-07-13
chapter: 02
part: "Parte I · Fundamentos"
language: "es"
---

# Triangle Construction

> *"A reserving model is only as good as the triangle it is built upon."*

---

## Learning Objectives

After completing this chapter, the reader should be able to:

- Understand why actuarial triangles exist.
- Transform claim-level data into development triangles.
- Distinguish between incremental and cumulative triangles.
- Compute development lags correctly.
- Select the appropriate exposure period.
- Identify common construction errors.
- Validate triangles before reserving.
- Produce production-ready triangles for actuarial analyses.

---

## Table of Contents

1. Introduction
2. Why Triangles?
3. Claim Life Cycle
4. Required Data
5. Triangle Dimensions
6. Accident, Report, Service and Payment Dates
7. Development Lag
8. Incremental Triangles
9. Cumulative Triangles
10. Triangle Types
11. Construction Algorithm
12. Practical Example
13. Data Validation
14. Common Problems
15. Best Practices
16. Summary

---

## 1. Introduction

A development triangle is the fundamental data structure used in actuarial reserving.

Rather than modeling each individual claim independently, actuaries aggregate historical claim development into a structured matrix.

This matrix summarizes how losses emerge over time.

Every deterministic and stochastic reserving methodology starts from this representation.

---

## 2. Why Do We Build Triangles?

Insurance liabilities develop gradually.

Claims:

- occur,
- are reported,
- receive multiple payments,
- may be reopened,
- finally close.

Since development occurs over months or years, we need a structure capable of representing this evolution.

Development triangles provide exactly that representation.

---

## 3. Claim Life Cycle

```text
Policy Effective

      │

      ▼

Accident Occurs

      │

      ▼

Medical Service

      │

      ▼

Provider Billing

      │

      ▼

Claim Reported

      │

      ▼

Adjudication

      │

      ▼

First Payment

      │

      ▼

Additional Payments

      │

      ▼

Claim Closed
```

Each stage contributes information used in reserving.

---

## 4. Required Data

A minimum claim-level dataset should include:

| Variable | Required | Description |
|-----------|----------|-------------|
| Claim ID | ✓ | Unique identifier |
| Accident Date | ✓ | Date loss occurred |
| Service Date | ✓ | Medical service date |
| Report Date | ✓ | Claim notification |
| Payment Date | ✓ | Date payment issued |
| Paid Amount | ✓ | Payment amount |
| Case Reserve | ✓ | Outstanding reserve |
| Line of Business | ✓ | Product |
| Coverage | Optional | Benefit |
| Provider | Optional | Healthcare provider |
| Diagnosis | Optional | ICD codes |
| Procedure | Optional | CPT/HCPCS |

---

## 5. Triangle Dimensions

Every triangle has two dimensions.

Rows:

Accident Period

Columns:

Development Period

Example

| Accident Month | Dev0 | Dev1 | Dev2 | Dev3 |
|----------------|------|------|------|------|
| Jan | | | | |
| Feb | | | | |
| Mar | | | | |

---

## 6. Choosing the Origin Period

Several origin periods are possible.

## Accident Date

Most common in Property & Casualty.

Advantages

- reflects when risk occurred
- stable

---

## Service Date

Widely used in Health Insurance.

Advantages

- aligns medical utilization
- PMPM analysis

---

## Report Date

Useful for operational metrics.

Not generally recommended for reserving.

---

## Payment Date

Never use as origin period.

Payment date defines development.

---

## 7. Development Lag

Development lag measures elapsed time between the origin period and payment.

Definition

```
Lag = Payment Date − Origin Date
```

Measured in months.

Example

| Accident | Payment | Lag |
|----------|----------|-----|
| Jan | Jan | 0 |
| Jan | Feb | 1 |
| Jan | Mar | 2 |
| Jan | Apr | 3 |

---

## 8. Incremental Triangles

Incremental triangles store payments occurring during each development period.

Example

| Accident | 0 |1|2|3|
|-----------|--|--|--|--|
|Jan|100|40|20|5|
|Feb|90|30|10||
|Mar|110|25|||

Each cell represents

Payments made only during that development month.

---

## Mathematical Representation

Let

```
X(i,j)
```

represent the incremental payment.

Then

```
X(i,j) ≥ 0
```

---

## 9. Cumulative Triangles

Cumulative values are obtained by

```
C(i,j)=ΣX(i,k)
```

where

k ≤ j

Example

Incremental

| Accident |0|1|2|
|-----------|--|--|--|
|Jan|100|40|20|

becomes

| Accident |0|1|2|
|-----------|--|--|--|
|Jan|100|140|160|

---

## Relationship

Incremental

↓

Cumulative

↓

Development Factors

↓

Ultimate

↓

IBNR

---

## 10. Triangle Types

Several triangle definitions exist.

## Paid Triangle

Contains paid losses only.

Most stable.

---

## Reported Triangle

Contains reported amounts.

---

## Incurred Triangle

Paid

+

Case Reserve

---

## Claim Count Triangle

Number of claims.

Useful for frequency modeling.

---

## Severity Triangle

Average payment.

---

## PMPM Triangle

Per Member Per Month.

Frequently used in Health Insurance.

---

## 11. Construction Algorithm

Step 1

Import claim-level data.

Step 2

Validate dates.

Step 3

Remove duplicates.

Step 4

Calculate development lag.

Step 5

Assign accident period.

Step 6

Aggregate

GROUP BY

Accident Month

Development Month

Step 7

Pivot.

Step 8

Create cumulative triangle.

Step 9

Validate totals.

---

## SQL Example

```sql
SELECT

accident_month,

development_month,

SUM(paid_amount)

FROM claims

GROUP BY

accident_month,

development_month;
```

---

## Python Example

```python
triangle = (
    claims
    .groupby(
        ["accident_month",
         "development_month"]
    )["paid_amount"]
    .sum()
    .unstack(fill_value=0)
)
```

---

## R Example

```r
triangle <-

claims |>

group_by(

accident_month,

development_month

) |>

summarise(

paid=sum(paid_amount)

)
```

---

## 12. Worked Example

Raw Claims

|Claim|Accident|Payment|Paid|
|------|---------|-------|----|
|1|Jan|Jan|100|
|2|Jan|Feb|40|
|3|Jan|Mar|20|
|4|Feb|Feb|90|
|5|Feb|Mar|30|

Incremental Triangle

|Accident|0|1|2|
|---------|--|--|--|
|Jan|100|40|20|
|Feb|90|30|0|

Cumulative Triangle

|Accident|0|1|2|
|---------|--|--|--|
|Jan|100|140|160|
|Feb|90|120|120|

---

## 13. Validation

Before reserving, verify

✓ totals reconcile

✓ no negative lags

✓ duplicate claims removed

✓ payments balanced

✓ calendar complete

✓ development continuous

✓ accident periods ordered

✓ cumulative monotonicity

---

## 14. Common Errors

## Using payment date as accident date

Wrong.

---

## Missing development periods

Produces biased factors.

---

## Negative development

Requires investigation.

---

## Duplicate claims

Artificial reserve inflation.

---

## Incorrect aggregation

Mixing service date and accident date.

---

## Calendar gaps

Missing months distort averages.

---

## 15. Health Insurance Specific Considerations

Unlike Property & Casualty,

Health Insurance introduces

- provider billing delays
- encounter claims
- pharmacy claims
- capitation
- coordination of benefits
- retroactive eligibility
- claim adjustments
- denied claims
- reversals
- corrected claims

Each may require customized preprocessing before triangle construction.

---

## 16. Production Checklist

□ Raw data reconciled

□ Eligibility validated

□ Duplicate claims removed

□ Dates validated

□ Development lag computed

□ Triangle completed

□ Incremental validated

□ Cumulative validated

□ Totals reconciled

□ Ready for Chain Ladder

---

## Key Takeaways

- Triangle quality determines reserving quality.
- Incremental triangles preserve original information.
- Cumulative triangles are used by most classical reserving methods.
- Health Insurance requires additional preprocessing compared with Property & Casualty.
- Every reserving exercise begins with rigorous triangle validation.

---

## References

- Friedland, *Estimating Unpaid Claims Using Basic Techniques*
- England & Verrall (2002)
- Mack (1993)
- Wüthrich & Merz (2008)
- Taylor, *Loss Reserving*
- ASOP No. 23 – Data Quality
- ASOP No. 41 – Actuarial Communications
- ASOP No. 56 – Modeling

---

## Next Chapter

➡️ **03-development-lags-and-triangle-transformations.md**