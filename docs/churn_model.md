
# Churn Prediction Model

## 1. Problem Definition

The goal of this model is to predict customers who are likely to stop purchasing (churn).

This is formulated as a **binary classification problem**:
- 1 → Customer will churn
- 0 → Customer will remain active

### Business Objective

The primary objective is to **maximize recall**, ensuring that as many potential churn customers as possible are identified.

Missing a churn customer is more costly than incorrectly flagging a non-churn customer.

---

## 2. Dataset

The dataset was derived from customer transaction records.

### Target Variable
- `churn_label`: Indicates whether a customer churned.

### Features (Engineered)

Key features include:

- `recency_days`: Days since last purchase
- `frequency_orders`: Number of orders
- `monetary_total`: Total spending
- `total_items`: Total quantity purchased
- `unique_products`: Number of unique products
- `avg_order_value`: Average order value

These features capture customer purchasing behavior using the **RFM framework**.

---

## 3. Data Preparation

- Cleaned invalid and negative values
- Converted date columns to datetime format
- Applied a **time-based split** to prevent data leakage
- Generated structured datasets for modeling

---

## 4. Modeling Approach

Several machine learning models were evaluated:

- Decision Tree
- Bagging
- Random Forest
- Voting Classifier (Hard & Soft)
- AdaBoost
- Gradient Boosting
- Stacking (final model)

---

## 5. Evaluation Strategy

To ensure reliable evaluation:

- Cross-validation was used on the training set
- The test set was kept completely unseen until final evaluation

Evaluation metrics included:
- Precision
- Recall
- F1 Score
- Precision-Recall Curve

---

## 6. Threshold Tuning

Instead of using the default classification threshold (0.5), threshold tuning was applied.

### Objective:
Achieve **Recall ≈ 70%**

The threshold was selected using:
- Cross-validated probability predictions
- Precision-Recall curve analysis

---

## 7. Final Model Selection

The final model selected was:

> **Stacking Classifier**

### Reasons:
- Combines multiple models to improve performance
- Learns how to optimally aggregate predictions
- Achieved the best balance between recall and precision

---

## 8. Model Architecture

### Base Models:
- Logistic Regression (with feature scaling)
- Random Forest
- Support Vector Machine (with feature scaling)

### Meta Model:
- Logistic Regression

---

## 9. Final Performance (Test Set)

| Metric | Value |
|------|------|
| Accuracy | 0.662 |
| Precision | 0.604 |
| Recall | 0.662 |
| F1 Score | 0.632 |

### Confusion Matrix
# Churn Prediction Model

## 1. Problem Definition

The goal of this model is to predict customers who are likely to stop purchasing (churn).

This is formulated as a **binary classification problem**:
- 1 → Customer will churn
- 0 → Customer will remain active

### Business Objective

The primary objective is to **maximize recall**, ensuring that as many potential churn customers as possible are identified.

Missing a churn customer is more costly than incorrectly flagging a non-churn customer.

---

## 2. Dataset

The dataset was derived from customer transaction records.

### Target Variable
- `churn_label`: Indicates whether a customer churned.

### Features (Engineered)

Key features include:

- `recency_days`: Days since last purchase
- `frequency_orders`: Number of orders
- `monetary_total`: Total spending
- `total_items`: Total quantity purchased
- `unique_products`: Number of unique products
- `avg_order_value`: Average order value

These features capture customer purchasing behavior using the **RFM framework**.

---

## 3. Data Preparation

- Cleaned invalid and negative values
- Converted date columns to datetime format
- Applied a **time-based split** to prevent data leakage
- Generated structured datasets for modeling

---

## 4. Modeling Approach

Several machine learning models were evaluated:

- Decision Tree
- Bagging
- Random Forest
- Voting Classifier (Hard & Soft)
- AdaBoost
- Gradient Boosting
- Stacking (final model)

---

## 5. Evaluation Strategy

To ensure reliable evaluation:

- Cross-validation was used on the training set
- The test set was kept completely unseen until final evaluation

Evaluation metrics included:
- Precision
- Recall
- F1 Score
- Precision-Recall Curve

---

## 6. Threshold Tuning

Instead of using the default classification threshold (0.5), threshold tuning was applied.

### Objective:
Achieve **Recall ≈ 70%**

The threshold was selected using:
- Cross-validated probability predictions
- Precision-Recall curve analysis

---

## 7. Final Model Selection

The final model selected was:

> **Stacking Classifier**

### Reasons:
- Combines multiple models to improve performance
- Learns how to optimally aggregate predictions
- Achieved the best balance between recall and precision

---

## 8. Model Architecture

### Base Models:
- Logistic Regression (with feature scaling)
- Random Forest
- Support Vector Machine (with feature scaling)

### Meta Model:
- Logistic Regression

---

## 9. Final Performance (Test Set)

| Metric | Value |
|------|------|
| Accuracy | 0.662 |
| Precision | 0.604 |
| Recall | 0.662 |
| F1 Score | 0.632 |

### Confusion Matrix
[[254 130]
[101 198]]

---

## 10. Interpretation

- The model successfully identifies approximately **66% of churn customers**
- Precision remains acceptable, reducing unnecessary false alarms
- The model provides a strong balance aligned with business needs

---

## 11. Key Insights

- Churn prediction is inherently challenging due to limited observable behavior
- Feature engineering (RFM-based features) plays a critical role
- Threshold tuning significantly improves business alignment

---

## 12. Model Artifacts

The following artifacts were generated:

- `churn_stacking_model.joblib`
- `churn_threshold.json`
- `churn_features.json`
- `churn_test_metrics.json`

---

## 13. Conclusion

The final churn prediction model provides a reliable and practical solution for identifying customers at risk of leaving.

Future improvements may include:
- Incorporating behavioral and interaction data
- Enhancing feature engineering
- Exploring more advanced gradient boosting techniques