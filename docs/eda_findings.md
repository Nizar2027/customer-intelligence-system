
# Exploratory Data Analysis (EDA)

This document summarizes the key findings from the exploratory data analysis performed in the notebook:

`notebooks/03_eda.ipynb`.

The goal of this analysis is to understand the structure of the transaction dataset, identify data quality issues, analyze purchasing behavior, and prepare insights that guide the feature engineering stage of the project.


## Overview

This notebook explores the **training transaction dataset** for the Customer Intelligence System.  
The analysis focuses on understanding transaction structure, temporal behavior, customer activity, product demand, revenue patterns, and basic numeric relationships before moving into feature engineering.

The dataset contains transactional line items, where each row represents a product within an invoice rather than a complete order.

---

## 1. Initial Data Inspection

The analysis started by loading `train_transactions.csv` and creating a working copy for exploration.

A quick preview of the data showed the main columns:

- `InvoiceNo`
- `StockCode`
- `Description`
- `Quantity`
- `InvoiceDate`
- `UnitPrice`
- `CustomerID`
- `Country`

Basic descriptive statistics revealed several important characteristics:

- Quantity contains both positive and negative values
- Unit price includes extreme values and at least one negative value
- Customer IDs are missing for a noticeable portion of rows
- The dataset spans from **December 2010 to September 2011** in the training window

---

## 2. Daily and Monthly Activity Patterns

### Transaction-line activity per day
The first time-series plot examined the number of transaction rows per day.  
This showed strong day-to-day variation, with high volatility across the training period.

### Unique invoices per day
A second daily plot counted **unique invoice numbers per day**, which provides a better approximation of actual order activity than raw transaction-line counts.  
This confirmed that the dataset is invoice-based and that line-level volume and order-level volume are different concepts.

### 7-day rolling average
A rolling 7-day mean was then applied to the daily transaction-line counts.  
This smoothing revealed the underlying activity trend more clearly by reducing daily noise.

### Monthly activity
Monthly aggregation showed that activity is not evenly distributed across months.  
There are visible fluctuations over time, and September appears lower because the training window ends before the month is complete.

---

## 3. Weekly and Hourly Purchase Behavior

### Day of week
A bar chart of `day_of_week` showed that purchasing activity is concentrated on business weekdays.

Observed pattern:

- Highest activity appears on **Thursday** and **Tuesday**
- Sunday is clearly lower than the main weekdays

This suggests that customer purchasing behavior follows a strong weekly rhythm.

### Hour of day
The hour distribution showed that most activity occurs during daytime working hours.

Observed pattern:

- Activity begins around **08:00**
- Strong concentration between roughly **10:00 and 16:00**
- Very little activity appears in late evening hours

This indicates that the store operates primarily in daytime commercial hours.

---

## 4. Quantity, Price, and Revenue Distributions

### Quantity distribution
The quantity histogram showed a highly skewed distribution:

- Most rows contain relatively small quantities
- There are negative quantities, which suggest returns or cancellations
- There are extreme outliers on the positive side

### Unit price distribution
The unit price histogram is also heavily skewed:

- Most products are low-priced
- A few very large values stretch the distribution
- Negative unit prices are present and require interpretation

### Raw revenue distribution
Revenue was calculated at line level as:

`Revenue = Quantity × UnitPrice`

The raw revenue histogram was highly compressed because of extreme values and skewness.

### Positive-only revenue distribution
Restricting revenue to positive values improved interpretability but still showed a strong right-skew.

### Log-transformed revenue
Applying `log1p()` to positive revenue created a much more readable distribution, confirming that revenue is strongly right-skewed and may benefit from log-based treatment in downstream analysis.

---

## 5. Country-Level Revenue

Revenue was aggregated by country and sorted in descending order.

Key observation:

- **United Kingdom** dominates total revenue by a very large margin
- Other countries such as **EIRE, Netherlands, Germany, France, and Australia** contribute much smaller totals

This indicates that the business is heavily concentrated in one primary market.

---

## 6. Product-Level Insights

### Top products by quantity sold
Products were grouped by `Description` and summed by `Quantity`.

This revealed the most frequently purchased products, including items such as:

- WORLD WAR 2 GLIDERS ASSTD DESIGNS
- JUMBO BAG RED RETROSPOT
- PACK OF 72 RETROSPOT CAKE CASES
- WHITE HANGING HEART T-LIGHT HOLDER

### Top products by revenue
Revenue was also aggregated by product description.

This highlighted high-revenue products, including:

- REGENCY CAKESTAND 3 TIER
- DOTCOM POSTAGE
- PARTY BUNTING
- WHITE HANGING HEART T-LIGHT HOLDER

This distinction is important because the most frequently sold products are not always the same as the products generating the highest revenue.

### Top products bar chart
The top product quantities were visualized in a bar chart, providing a clearer comparison of product popularity.

---

## 7. Customer-Level Insights

### Top customers by total quantity purchased
Customers were grouped by `CustomerID` and summed by quantity.  
This highlighted the heaviest buyers in terms of product volume.

### Top customers by number of invoices
Customers were also ranked using the number of **unique invoices** rather than raw quantity.

This is more useful for behavior analysis because it measures how often a customer places orders, not just how many items they bought.

### Orders per customer distribution
A histogram of invoice counts per customer showed a highly skewed structure:

- Most customers place only a small number of orders
- A small minority of customers place many orders

This is a common pattern in retail and strongly supports the use of customer-level behavioral features later.

### Customer revenue distribution
Customer-level revenue was computed by summing line-level revenue per customer.

The resulting histogram showed a very strong long-tail pattern:

- Most customers generate relatively low total revenue
- A small set of customers contribute disproportionately large revenue

This confirms the presence of customer value concentration in the business.

---

## 8. Missing Values and Data Quality Issues

### Missing CustomerID
Two checks were performed on `CustomerID`:

- total missing count
- missing proportion

Findings:

- Missing `CustomerID` rows are substantial
- The missing ratio is approximately **27.5%**

This is one of the most important data quality findings in the notebook and will affect feature engineering because customer-level features cannot be created for rows without an identified customer.

### Negative unit price
Rows with negative `UnitPrice` were isolated.

The observed examples had descriptions such as:

- `Adjust bad debt`

This suggests that these are accounting or adjustment entries rather than normal purchase transactions.

### Extreme quantity outlier
An extremely large quantity value of **80995** was checked.

- It was not found in the training set under the inspected filter
- A matching row was found in the future dataset

This confirms the existence of extreme transaction outliers that should be considered during downstream processing.

---

## 9. Cancellations and Returns

Invoices beginning with `"C"` were inspected.

Findings:

- These rows correspond to cancelled or reversed transactions
- Their quantities are negative
- The total count of such invoice rows is non-trivial

This strongly indicates that:

- negative quantities often represent returns/cancellations
- invoice prefix `"C"` is a useful rule for identifying them

These business rules will be important when engineering clean customer-level features.

---

## 10. Daily Revenue Trend

Daily total revenue was aggregated and plotted across time.

This analysis complements transaction counts because it measures **financial activity** rather than just row volume.

The plot shows:

- substantial daily volatility
- occasional strong spikes
- no simple stable linear pattern

This suggests that revenue behavior is irregular and may depend on promotions, basket composition, or calendar effects.

---

## 11. Correlation Analysis

A numeric correlation matrix was generated for:

- `Quantity`
- `UnitPrice`
- `CustomerID`
- `hour`

The observed correlations were all very small, close to zero.

Interpretation:

- there is no strong linear relationship among these transaction-level numeric variables
- simple raw transaction fields are unlikely to provide strong predictive signal on their own

This reinforces the need for **feature engineering at customer level**, especially features such as recency, frequency, monetary value, average basket behavior, and preference patterns.

---

## 12. Main EDA Conclusions

The exploratory analysis leads to the following conclusions:

1. The dataset is **line-item transactional data**, not order-level customer behavior data.
2. Order activity varies meaningfully across days, weeks, and months.
3. Purchase behavior follows clear weekly and hourly patterns.
4. Quantity, unit price, and revenue are all strongly skewed, with extreme outliers present.
5. A large portion of rows are missing `CustomerID`, which limits direct customer-level modeling from raw data.
6. Negative quantities and `"C"`-prefixed invoices indicate cancellations/returns.
7. Negative unit price rows appear to be accounting adjustments rather than retail purchases.
8. Customer activity is highly concentrated: a small group of customers generates many orders and a large share of revenue.
9. Product demand is concentrated in a relatively small set of popular items.
10. Transaction-level raw numeric variables have weak linear correlations, so stronger behavioral features must be engineered.

---

## 13. Implication for the Next Stage

Based on these findings, the next stage should focus on transforming transactional data into **customer-level features**, including:

- Recency
- Frequency
- Monetary value
- Order count
- Average basket size
- Average order value
- Product/category preference features

These engineered features will provide a stronger foundation for:

- churn prediction
- revenue forecasting
- preference modeling