from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "processed" / "train_transactions.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "customer_preferences.csv"
REPORTS_DIR = BASE_DIR / "reports"

# These weights were derived from a linear regression model trained on the revenue dataset
# and later adjusted using business intuition during the preference modeling notebook.

W_FREQ = 0.47
W_MONETARY = 0.42
W_RECENCY = 0.10


def build_preference_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.dropna(subset=["CustomerID"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df = df[(df["Quantity"] > 0) & (df["Revenue"] > 0)]

    pref = df.groupby(["CustomerID", "Description"]).agg(
        frequency=("InvoiceNo", "nunique"),
        monetary=("Revenue", "sum"),
        last_purchase=("InvoiceDate", "max"),
    ).reset_index()

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

    pref["preference_score"] = (
        W_FREQ * pref["freq_norm"]
        + W_MONETARY * pref["monetary_norm"]
        + W_RECENCY * pref["recency_norm"]
    )

    return pref


def sort_preferences(pref: pd.DataFrame) -> pd.DataFrame:
    return pref.sort_values(
        ["CustomerID", "preference_score"],
        ascending=[True, False]
    ).copy()


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading transactions dataset...")
    df = pd.read_csv(DATA_PATH, parse_dates=["InvoiceDate"])

    print("Building preference features...")
    pref = build_preference_features(df)

    print("Applying normalization...")
    pref = normalize_per_customer(pref)

    print("Computing preference scores...")
    pref = compute_preference_score(pref)

    print("Sorting results...")
    pref = sort_preferences(pref)

    print("Saving preferences...")
    pref.to_csv(OUTPUT_PATH, index=False)

    summary = {
        "num_customers": int(pref["CustomerID"].nunique()),
        "num_rows": int(len(pref)),
        "top_score_mean": float(
            pref.groupby("CustomerID")["preference_score"].max().mean()
        ),
    }

    config = {
        "w_freq": W_FREQ,
        "w_monetary": W_MONETARY,
        "w_recency": W_RECENCY,
        "normalization": "per_customer",
        "monetary_transform": "log1p",
    }

    summary_path = REPORTS_DIR / "preference_summary.json"
    config_path = REPORTS_DIR / "preference_config.json"

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print("Done.")
    print(f"Preferences saved to: {OUTPUT_PATH}")
    print(f"Summary saved to: {summary_path}")
    print(f"Config saved to: {config_path}")


if __name__ == "__main__":
    main()