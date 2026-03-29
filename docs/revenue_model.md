
# Revenue Prediction Model

## Objective

The goal of this model is to predict the **future revenue of each customer** based on their historical behavior.

This model is part of the Customer Intelligence System and is designed to support:
- Customer segmentation
- Revenue forecasting
- Business decision-making

---

## Dataset

The dataset was built from transactional data using a time-based split strategy.

### Features used:

- `recency_days` → Days since last purchase
- `frequency_orders` → Number of orders
- `monetary_total` → Total historical spending
- `total_items` → Total number of items purchased
- `unique_products` → Number of unique products purchased
- `avg_order_value` → Average value per order

### Target:

- `future_revenue` → Total spending in the future window

---

## Modeling Approach

### 1. Model Selection

Multiple models were tested:

- Linear Regression (Selected)
- Random Forest
- Extra Trees
- Gradient Boosting

### Final Decision:
Linear Regression was selected because it achieved the **best performance** on validation data.

---

## Evaluation Methodology

We followed a strict evaluation strategy:

### Cross-Validation (Training Set)
- 5-fold cross-validation
- Metric: RMSE (Root Mean Squared Error)

### Final Evaluation (Test Set)
- Evaluated on unseen data

---

## Results

### Cross-Validation Performance:
- Mean RMSE: **1910.75**
- Std RMSE: **605.09**

### Test Performance:
- RMSE: **2516.99**

### Interpretation:
- The model generalizes well with a reasonable increase from CV to test error.
- This indicates no severe overfitting.

---

## Feature Importance (Interpretability)

Since Linear Regression was used, feature importance was analyzed using model coefficients.

### Key Insights:

- `monetary_total` is the strongest predictor of future revenue.
- Some features showed unexpected signs due to **multicollinearity**.
- Features like `avg_order_value` and `frequency_orders` are highly correlated.

### Important Note:

Due to feature correlations, coefficients should be interpreted with caution.

---

## Challenges

### 1. Multicollinearity
Some features are mathematically related:

This caused:
- Unstable coefficients
- Non-intuitive signs (positive/negative)

### 2. Outliers
- Some customers have extremely high revenue values
- This impacts RMSE and model stability

---

## Experiments Performed

The following improvements were tested:

### Polynomial Features
- Result: Performance worsened significantly
- Conclusion: Overfitting

### Regularization (Ridge & Lasso)
- No improvement in RMSE
- Linear model remained best

### Log Transformation
- Attempted but resulted in data issues (NaN)

---

 ## Conlustion

 - Linear Regression provided the best performance among all tested models.
 - The model is simple, fast, and interpretable.
 - Despite some coefficient instability due to correlated features, predictions remain reliable.



