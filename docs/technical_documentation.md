
# Technical Documentation

## Overview

This document describes the technical architecture and components of the Customer Intelligence System.

The system is designed as an end-to-end machine learning pipeline with analytics and decision support.

---

## System Architecture

The system consists of four main layers:

1. Data Layer
2. Machine Learning Layer
3. Business Logic Layer
4. Visualization Layer

---

## 1. Data Layer

### Dataset

- Online Retail Dataset
- Transactional customer data

### Processing

- Data cleaning
- Handling missing values
- Removing cancellations and invalid entries

---

## 2. Machine Learning Layer

### Feature Engineering

Customer-level features:

- recency_days
- frequency_orders
- monetary_total
- total_items
- unique_products
- avg_order_value

---

### Churn Model

- Type: Classification
- Output: churn_probability
- Evaluation: Precision, Recall, F1 Score

---

### Revenue Model

- Type: Regression
- Output: predicted_revenue
- Evaluation: RMSE

---

### Preference Modeling

- Type: Scoring and Ranking (Non-ML)

Inputs:

- frequency
- monetary
- recency

Process:

- Normalization
- Recency inversion
- Score aggregation

Output:

- preference_score
- preference_strength

---

## 3. Business Logic Layer

Transforms model outputs into decisions:

- Churn classification
- Revenue segmentation
- Customer segmentation
- Next Best Action

Defined in:

- decision_logic.md

---

## 4. API Layer

Built using FastAPI.

Main endpoints:

- /predict → model predictions
- /preferences → customer preferences
- /health → system check

Handles:

- Model inference
- Business logic execution
- Response formatting

---

## 5. Visualization Layer

Implemented using Power BI.

Features:

- KPI dashboards
- Customer segmentation visuals
- Preference analysis
- Dynamic insights
- Recommendation engine

---

## Project Structure

```
customer-intelligence-system/

├── data/
├── notebooks/
├── src/
├── api/
├── dashboards/
├── docs/
├── models/
├── reports/
├── README.md
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- FastAPI
- Power BI

---

## Execution Flow

1. Load and clean data
2. Perform feature engineering
3. Train models
4. Generate predictions
5. Apply business logic
6. Store outputs
7. Visualize in Power BI

---

## Deployment Notes

- Local environment execution
- API ready for deployment
- Dashboard uses static data
- Extendable to real-time systems

---

## Future Improvements

- Real-time pipeline integration
- Automated retraining
- Cloud deployment
- Scalable data processing