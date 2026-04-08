
# Model Monitoring

## Overview

This document describes how the models in the Customer Intelligence System should be monitored over time.

The system includes:

- Churn Prediction Model (Classification)
- Revenue Prediction Model (Regression)
- Preference Modeling (Scoring System)

Monitoring ensures that model performance remains stable and reliable in production.

---

## 1. Monitoring Objectives

The main goals of model monitoring are:

- Detect performance degradation
- Identify data drift
- Ensure prediction consistency
- Maintain business reliability

---

## 2. Churn Model Monitoring

### Key Metrics

- Precision
- Recall
- F1 Score
- ROC AUC

### Threshold Monitoring

The model uses a fixed threshold:

- High Risk ≥ 0.65
- Medium Risk ≥ 0.35

Important checks:

- Stability of High Risk percentage
- Sudden increase or decrease in churn predictions

---

## 3. Revenue Model Monitoring

### Key Metrics

- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)

### Monitoring Points

- Distribution of predicted revenue
- Percentage of zero values after cleaning
- Detection of extreme values

---

## 4. Data Drift Monitoring

Monitor changes in input features over time:

- recency_days
- frequency_orders
- monetary_total
- avg_order_value

### Example Checks

- Mean and median shifts
- Distribution changes
- Outlier increase

---

## 5. Prediction Drift

Monitor output distributions:

- Churn probability distribution
- Revenue prediction distribution
- Segment distribution

### Expected Behavior

Based on the current dataset:

- Most customers fall into Low Risk and Medium Risk
- High Risk customers represent a smaller portion of the dataset

### Warning Signals

- Sudden increase in High Risk customers
- Unusual drop in Low Risk customers
- Extremely imbalanced distribution (e.g., all customers become High Risk)

These changes may indicate:

- Data drift
- Model instability
- Incorrect input data
---

## 6. Preference Monitoring

Monitor preference behavior:

- Top products stability
- Preference score distribution
- Frequency and monetary changes

Important checks:

- Dominance of a single product
- Sudden changes in top products

---

## 7. Business Monitoring

Track business-level indicators:

- High Risk Customers count
- Revenue segments distribution
- Customer segments distribution

These are visible in Power BI dashboard KPIs.

---

## 8. Alerts (Future)

Possible alert conditions:

- Sudden increase in churn rate
- Drop in predicted revenue
- Data distribution shift
- Missing or corrupted data

---

## 9. Monitoring Strategy

Recommended approach:

- Daily dashboard review
- Weekly metric evaluation
- Monthly model validation

---

## 10. Future Improvements

- Automated monitoring pipeline
- Model retraining triggers
- Drift detection algorithms
- Logging and tracking system