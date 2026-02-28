
# Data Quality Report
### Dataset: Online Retail
### File: online_retail.csv
### Audit Notebook: 01_data_audit.ipynb

## Dataset Overview:

- Total Records: 541,909
- Total Columns: 8
- Memory Usage: ~33 MB
- Time Range: December 2010 – December 2011
- Primary Market: United Kingdom (~91%)

## Data Structure:

| Column | Type | Notes |
|---|---|---|
| InvoiceNo | object | Contains cancellation indicators (prefix "C") |
| StockCode | object | Product identifier |
| Description | object | Product name (contains missing values) |
| Quantity | int64 | Contains negative values (returns) |
| InvoiceDate | datetime | Successfully converted from object |
| UnitPrice | float64 | Contains negative values |
| CustomerID | float64 | Contains missing values |
| Country | object | Highly imbalanced distribution |

## Missing Values Analysis:

| Column | Missing Count | Action Plan |
|---|---|---|
| Customer ID | 135,080 | Rows will be removed (cannot track behavior without customer) |
| Description | 1,454 | Will be retained (not critical for behavioral modeling) |

Decision:
Rows without CustomerID will be excluded from modeling phase.

## Negative Values Investigation:

### Quantity:
- Minimum: -80,995
- Indicates product returns or cancellations.
- Negative quantities will be preserved as they represent real business behavior.

### UnitPrice:
- Minimum: -11,062
- Likely price adjustments or refund corrections.
- Requires careful handling during feature engineering.

## Cancellations Analysis:

### Invoices starting with "C":
- Total Canceled Transactions: 9,288
These represent reversed or refunded transactions and are important for churn and behavior analysis.

## Distribution Analysis:

### Quantity:
- Highly skewed distribution.
- Majority of values between 1 and 10.
- Extreme outliers detected (±80,995).

### UnitPrice:
- Strong right skew.
- Majority of prices below 5.
- Extreme positive and negative outliers exist.

### CustomerID:
- Uniform distribution (identifier only).

## Geographic Distribution:
- United Kingdom dominates dataset (~495k records).
- Other countries have significantly fewer transactions.
- Dataset is geographically imbalanced.

## Identified Data Issues:
1. Missing CustomerID values.
2. Extreme outliers in Quantity.
3. Negative UnitPrice values.
4. High geographic imbalance.
5. Presence of cancellations.

## Preliminary Cleaning Decisions:
- Remove rows with missing CustomerID.
- Keep negative quantities (returns).
- Investigate negative UnitPrice cases.
- Handle extreme outliers during feature engineering.
- Convert InvoiceDate to datetime (completed).

## Conclusion:
The dataset is structurally sound and suitable for customer behavior modeling after cleaning.
Main challenges involve handling returns, cancellations, and extreme values.

