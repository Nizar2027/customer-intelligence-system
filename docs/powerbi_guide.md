
# Power BI Guide

## Overview

This document explains the structure, purpose, and usage of the Power BI dashboard in the Customer Intelligence System.

The dashboard translates model outputs into business-ready insights and recommendations.

It is organized into two main pages:

- Executive Overview
- Customer Preferences

---

## Dashboard Objectives

The Power BI dashboard is designed to:

- Monitor customer churn risk
- Track predicted revenue
- Identify customer segments
- Analyze customer preferences
- Generate business insights
- Support next best action decisions

---

## Data Sources

The dashboard uses precomputed outputs generated from the machine learning pipeline.

Main tables used:

- `customer_insights`
- `customer_preferences_dashboard`

These tables contain:

- Churn probability
- Churn risk
- Predicted revenue
- Revenue segment
- Customer segment
- Preference score
- Preference strength
- Product-level preference data

---

## Page 1: Executive Overview

### Purpose

Provides a high-level business view of customer status, risk, value, and recommended actions.

### Main Components

#### KPI Cards

- Total Customers
- Average Revenue
- Average Churn Risk
- High Risk Customers

#### Dynamic Insight

A text-based measure that describes the current state of the customer base.

Examples:
- High-value customers are at risk
- Customers with high churn risk are present
- Customer base is stable

#### Dynamic Recommendation

A text-based measure that recommends strategic action based on current customer conditions.

Examples:
- Focus on at-risk customers
- Launch retention actions
- Strengthen loyalty and upselling

#### Visuals

- Revenue Segment Distribution
- Customer Segment Distribution
- Churn Risk Distribution
- Scatter Plot: Predicted Revenue vs Churn Probability
- Customer Detail Table

#### Filters

- `churn_risk`
- `customer_segment`

---

## Page 2: Customer Preferences

### Purpose

Provides customer-level analysis of product preferences and recommended actions.

### Main Components

#### Customer Filter

A dropdown slicer based on `CustomerID`.

This allows the dashboard user to analyze one customer at a time.

#### Top Products Table

Displays the top preferred products for the selected customer.

Columns include:

- `description`
- `preference_score`
- `frequency`
- `monetary`

Aggregation rules:

- `preference_score` → Max
- `frequency` → Sum
- `monetary` → Sum

The table is filtered to show Top 5 products by `preference_score`.

#### Next Best Action

A text-based recommendation generated using:

- Top preferred product
- Churn risk
- Customer segment

Examples:
- Offer discount on preferred product
- Recommend similar items
- Use upselling strategy

---

## Dynamic Measures

### Dynamic Insight

Purpose:
Describe the current condition of the customer base.

Used in:
- Executive Overview page

### Dynamic Recommendation

Purpose:
Suggest an action at the dashboard level.

Used in:
- Executive Overview page

### Top Product

Purpose:
Identify the highest-ranked product for a selected customer.

Used in:
- Customer Preferences page

### Next Best Action

Purpose:
Generate personalized action recommendations based on customer state and preference.

Used in:
- Customer Preferences page

---

## Preference Logic in Power BI

The preference dashboard uses the selected `CustomerID` to filter all visuals.

The recommendation logic excludes non-product entries such as:

- POSTAGE
- MANUAL
- DISCOUNT

This ensures that the top product is a valid item for recommendation.

---

## Usage Instructions

### Executive Overview

Use this page to:

- Monitor portfolio-wide customer health
- Review strategic customer segments
- Understand revenue and churn patterns
- Identify high-risk groups

### Customer Preferences

Use this page to:

- Inspect one customer at a time
- Review top preferred products
- Understand product-level preference strength
- Generate next best action recommendations

---

## Design Notes

The dashboard was designed to support:

- Clear executive storytelling
- Business interpretation of model outputs
- Action-oriented decision support
- Simple and clean navigation

The layout prioritizes:

- KPI visibility
- Dynamic text insights
- Customer segmentation
- Recommendation clarity

---

## File Location

The Power BI dashboard file is stored in:

```text
dashboards/customer_intelligence_dashboard.pbix
```

---

## Future Improvements

- Add category-level preference analysis
- Add cross-sell recommendations
- Add drill-through customer profile page
- Connect to live API or database
- Add scheduled refresh and monitoring