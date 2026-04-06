# From Predictive Performance to Trustworthy Temporal Modeling

## A Study of Measurement Bias and Robustness in Clinical Time-Series

## Motivation

Clinical time-series data is complex, irregular, and often shaped by clinical workflows rather than purely physiological processes. Standard machine learning approaches may inadvertently exploit artifacts such as missingness patterns and measurement frequency, leading to misleading performance estimates.

## Objective

This project investigates how predictive models behave under realistic conditions in temporal healthcare data, with a focus on robustness, interpretability, and measurement bias.

## Methodological Development

### Stage 1 - Baseline Pipeline

-   Aggregated temporal features into static representations
-   Logistic Regression and Random Forest models
-   Threshold-dependent evaluation
-   Focus on predictive performance and reproducibility

### Stage 2 - Research-Oriented Pipeline

-   Leakage-aware patient-level data splitting
-   Cohort-based evaluation to assess distribution shifts
-   Temporal feature engineering (trends, deltas, missingness indicators)
-   Interpretability analysis using coefficients and SHAP

## Key Findings

-   Models rely heavily on measurement patterns, not only physiological signals
-   Performance varies significantly across cohorts
-   High recall leads to a large number of false positives
-   Predictive signal is weak but consistent across experiments

## Discussion

These findings suggest that clinical prediction models may capture clinical behavior rather than true patient state. Interpretability methods are sensitive to data distribution, and evaluation protocols strongly influence conclusions.

## Limitations

-   No sequence-based models (e.g., RNN, Transformer)
-   Limited validation strategy
-   No uncertainty estimation

## Future Work

-   Sequence modeling for temporal dynamics
-   Domain adaptation across cohorts
-   Disentangling physiological vs measurement signals
-   Developing trustworthy and interpretable clinical prediction systems
