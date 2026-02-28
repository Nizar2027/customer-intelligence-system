
# Welcome to the Customer Intelligence Corporation

## In this project, we use a real-world online retail transactions dataset to design and implement a Customer Intelligence System helps companies to:

- Predicting customers who may stop purchasing.
- Revenue forcast.
- Understanding customers preferences.
- Proposing appropriate marketing actions and recommendations.

## What is dataset about:

### It is a real dataset from kaggle contains:
- Customer ID
- Invoice date
- Products
- Unit price + Quantity
- Country
 And those will represent customers behaviour over time.

 ## Frame the problem

### 1. Business objective:

### The business objective of this system is to reduce customer churn and increase revenue by leveraging predictive analytics through:
- Identifying customers at risk of early churn.
- Targeting them with suitable offers.
- Improving marketing campaigns based on preferences.
### Churn Definition:
A customer is considered churned if they have not made any purchase within 90 days following their last recorded transaction.
The model predicts the probability that a customer will churn within the next 90 days.

### 2. How company will use this system?
It will be used inside the company as following:
- Marketing team will see the dashboards in Power Bi.
- System provides API Endpoint for internal systems (CRM/ERP).
- The management makes decisions based on reports.

### 3. How probably current solution often looks like?
Current solutions often:
- Employees relied on their experience.
- Public marketing campaigns for everyone.
- Without careful analysis.
For example send discounts for all customers instead of targeting customers at risk of leaving.
And this is costly and ineffective.

## Our system's types of predicting:
- For churn prediction task its a classification type.
- For Revenue forcasting task its a regression type.
- For customres prefrences task its a ranking/scoring type.

## Our system's types of learning:
- For churn prediction task its a supervised learning type.
- For Revenue forcasting task its a supervised regression type.
- For customres prefrences task its often not a supervised model but rather feature-based scoring or simple clustering.
The system follows a Batch Learning approach, as the dataset is static and does not require real-time model updates. Models will be retrained periodically using updated transaction data.

## Performance measures:
To properly evaluate the effectiveness of the proposed Customer Intelligence System, appropriate performance metrics must be selected for each predictive task.

### 1. Churn Prediction (Classification Task):
Since churn prediction is a binary classification problem (customer will churn or not), accuracy alone is not sufficient, especially in cases where class imbalance may exist.
Therefore:
- Primary metric: ROC-AUC
- Secondry metric: F1-Score
ROC-AUC is selected as the primary evaluation metric because it measures the model’s ability to distinguish between churn and non-churn customers across different threshold settings. F1-score is used as a complementary metric to balance precision and recall, ensuring that high-risk customers are correctly identified without generating excessive false positives.

### 2. Revenue Forecasting (Regression Task):
Revenue forecasting is a supervised regression problem where the model predicts a numerical value representing future customer spending.
- Primary metric: Root Mean Squared Error (RMSE).
- Secondary metric: Mean Absolute Error (MAE).
RMSE is selected as the primary metric because it penalizes large prediction errors more heavily, which is critical in financial forecasting scenarios where significant deviations may negatively impact business decisions. MAE is used as a secondary metric to provide an interpretable average error magnitude.

### 3. Customer Preference Modeling:
Customer preference modeling is primarily implemented using feature-based scoring and ranking techniques. Since this task does not rely on labeled outputs, traditional supervised evaluation metrics are not applicable. Instead, interpretability and business validation will be used to assess effectiveness.

## Assumptions Validation:
Before proceeding with model development, it is important to validate the key assumptions underlying this project:
1. The company requires actual churn probabilities rather than categorical labels only.
2. Revenue forecasts must provide numerical predictions instead of grouped spending categories.
3. The predictive outputs will be integrated into internal CRM/ERP systems through APIs.
4. Customer transaction data is reliable and consistently linked to unique customer identifiers.
5. Historical transaction behavior is representative of future customer behavior.
If any of these assumptions change, the problem formulation (e.g., regression vs classification) may need to be revised accordingly.
After validating these assumptions with stakeholders, the system design remains aligned with business requirements.

