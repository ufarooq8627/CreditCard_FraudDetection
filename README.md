# 🛡️ FraudShield AI — Credit Card Fraud Detection

A machine learning project that detects credit card fraud using **Neural Networks (MLPClassifier)** trained on the [Kaggle Credit Card Fraud Detection Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). Includes an interactive **Streamlit web app** for real-time fraud prediction.

---

## 📊 Project Overview

Credit card fraud is a major problem in the financial industry. This project tackles the challenge of detecting fraud in a **highly imbalanced dataset** (only 0.17% are fraud) using:

- **SMOTE** oversampling to balance the dataset
- **Stratified K-Fold** cross-validation for robust evaluation
- **4 ML models** compared: Logistic Regression, Random Forest, XGBoost, Neural Network
- **Threshold optimization** using Precision-Recall curve analysis

### 🏆 Model Comparison (on Original Test Data)

| Model | Fraud Precision | Fraud Recall | F1 Score | Accuracy |
|-------|:--------------:|:------------:|:--------:|:--------:|
| Logistic Regression | 0.04 | 0.91 | 0.08 | 0.97 |
| XGBoost | 0.00 | 1.00 | 0.01 | 0.64 |
| **Neural Network** 🏆 | **0.65** | **1.00** | **0.79** | **1.00** |

> **Winner: Neural Network (MLPClassifier)** — Catches 100% of fraud with the best F1 score.

---

## 🚀 Features

- **Jupyter Notebook** — Full EDA, preprocessing, model training, and evaluation pipeline
- **Streamlit Web App** — Interactive fraud prediction with:
  - 🎲 Random transaction generator (normal + real fraud)
  - ✏️ Manual input with pre-built demo presets
  - 📄 CSV batch upload for bulk predictions
  - 📊 Real-time probability scores and verdict display
  - 🔍 Key fraud indicator reference panel

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| **Language** | Python 3.x |
| **ML Libraries** | scikit-learn, XGBoost, imbalanced-learn (SMOTE) |
| **Data** | pandas, NumPy |
| **Visualization** | matplotlib, seaborn |
| **Web App** | Streamlit |
| **Deployment** | joblib (model serialization) |

---

## 📁 Project Structure

```
Credit_Card_Fraud_Det/
├── exercise/
│   ├── cc_fraud_detection.ipynb   # Main notebook (EDA → Training → Evaluation)
│   ├── app.py                     # Streamlit web application
│   ├── creditcard.csv             # Dataset (284,807 transactions)
│   ├── models/
│   │   ├── fraud_model.pkl        # Saved Neural Network model
│   │   └── rbscaler.pkl           # Saved RobustScaler
│   └── .streamlit/
│       └── config.toml            # Streamlit theme & config
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/Credit_Card_Fraud_Det.git
cd Credit_Card_Fraud_Det/exercise
```

### 2. Install Dependencies
```bash
pip install pandas numpy scikit-learn xgboost imbalanced-learn matplotlib seaborn streamlit joblib
```

### 3. Run the Notebook
Open `cc_fraud_detection.ipynb` in Jupyter Notebook or VS Code to see the full analysis pipeline.

### 4. Launch the Web App
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 📓 Notebook Pipeline

1. **Data Exploration** — Distribution plots, class imbalance visualization, time analysis
2. **Feature Engineering** — RobustScaler on Amount & Time, PCA feature correlation heatmap
3. **Resampling** — SMOTE oversampling to create balanced training data
4. **Model Training** — 4 models with Stratified 5-Fold Cross-Validation:
   - Logistic Regression (baseline)
   - Random Forest (ensemble)
   - XGBoost (ensemble)
   - Neural Network / MLPClassifier (deep learning)
5. **Evaluation** — Confusion matrix, classification report, precision-recall curve
6. **Threshold Optimization** — F1-maximizing threshold at 0.9978
7. **Deployment** — Model saved as `.pkl` for production use

---

## 🔍 Key Findings

- **Recall is the most important metric** for fraud detection — missing fraud costs more than false alarms
- **Neural Network achieved 100% fraud recall** on the original test data
- **SMOTE oversampling** was critical — models trained on imbalanced data performed poorly
- **Threshold tuning** improved F1 from 0.79 → 0.94 by raising the decision threshold to 0.9978
- **V14, V12, V10, V17** are the strongest fraud indicators (PCA components)

---

## 📸 App Screenshots

### Legitimate Transaction Detection
The app correctly identifies normal transactions as safe with high confidence.

### Fraudulent Transaction Detection  
Real fraud patterns trigger the alert system with 99.99%+ confidence.

### Manual Input with Presets
Pre-built demo presets allow quick demonstration of fraud vs legitimate detection.

---

## 📄 Dataset

- **Source:** [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Size:** 284,807 transactions over 2 days
- **Features:** 30 (V1–V28 from PCA + Time + Amount)
- **Fraud Rate:** 0.17% (492 frauds out of 284,807)

> ⚠️ The `creditcard.csv` file is ~150MB and may need to be added to `.gitignore`. Download it separately from Kaggle.

---

## 👤 Author

**Farooque** — GUVI Capstone Project

---

## 📜 License

This project is for educational purposes as part of the GUVI Data Science curriculum.
