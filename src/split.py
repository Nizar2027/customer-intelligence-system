
import pandas as pd

def time_based_split(df, churn_days=90):
    df = df.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    max_date = df["InvoiceDate"].max()
    cutoff_date = max_date - pd.Timedelta(days=churn_days)

    train_df = df[df["InvoiceDate"] < cutoff_date]
    future_df = df[df["InvoiceDate"] >= cutoff_date]

    return train_df, future_df, cutoff_date
