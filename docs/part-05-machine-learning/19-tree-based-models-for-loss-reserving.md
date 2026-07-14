---
title: "Tree-Based Models for Loss Reserving"
part: "Parte V · Machine Learning"
chapter: 19
language: "es"
status: "draft"
last_updated: "2026-07-14"
---

19-tree-based-models-for-loss-reserving.md
---
title: Tree-Based Models for Loss Reserving
subtitle: Decision Trees, Random Forests and Gradient Boosting for Health Insurance Reserving
author: Health Insurance Reserving Handbook
version: 1.0
chapter: 19
status: Draft
last_updated: 2026-07-13
---

# Tree-Based Models for Loss Reserving

> *"Tree-based models replace actuarial assumptions with recursive partitioning, allowing the data to identify the drivers of reserve development."*

---

## Learning Objectives

After completing this chapter, the reader should be able to

- Understand the mathematical foundation of decision trees.
- Explain recursive partitioning.
- Build Random Forest models.
- Implement Gradient Boosting.
- Understand XGBoost, LightGBM and CatBoost.
- Compare ensemble methods.
- Evaluate feature importance.
- Apply tree-based methods to Health Insurance reserving.
- Deploy production-ready models.

---

## Table of Contents

1. Introduction
2. Why Tree-Based Models?
3. Decision Trees
4. Recursive Partitioning
5. Regression Trees
6. Tree Pruning
7. Random Forest
8. Gradient Boosting
9. XGBoost
10. LightGBM
11. CatBoost
12. Feature Importance
13. Explainability
14. Hyperparameter Tuning
15. Validation
16. Health Insurance Applications
17. Production Architecture
18. Best Practices
19. Summary

---

## 1 Introduction

Decision Trees are among the most interpretable Machine Learning models.

Unlike GLMs,

they make almost no assumptions regarding

- linearity
- distributions
- interactions

Instead,

they recursively partition the feature space.

---

## 2 Why Trees?

Traditional reserving assumes

stable development.

Trees assume

the data determine

the prediction rules.

Example

Instead of

```
Reserve = β₀ + β₁ Age
```

a tree learns

```
Age < 65 ?

│

├── Yes

│     Reserve = ...

│

└── No

      Reserve = ...
```

---

## 3 Recursive Partitioning

Decision Trees repeatedly split observations.

Objective

maximize

homogeneity

within each node.

General algorithm

```
Dataset

↓

Best Split

↓

Left Node

Right Node

↓

Repeat

↓

Leaf Nodes
```

---

## 4 Mathematical Formulation

Suppose

training observations

$$
(x_i,y_i)
$$

The algorithm searches

split

$$
(x_j,c)
$$

minimizing

Residual Sum of Squares

$$
RSS

=

\sum

(y_i-\bar y)^2
```

within each partition.

---

# 5 Regression Trees

Leaves contain

predicted reserve

$$
\hat y

=

mean(y)
$$

of observations

inside each leaf.

Prediction becomes

piecewise constant.

---

# 6 Tree Depth

Increasing depth

↓

Lower Bias

Higher Variance

Decreasing depth

↓

Higher Bias

Lower Variance

Maximum depth

is therefore

a tuning parameter.

---

# 7 Pruning

Large trees

overfit.

Pruning minimizes

$$
Cost

=

RSS

+

\alpha

Leaves
$$

where

$$
\alpha
$$

controls

tree complexity.

---

# 8 Random Forest

Random Forest

combines

many trees.

Algorithm

```
Bootstrap Sample

↓

Tree

Bootstrap Sample

↓

Tree

Bootstrap Sample

↓

Tree

↓

Average Prediction
```

---

# 9 Bagging

Bootstrap Aggregation

reduces variance.

Each tree

sees

a different sample.

Prediction

equals

average

of all trees.

---

# 10 Random Feature Selection

Each split

considers

only

a random subset

of predictors.

Advantages

- decorrelation
- improved robustness
- reduced overfitting

---

# 11 Out-of-Bag Error

Approximately

one-third

of observations

are excluded

from each bootstrap sample.

These observations estimate

generalization error

without

additional validation data.

---

# 12 Gradient Boosting

Boosting

learns

sequentially.

Each tree

corrects

errors

made by previous trees.

Workflow

```
Initial Prediction

↓

Residuals

↓

Tree 1

↓

Residuals

↓

Tree 2

↓

Residuals

↓

...

↓

Final Prediction
```

---

# 13 XGBoost

XGBoost extends

Gradient Boosting

through

- regularization
- parallel computing
- missing-value handling
- sparse optimization
- tree pruning

Objective

$$
Loss

+

Regularization
$$

Regularization

reduces

overfitting.

---

# 14 LightGBM

LightGBM

introduces

Histogram Learning

Leaf-wise Growth

Gradient-based Sampling

Advantages

- faster
- scalable
- lower memory
- excellent for large portfolios

---

# 15 CatBoost

CatBoost

focuses

on

categorical variables.

Advantages

- minimal preprocessing
- ordered boosting
- reduced prediction shift

Useful for

Health Insurance

where

categorical variables dominate.

Examples

- provider
- diagnosis
- region
- plan
- employer

---

# 16 Feature Importance

Common metrics

- Gain
- Split Count
- SHAP
- Permutation Importance

Example

| Variable | Importance |
|------------|-----------|
| Development | 28% |
| Paid-to-Date | 21% |
| Diagnosis | 15% |
| Age | 12% |
| Provider | 10% |
| Inflation | 7% |
| Region | 4% |
| Others | 3% |

---

# 17 SHAP Values

SHAP

explains

individual predictions.

Example

Reserve Prediction

```
Base

120

+

Age

+10

+

Development

+15

+

Provider

−8

=

137
```

This provides

local interpretability.

---

# 18 Hyperparameter Tuning

Important parameters

## Decision Tree

- max_depth
- min_samples_leaf
- min_samples_split

---

## Random Forest

- n_estimators
- max_features
- max_depth

---

## XGBoost

- learning_rate
- max_depth
- gamma
- subsample
- colsample_bytree
- lambda
- alpha

---

## LightGBM

- num_leaves
- max_depth
- learning_rate
- feature_fraction

---

## CatBoost

- depth
- learning_rate
- iterations

---

# 19 Cross Validation

Time-dependent data

require

rolling validation.

Recommended

```
Train

↓

Validate

↓

Advance Window

↓

Repeat
```

Avoid

random sampling.

---

# 20 Python Example

Decision Tree

```python
from sklearn.tree import DecisionTreeRegressor

tree = DecisionTreeRegressor(

max_depth=6

)

tree.fit(X_train,y_train)
```

---

Random Forest

```python
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(

n_estimators=500,

max_depth=10,

random_state=123

)

rf.fit(X_train,y_train)
```

---

XGBoost

```python
from xgboost import XGBRegressor

xgb = XGBRegressor(

n_estimators=1000,

learning_rate=0.03,

max_depth=6,

subsample=0.8,

colsample_bytree=0.8

)

xgb.fit(X_train,y_train)
```

---

LightGBM

```python
from lightgbm import LGBMRegressor

lgb = LGBMRegressor(

n_estimators=1000,

num_leaves=64,

learning_rate=0.03

)

lgb.fit(X_train,y_train)
```

---

CatBoost

```python
from catboost import CatBoostRegressor

cat = CatBoostRegressor(

iterations=1000,

depth=8,

learning_rate=0.03,

verbose=False

)

cat.fit(X_train,y_train)
```

---

# 21 Model Evaluation

Recommended metrics

Regression

- RMSE
- MAE
- MAPE
- R²

Business

- Reserve Bias
- Reserve Stability
- Prediction Interval Coverage
- Financial Impact

---

# 22 Health Insurance Applications

Tree models perform well for

- Medicare Advantage
- Medicaid
- ACA
- Provider contracting
- Pharmacy
- Stop-loss
- High-cost claim prediction
- Risk adjustment
- Medical inflation

---

# 23 Production Pipeline

```
Claims

↓

Validation

↓

Feature Engineering

↓

Training

↓

Cross Validation

↓

Hyperparameter Optimization

↓

SHAP

↓

Backtesting

↓

Deployment

↓

Monitoring
```

---

# 24 Governance

Every production model should include

✓ Data Lineage

✓ Version Control

✓ Hyperparameter Documentation

✓ Independent Validation

✓ SHAP Reports

✓ Drift Detection

✓ Retraining Schedule

✓ Peer Review

✓ Audit Trail

---

# 25 Relationship with ASOPs

Tree-based reserving models should be governed consistently with:

| ASOP | Relevance |
|-------|-----------|
| ASOP 5 | Health claim reserving principles |
| ASOP 23 | Data quality and preprocessing |
| ASOP 41 | Communication of assumptions, limitations and results |
| ASOP 56 | Model design, validation and governance |

In practice, documentation should explain why a tree-based model is appropriate, how it was validated, and what limitations remain.

---

# 26 Comparison

| Model | Accuracy | Speed | Interpretability |
|---------|----------|--------|-----------------|
| Decision Tree | Moderate | Excellent | Excellent |
| Random Forest | High | High | Moderate |
| XGBoost | Very High | High | Moderate |
| LightGBM | Very High | Excellent | Moderate |
| CatBoost | Very High | High | Moderate |

---

# 27 Common Pitfalls

- Using random train/test splits on temporal claims data.
- Ignoring concept drift after regulatory or operational changes.
- Overfitting through excessive tree depth.
- Failing to explain predictions to stakeholders.
- Treating feature importance as causal evidence.
- Ignoring reserve stability across valuation dates.
- Using ML models without benchmarking against actuarial methods.

---

# 28 Best Practices

- Benchmark every ML model against Chain Ladder and GLM.
- Perform rolling-origin validation.
- Monitor prediction drift after deployment.
- Explain material reserve movements with SHAP.
- Document feature engineering decisions.
- Keep deterministic and statistical benchmark models in production.
- Retrain only after evaluating changes in portfolio characteristics.

---

# 29 Hybrid Actuarial–Machine Learning Framework

A recommended production framework combines classical actuarial methods with ML.

```text
Claims Data
      │
      ▼
Data Quality (ASOP 23)
      │
      ▼
Triangle Construction
      │
      ├──────────────┐
      ▼              ▼
Chain Ladder      Machine Learning
      │              │
      ▼              ▼
Benchmark      Predictive Model
      └──────┬───────┘
             ▼
      Model Comparison
             ▼
 Professional Judgment
             ▼
      Final Reserve
```

This approach preserves the transparency of traditional reserving while leveraging the predictive capabilities of modern machine learning.

---

# Key Takeaways

Tree-based models provide a flexible alternative to classical reserving by automatically learning nonlinear relationships and interactions among predictors.

Ensemble methods such as Random Forest, XGBoost, LightGBM, and CatBoost generally outperform single decision trees in predictive accuracy, but require stronger governance, validation, and explainability.

For Health Insurance reserving, these models are particularly valuable when claim-level data are available and portfolios exhibit complex operational, clinical, or demographic drivers that cannot be adequately represented by traditional development triangles alone.

---

# References

- Breiman, L. (1984). *Classification and Regression Trees.*
- Breiman, L. (2001). *Random Forests.*
- Friedman, J. (2001). *Greedy Function Approximation: A Gradient Boosting Machine.*
- Chen, T. & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System.*
- Ke, G. et al. (2017). *LightGBM: A Highly Efficient Gradient Boosting Decision Tree.*
- Dorogush, A., Ershov, V., & Gulin, A. (2018). *CatBoost: Gradient Boosting with Categorical Features.*
- Wüthrich, M. *Machine Learning in Non-Life Insurance.*
- ASOP No. 5 – Incurred Health and Disability Claims.
- ASOP No. 23 – Data Quality.
- ASOP No. 41 – Actuarial Communications.
- ASOP No. 56 – Modeling.

---

# Next Chapter

➡️ **20-deep-learning-for-loss-reserving.md**
```
