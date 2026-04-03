
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "data" / "processed" / "train_transactions.csv"
FUTURE_PATH = BASE_DIR / "data" / "processed" / "future_transactions.csv"

CHURN_OUTPUT_PATH = BASE_DIR / "data" / "processed" / "churn_dataset.csv"
REVENUE_OUTPUT_PATH = BASE_DIR / "data" / "processed" / "revenue_dataset.csv"


def load_transactions(file_path: str | Path) -> pd.DataFrame:
    """
    Load transaction data and parse InvoiceDate as datetime.
    """
    return pd.read_csv(file_path, parse_dates=["InvoiceDate"])


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows without CustomerID.
    """
    df = df.dropna(subset=["CustomerID"]).copy()
    return df


def add_revenue_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create Revenue column as Quantity * UnitPrice.
    """
    df = df.copy()
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    return df


def get_snapshot_date(train_df: pd.DataFrame) -> pd.Timestamp:
    """
    Define snapshot date as one day after the last transaction date
    in the training window.
    """
    return train_df["InvoiceDate"].max() + pd.Timedelta(days=1)


def build_customer_features(
    transactions: pd.DataFrame,
    snapshot_date: pd.Timestamp
) -> pd.DataFrame:
    """
    Aggregate transaction-level data into customer-level behavioral features.
    """
    features = transactions.groupby("CustomerID").agg(
        recency_days=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        frequency_orders=("InvoiceNo", "nunique"),
        monetary_total=("Revenue", "sum"),
        total_items=("Quantity", "sum"),
        unique_products=("StockCode", "nunique"),
    )

    features["avg_order_value"] = (
        features["monetary_total"] / features["frequency_orders"]
    )

    return features.reset_index()


def build_future_labels(future_transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate future-window transactions to create future revenue
    and future order counts per customer.
    """
    future_labels = future_transactions.groupby("CustomerID").agg(
        future_revenue=("Revenue", "sum"),
        future_orders=("InvoiceNo", "nunique"),
    )

    return future_labels.reset_index()


def build_model_dataset(
    customer_features: pd.DataFrame,
    future_labels: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge historical customer features with future labels.
    Customers with no purchases in the future window receive:
    - future_revenue = 0
    - future_orders = 0
    - churn_label = 1
    """
    model_dataset = customer_features.merge(
        future_labels,
        on="CustomerID",
        how="left"
    )

    model_dataset["future_revenue"] = model_dataset["future_revenue"].fillna(0)
    model_dataset["future_orders"] = model_dataset["future_orders"].fillna(0)

    model_dataset["churn_label"] = (
        model_dataset["future_orders"] == 0
    ).astype(int)

    return model_dataset


def build_churn_dataset(model_dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Create churn dataset using only historical features and churn label.
    Future-only fields are removed to prevent leakage.
    """
    return model_dataset.drop(columns=["future_revenue", "future_orders"]).copy()


def build_revenue_dataset(model_dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Create revenue dataset using only historical features and future revenue label.
    Future-only helper fields are removed to prevent leakage.
    """
    return model_dataset.drop(columns=["churn_label", "future_orders"]).copy()


def save_dataset(df: pd.DataFrame, output_path: str | Path) -> None:
    """
    Save dataset to CSV.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def run_feature_pipeline() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Full feature engineering pipeline:
    1. Load train and future transactions
    2. Clean missing CustomerID rows
    3. Create Revenue column
    4. Build customer-level features from train window
    5. Build labels from future window
    6. Merge features and labels
    7. Create churn and revenue datasets
    8. Save outputs
    """
    train_df = load_transactions(TRAIN_PATH)
    future_df = load_transactions(FUTURE_PATH)

    train_df = clean_transactions(train_df)
    future_df = clean_transactions(future_df)

    train_df = add_revenue_column(train_df)
    future_df = add_revenue_column(future_df)

    snapshot_date = get_snapshot_date(train_df)

    customer_features = build_customer_features(train_df, snapshot_date)
    future_labels = build_future_labels(future_df)

    model_dataset = build_model_dataset(customer_features, future_labels)

    churn_dataset = build_churn_dataset(model_dataset)
    revenue_dataset = build_revenue_dataset(model_dataset)

    save_dataset(churn_dataset, CHURN_OUTPUT_PATH)
    save_dataset(revenue_dataset, REVENUE_OUTPUT_PATH)

    return model_dataset, churn_dataset, revenue_dataset


if __name__ == "__main__":
    model_dataset, churn_dataset, revenue_dataset = run_feature_pipeline()

    print("Feature engineering completed successfully.")
    print(f"Model dataset shape: {model_dataset.shape}")
    print(f"Churn dataset shape: {churn_dataset.shape}")
    print(f"Revenue dataset shape: {revenue_dataset.shape}")