
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_STATE = 42


def build_preference_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Clean data
    df = df.dropna(subset=["CustomerID"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df = df[(df["Quantity"] > 0) & (df["Revenue"] > 0)]

    # Grouping
    pref = df.groupby(["CustomerID", "Description"]).agg(
        frequency=("InvoiceNo", "nunique"),
        monetary=("Revenue", "sum"),
        last_purchase=("InvoiceDate", "max"),
    ).reset_index()

    # Recency
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    pref["recency_days"] = (snapshot_date - pref["last_purchase"]).dt.days

    return pref


def normalize_per_customer(pref: pd.DataFrame) -> pd.DataFrame:
    pref = pref.copy()

    pref["monetary_log"] = np.log1p(pref["monetary"])

    pref["freq_norm"] = pref.groupby("CustomerID")["frequency"].transform(
        lambda x: x / (x.max() + 1e-9)
    )

    pref["monetary_norm"] = pref.groupby("CustomerID")["monetary_log"].transform(
        lambda x: x / (x.max() + 1e-9)
    )

    pref["recency_norm"] = pref.groupby("CustomerID")["recency_days"].transform(
        lambda x: 1 - (x / (x.max() + 1e-9))
    )

    return pref


def compute_preference_score(pref: pd.DataFrame) -> pd.DataFrame:
    pref = pref.copy()

    # Final tuned weights (من شغلك 👇)
    w_freq = 0.47
    w_monetary = 0.42
    w_recency = 0.10

    pref["preference_score"] = (
        w_freq * pref["freq_norm"]
        + w_monetary * pref["monetary_norm"]
        + w_recency * pref["recency_norm"]
    )

    return pref


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    data_path = project_root / "data" / "processed" / "train_transactions.csv"
    output_path = project_root / "data" / "processed" / "customer_preferences.csv"
    reports_dir = project_root / "reports"

    reports_dir.mkdir(parents=True, exist_ok=True)

    print("Loading transactions dataset...")
    df = pd.read_csv(data_path, parse_dates=["InvoiceDate"])

    print("Building preference features...")
    pref = build_preference_features(df)

    print("Applying normalization...")
    pref = normalize_per_customer(pref)

    print("Computing preference scores...")
    pref = compute_preference_score(pref)

    print("Sorting results...")
    pref = pref.sort_values(
        ["CustomerID", "preference_score"],
        ascending=[True, False]
    )

    print("Saving preferences...")
    pref.to_csv(output_path, index=False)

    summary = {
        "num_customers": int(pref["CustomerID"].nunique()),
        "num_rows": int(len(pref)),
        "top_score_mean": float(pref.groupby("CustomerID")["preference_score"].max().mean())
    }

    summary_path = reports_dir / "preference_summary.json"

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("Done.")
    print(f"Preferences saved to: {output_path}")
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()