# Interpretable Machine Learning for Early Sepsis Prediction from Temporal Healthcare Data

## Overview

This project presents a proof-of-concept pipeline for early sepsis prediction using temporal ICU data from the PhysioNet 2019 Challenge dataset.

The goal is to investigate how static and time-dependent clinical variables can be combined into interpretable machine learning models, with particular focus on decision-making under class imbalance and threshold-dependent performance.

---

## Repository Structure

- ML_healthcare.ipynb → main notebook  
- results/ → exported evaluation tables (threshold analysis and model comparison)

---

## Dataset

The dataset is sourced from the **PhysioNet/Computing in Cardiology Challenge 2019**.

- Each file corresponds to one ICU patient  
- Each row represents hourly measurements  
- Variables include:
  - Vital signs (HR, O2Sat, Temp, SBP, MAP, Resp, etc.)
  - Laboratory values (Glucose, Lactate, WBC, Creatinine, etc.)
  - Demographics (Age, Gender, admission information)  
- Target: early detection of sepsis (labels shifted to predict up to 6 hours before onset)

- The dataset is highly imbalanced (~3% sepsis cases), making threshold-dependent evaluation critical

Only publicly available training data is used.

---

## Methodology

The pipeline consists of the following steps:

### 1. Patient-level feature construction
- Static features from demographic and admission variables  
- Temporal features summarized over the first 12 hours:
  - mean, standard deviation, minimum, maximum, last value  

### 2. Data preprocessing
- Removal of highly sparse features  
- Median imputation for missing values  
- Handling of class imbalance  

### 3. Modeling
- Logistic Regression (primary predictive baseline)  
- Random Forest (used for feature importance analysis)  

### 4. Evaluation
- AUC and AUPRC for ranking performance  
- Threshold-dependent metrics:
  - Precision  
  - Recall  
  - F1-score  
- Precision–Recall curve analysis  

### 5. Interpretability
- Feature importance derived from Random Forest  
- Identification of clinically relevant predictors  

---

## Key Results

- The dataset is highly imbalanced (~3% sepsis cases)  
- Logistic regression models achieved AUC ≈ 0.73 using temporal features  
- Model performance is strongly dependent on decision threshold  
- Lower thresholds increase recall but lead to more false positives  
- Temporal and multimodal features provide useful predictive signal  

- Important features include:
  - Admission timing (HospAdmTime)
  - Blood pressure (MAP, SBP)
  - Respiratory rate
  - Oxygen saturation
  - Glucose
  - Age  

---

## Key Insight

In clinical prediction tasks, model performance alone is not sufficient.  
The choice of decision threshold plays a critical role in balancing early detection (recall) and false alarms (precision), making threshold selection a key component of real-world deployment.

---

## How to Run

1. Download the PhysioNet dataset (training set A and B):  
   https://physionet.org/content/challenge-2019/

2. Extract the data locally  

3. Update the dataset paths in the notebook  

4. Run all cells in:

> ML_healthcare.ipynb

---

## Limitations

- Temporal dynamics are simplified through summary statistics rather than sequence models  
- Only a subset of the available dataset may be used depending on local setup  
- No calibration or uncertainty estimation is included in this baseline pipeline  

---

## Future Work

- Sequence-based models (RNNs, Transformers)  
- SHAP-based interpretability  
- Model calibration and decision threshold optimization  
- Extension to multimodal biomedical data (e.g., oncology, omics, longitudinal systems)  

---

## Notes

This project is intended as a proof-of-concept demonstration of interpretable machine learning applied to temporal healthcare data, with emphasis on methodology, evaluation, and clinical relevance rather than model complexity.