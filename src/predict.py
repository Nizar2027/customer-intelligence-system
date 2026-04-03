
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.business_rules import (
    assign_customer_segment,
    classify_churn_risk,
    classify_preference_strength,
    classify_revenue_segment,
)
from src.data_validation import validate_prediction_input


BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

CHURN_MODEL_PATH = MODELS_DIR / "churn_stacking_model.joblib"
CHURN_THRESHOLD_PATH = MODELS_DIR / "churn_threshold.json"
CHURN_FEATURES_PATH = MODELS_DIR / "churn_features.json"

REVENUE_MODEL_PATH = MODELS_DIR / "revenue_linear_model.joblib"
REVENUE_FEATURES_PATH = MODELS_DIR / "revenue_features.json"

PREFERENCES_PATH = DATA_DIR / "customer_preferences.csv"


def load_json_file(file_path: str | Path) -> Any:
    """
    Load a JSON file and return its contents.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_churn_artifacts():
    """
    Load churn model, threshold, and feature names.
    """
    model = joblib.load(CHURN_MODEL_PATH)
    threshold_data = load_json_file(CHURN_THRESHOLD_PATH)
    feature_names = load_json_file(CHURN_FEATURES_PATH)

    threshold = float(threshold_data["threshold"])

    return model, threshold, feature_names


def load_revenue_artifacts():
    """
    Load revenue model and feature names.
    """
    model = joblib.load(REVENUE_MODEL_PATH)
    feature_names = load_json_file(REVENUE_FEATURES_PATH)

    return model, feature_names


def prepare_input_dataframe(
    input_data: dict[str, Any],
    feature_names: list[str]
) -> pd.DataFrame:
    """
    Convert input dictionary to validated DataFrame with correct feature order.
    """
    input_df = pd.DataFrame([input_data])
    input_df = validate_prediction_input(input_df, feature_names)
    return input_df


def predict_churn(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Predict churn probability, binary churn output, and business risk label.
    """
    model, threshold, feature_names = load_churn_artifacts()
    input_df = prepare_input_dataframe(input_data, feature_names)

    churn_probability = float(model.predict_proba(input_df)[0, 1])
    churn_prediction = int(churn_probability >= threshold)
    churn_risk = classify_churn_risk(churn_probability)

    return {
        "churn_probability": churn_probability,
        "churn_prediction": churn_prediction,
        "threshold": threshold,
        "churn_risk": churn_risk,
    }


def predict_revenue(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Predict future revenue and business value segment.
    """
    model, feature_names = load_revenue_artifacts()
    input_df = prepare_input_dataframe(input_data, feature_names)

    predicted_revenue = float(model.predict(input_df)[0])
    revenue_segment = classify_revenue_segment(predicted_revenue)

    return {
        "predicted_revenue": predicted_revenue,
        "revenue_segment": revenue_segment,
    }


def predict_customer_profile(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Run both churn and revenue predictions, then assign final customer segment.
    """
    churn_result = predict_churn(input_data)
    revenue_result = predict_revenue(input_data)

    customer_segment = assign_customer_segment(
        churn_probability=churn_result["churn_probability"],
        predicted_revenue=revenue_result["predicted_revenue"],
    )

    return {
        **churn_result,
        **revenue_result,
        "customer_segment": customer_segment,
    }


def get_customer_preferences(
    customer_id: int | float,
    top_n: int = 5
) -> dict[str, Any]:
    """
    Retrieve top product preferences for a given customer.
    """
    pref_df = pd.read_csv(PREFERENCES_PATH)

    customer_pref = pref_df[pref_df["CustomerID"] == customer_id].copy()

    if customer_pref.empty:
        return {
            "customer_id": customer_id,
            "top_preferences": [],
        }

    customer_pref = customer_pref.sort_values(
        "preference_score",
        ascending=False
    ).head(top_n)

    top_preferences = []
    for _, row in customer_pref.iterrows():
        top_preferences.append(
            {
                "description": row["Description"],
                "preference_score": float(row["preference_score"]),
                "preference_strength": classify_preference_strength(
                    float(row["preference_score"])
                ),
                "frequency": int(row["frequency"]),
                "monetary": float(row["monetary"]),
                "recency_days": int(row["recency_days"]),
            }
        )

    return {
        "customer_id": customer_id,
        "top_preferences": top_preferences,
    }


if __name__ == "__main__":
    sample_input = {
        "recency_days": 39,
        "frequency_orders": 5,
        "monetary_total": 2790.86,
        "total_items": 1590,
        "unique_products": 82,
        "avg_order_value": 558.172,
    }

    print("=== Customer Profile Prediction ===")
    print(predict_customer_profile(sample_input))

    print("\n=== Customer Preferences ===")
    print(get_customer_preferences(customer_id=12347, top_n=5))