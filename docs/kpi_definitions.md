
# KPI Definitions

## Overview

This document defines the key performance indicators (KPIs) used in the Customer Intelligence System.

These KPIs summarize customer behavior, risk, and value to support data-driven business decisions.

---

## 1. Total Customers

Definition:
Total number of unique customers.

Calculation:
```
COUNT(CustomerID)
```

Business Value:
Provides visibility into the size of the customer base.

---

## 2. Average Predicted Revenue

Definition:
Average expected future revenue per customer.

Calculation:
```
AVERAGE(predicted_revenue)
```

Business Value:
Helps estimate overall revenue potential.

---

## 3. Average Churn Probability

Definition:
Average likelihood of customers churning.

Calculation:
```
AVERAGE(churn_probability)
```

Business Value:
Indicates overall retention risk across customers.

---

## 4. High Risk Customers

Definition:
Number of customers classified as High Risk.

Calculation:
```
COUNTROWS(churn_risk = "High Risk")
```

Business Value:
Highlights customers requiring immediate retention strategies.

---

## 5. Revenue Segment Distribution

Definition:
Distribution of customers across revenue categories:

- High Value
- Medium Value
- Low Value

Business Value:
Shows how revenue is distributed across the customer base.

---

## 6. Customer Segment Distribution

Definition:
Distribution of customers based on segmentation:

- Critical Retention Target
- At-Risk Customer
- Loyal High-Value Customer
- Standard Customer

Business Value:
Supports targeted marketing and retention strategies.

---

## 7. Churn Risk Distribution

Definition:
Distribution of customers across churn levels:

- High Risk
- Medium Risk
- Low Risk

Business Value:
Helps prioritize retention actions.

---

## 8. Top Preferred Product

Definition:
The highest-ranked product based on preference score.

Calculation Logic:
- Based on frequency, monetary, and recency
- Highest preference_score is selected
- Excludes non-product entries (POSTAGE, MANUAL, DISCOUNT)

Business Value:
Enables personalized recommendations.

---

## 9. Preference Strength Distribution

Definition:
Classification of product preference:

- Strong
- Moderate
- Weak

Business Value:
Indicates how strongly a customer prefers certain products.

---

## 10. Next Best Action

Definition:
Recommended action generated using:

- Churn risk
- Revenue segment
- Customer segment
- Top preferred product

Business Value:
Transforms insights into actionable business decisions.

---

## Conclusion

These KPIs provide a comprehensive view of customer behavior and business performance, enabling:

- Improved customer retention
- Increased revenue
- Personalized marketing strategies
- Data-driven decision makings