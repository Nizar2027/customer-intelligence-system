
# Customer Intelligence System

## Overview

The Customer Intelligence System is an end-to-end data science project designed to transform raw transactional data into actionable business decisions.

The system combines machine learning, analytics, and business logic to:

- Predict customer churn
- Forecast future revenue
- Understand customer preferences
- Segment customers
- Generate personalized recommendations

---

## Business Objectives

The system addresses key business challenges:

- Identifying customers at risk of churn
- Predicting future customer value
- Understanding customer behavior and preferences
- Supporting targeted marketing strategies
- Enabling data-driven decision making

---

## System Components

### 1. Machine Learning Models

- Churn Prediction (Classification)
- Revenue Forecasting (Regression)

### 2. Preference Modeling

- Scoring-based approach (no supervised model)
- Based on:
  - Frequency
  - Monetary value
  - Recency

### 3. Customer Segmentation

Customers are grouped into:

- Critical Retention Target
- At-Risk Customer
- Loyal High-Value Customer
- Standard Customer

### 4. Decision Engine

The system generates a **Next Best Action** for each customer based on:

- Churn risk
- Revenue segment
- Customer segment
- Product preferences

---

## Dataset

- Online Retail Dataset
- Transactional data containing customer purchases

---

## Methodology

### Data Processing

- Data cleaning
- Handling missing values
- Removing invalid transactions

### Feature Engineering

Customer-level features:

- recency_days
- frequency_orders
- monetary_total
- total_items
- unique_products
- avg_order_value

### Modeling

- Classification model for churn prediction
- Regression model for revenue prediction

### Preference Modeling

- Normalization of features
- Recency inversion
- Weighted scoring
- Ranking products per customer

---

## Results

The system produces:

- Churn risk classification (High, Medium, Low)
- Revenue segmentation (High, Medium, Low)
- Customer segmentation
- Top preferred products
- Personalized recommendations
- Next Best Action for each customer

---

## Power BI Dashboard

The system includes an interactive Power BI dashboard with:

### Executive Overview

- KPIs
- Customer segmentation
- Churn analysis
- Revenue distribution
- Dynamic insights
- Business recommendations

### Customer Preferences

- Customer-level filtering
- Top preferred products
- Preference strength
- Next Best Action

Dashboard file:

```
dashboards/customer_intelligence_dashboard.pbix
```

---

## API

A FastAPI backend is included to serve:

- Customer predictions
- Preference data
- Model outputs

Endpoints:

- `/predict`
- `/preferences`
- `/health`

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

## Key Features

- End-to-end machine learning pipeline
- Business-driven feature engineering
- Preference-based recommendation system
- Customer segmentation strategy
- Decision engine for actionable insights

---

## Future Improvements

- Real-time API integration
- Automated model retraining
- Product category recommendations
- Cross-sell and upsell strategies
- Cloud deployment

---

## Conclusion

This project demonstrates how machine learning can be integrated with business logic and analytics tools to create a complete customer intelligence system.

It moves beyond prediction to deliver:

- Insights
- Recommendations
- Decisions