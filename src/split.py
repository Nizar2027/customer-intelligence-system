import pandas as pd


def time_based_split(
    df: pd.DataFrame,
    churn_days: int = 90
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Timestamp]:

    df = df.copy()

    # convert to datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # sort
    df = df.sort_values("InvoiceDate")

    # define cutoff
    max_date = df["InvoiceDate"].max()
    cutoff_date = max_date - pd.Timedelta(days=churn_days)

    # split
    train_df = df[df["InvoiceDate"] < cutoff_date]
    future_df = df[df["InvoiceDate"] >= cutoff_date]

    print(f"Total rows: {len(df)}")
    print(f"Train rows: {len(train_df)}")
    print(f"Future rows: {len(future_df)}")
    print(f"Cutoff date: {cutoff_date}")

    return train_df, future_df, cutoff_date