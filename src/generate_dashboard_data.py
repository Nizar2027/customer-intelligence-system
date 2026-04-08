import os
import json
import joblib
import pandas as pd

from src.predict import (
    CHURN_MODEL_PATH,
    CHURN_THRESHOLD_PATH,
    CHURN_FEATURES_PATH,
    REVENUE_MODEL_PATH,
    REVENUE_FEATURES_PATH,
    PREFERENCES_PATH,
    load_json_file,
)
from src.business_rules import (
    assign_customer_segment,
    classify_churn_risk,
    classify_preference_strength,
    classify_revenue_segment,
    clean_revenue
)
from src.data_validation import validate_prediction_input

# =========================
# 1) Paths
# =========================
FEATURES_PATH = "data/processed/normal_dataset.csv"
OUTPUT_DIR = "data/powerbi"

CUSTOMER_INSIGHTS_PATH = os.path.join(OUTPUT_DIR, "customer_insights.csv")
CUSTOMER_PREFERENCES_PATH = os.path.join(OUTPUT_DIR, "customer_preferences_dashboard.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# 2) Load source data
# =========================
df = pd.read_csv(FEATURES_PATH)

feature_cols = [
    "recency_days",
    "frequency_orders",
    "monetary_total",
    "total_items",
    "unique_products",
    "avg_order_value",
]

required_cols = ["CustomerID"] + feature_cols
df = df[required_cols].dropna().drop_duplicates()

print(f"Total customers found: {len(df)}")

# =========================
# 3) Load artifacts ONCE
# =========================
print("Loading models and artifacts once...")

churn_model = joblib.load(CHURN_MODEL_PATH)
churn_threshold = float(load_json_file(CHURN_THRESHOLD_PATH)["threshold"])
churn_feature_names = load_json_file(CHURN_FEATURES_PATH)

revenue_model = joblib.load(REVENUE_MODEL_PATH)
revenue_feature_names = load_json_file(REVENUE_FEATURES_PATH)

pref_df = pd.read_csv(PREFERENCES_PATH)

print("Artifacts loaded successfully.")

# =========================
# 4) Generate outputs
# =========================
customer_results = []
preferences_results = []

for i, row in df.iterrows():
    customer_id = row["CustomerID"]
    input_data = row[feature_cols].to_dict()

    try:
        # ----- Churn prediction -----
        churn_input_df = pd.DataFrame([input_data])
        churn_input_df = validate_prediction_input(churn_input_df, churn_feature_names)

        churn_probability = float(churn_model.predict_proba(churn_input_df)[0, 1])
        churn_prediction = int(churn_probability >= churn_threshold)
        churn_risk = classify_churn_risk(churn_probability)

        # ----- Revenue prediction -----
        revenue_input_df = pd.DataFrame([input_data])
        revenue_input_df = validate_prediction_input(revenue_input_df, revenue_feature_names)

        predicted_revenue = float(revenue_model.predict(revenue_input_df)[0])
        predicted_revenue = clean_revenue(predicted_revenue)
        revenue_segment = classify_revenue_segment(predicted_revenue)

        # ----- Final segment -----
        customer_segment = assign_customer_segment(
            churn_probability=churn_probability,
            predicted_revenue=predicted_revenue,
        )

        customer_results.append({
            "CustomerID": customer_id,
            "churn_probability": churn_probability,
            "churn_prediction": churn_prediction,
            "threshold": churn_threshold,
            "churn_risk": churn_risk,
            "predicted_revenue": predicted_revenue,
            "revenue_segment": revenue_segment,
            "customer_segment": customer_segment,
        })

        # ----- Preferences -----
        customer_pref = pref_df[pref_df["CustomerID"] == customer_id].copy()

        if not customer_pref.empty:
            customer_pref = customer_pref.sort_values(
                "preference_score",
                ascending=False
            ).head(5)

            for _, pref_row in customer_pref.iterrows():
                preferences_results.append({
                    "CustomerID": customer_id,
                    "description": pref_row["Description"],
                    "preference_score": float(pref_row["preference_score"]),
                    "preference_strength": classify_preference_strength(
                        float(pref_row["preference_score"])
                    ),
                    "frequency": int(pref_row["frequency"]),
                    "monetary": float(pref_row["monetary"]),
                    "recency_days": int(pref_row["recency_days"]),
                })

        if (i + 1) % 250 == 0:
            print(f"Processed {i + 1} customers...")

    except Exception as e:
        print(f"[Error] Row {i}, CustomerID {customer_id}: {e}")

# =========================
# 5) Save outputs
# =========================
customer_insights_df = pd.DataFrame(customer_results)
customer_preferences_df = pd.DataFrame(preferences_results)

# -------- Force clean dtypes --------
if not customer_insights_df.empty:
    customer_insights_df["CustomerID"] = customer_insights_df["CustomerID"].astype("int64")
    customer_insights_df["churn_probability"] = customer_insights_df["churn_probability"].astype("float64")
    customer_insights_df["churn_prediction"] = customer_insights_df["churn_prediction"].astype("int64")
    customer_insights_df["threshold"] = customer_insights_df["threshold"].astype("float64")
    customer_insights_df["predicted_revenue"] = customer_insights_df["predicted_revenue"].astype("float64")

    # Round numeric columns for Power BI friendliness
    customer_insights_df["churn_probability"] = customer_insights_df["churn_probability"].round(6)
    customer_insights_df["threshold"] = customer_insights_df["threshold"].round(6)
    customer_insights_df["predicted_revenue"] = customer_insights_df["predicted_revenue"].round(2)

if not customer_preferences_df.empty:
    customer_preferences_df["CustomerID"] = customer_preferences_df["CustomerID"].astype("int64")
    customer_preferences_df["preference_score"] = customer_preferences_df["preference_score"].astype("float64")
    customer_preferences_df["frequency"] = customer_preferences_df["frequency"].astype("int64")
    customer_preferences_df["monetary"] = customer_preferences_df["monetary"].astype("float64")
    customer_preferences_df["recency_days"] = customer_preferences_df["recency_days"].astype("int64")

    # Round numeric columns for Power BI friendliness
    customer_preferences_df["preference_score"] = customer_preferences_df["preference_score"].round(6)
    customer_preferences_df["monetary"] = customer_preferences_df["monetary"].round(2)

# -------- Save with explicit decimal point --------
customer_insights_df.to_csv(
    CUSTOMER_INSIGHTS_PATH,
    index=False,
    encoding="utf-8-sig",
    float_format="%.6f"
)

customer_preferences_df.to_csv(
    CUSTOMER_PREFERENCES_PATH,
    index=False,
    encoding="utf-8-sig",
    float_format="%.6f"
)

print("Dashboard files created successfully!")
print(f"Saved: {CUSTOMER_INSIGHTS_PATH}")
print(f"Saved: {CUSTOMER_PREFERENCES_PATH}")