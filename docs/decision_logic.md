
# Decision Logic

## Overview

This document explains the business logic used to transform model predictions into actionable decisions.

The system combines:

- Churn Prediction
- Revenue Prediction
- Customer Segmentation
- Preference Modeling

to generate a **Next Best Action** for each customer.

---

## 1. Churn Risk Classification

Customers are classified based on predicted churn probability:

| Churn Probability | Risk Level   |
|------------------|-------------|
| ≥ 0.65           | High Risk    |
| ≥ 0.35           | Medium Risk  |
| < 0.35           | Low Risk     |

---

## 2. Revenue Segmentation

Customers are categorized based on predicted future revenue:

| Predicted Revenue | Segment        |
|-------------------|---------------|
| ≥ 2000            | High Value     |
| ≥ 500             | Medium Value   |
| < 500             | Low Value      |

---

## 3. Customer Segmentation

Customer segments are created by combining churn risk and revenue:

| Condition                                  | Segment                      |
|-------------------------------------------|------------------------------|
| High Risk + High Value                     | Critical Retention Target    |
| High Risk                                  | At-Risk Customer             |
| Low Risk + High Value                      | Loyal High-Value Customer    |
| Otherwise                                  | Standard Customer            |

---

## 4. Preference Modeling Integration

Each customer is associated with a **Top Preferred Product**, determined using:

- Frequency of purchases
- Monetary value
- Recency of interaction

The system calculates a **preference score** and selects the highest-ranking product.

Non-product entries such as:
- POSTAGE
- MANUAL
- DISCOUNT

are excluded from recommendation logic.

---

## 5. Next Best Action Logic

The system generates personalized recommendations based on customer state:

### High Risk Customers
- Action: Offer discount on top preferred product
- Goal: Prevent churn

### Medium Risk Customers
- Action: Provide targeted promotions
- Goal: Increase engagement before risk escalates

### Loyal High-Value Customers
- Action: Upsell premium or related products
- Goal: Maximize customer lifetime value

### Standard Customers
- Action: Recommend similar or complementary products
- Goal: Encourage repeat purchases

---

## 6. Decision Flow

The system follows this sequence:

1. Predict churn probability
2. Predict future revenue
3. Classify customer risk and value
4. Assign customer segment
5. Identify top preferred product
6. Generate next best action

---

## 7. Example

### Input

- Churn Probability: 0.72
- Predicted Revenue: 850
- Top Product: "PINK HEART SHAPE EGG FRYING PAN"

### Output

- Churn Risk: High Risk
- Revenue Segment: Medium Value
- Customer Segment: At-Risk Customer
- Action:

---

## Conclusion

This decision logic transforms raw predictions into business-ready actions, enabling companies to:

- Reduce churn
- Increase revenue
- Personalize customer engagement
- Optimize marketing strategies