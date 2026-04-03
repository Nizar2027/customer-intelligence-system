
from __future__ import annotations


def classify_churn_risk(churn_probability: float) -> str:
    if churn_probability >= 0.80:
        return "High Risk"
    if churn_probability >= 0.50:
        return "Medium Risk"
    return "Low Risk"


def classify_revenue_segment(predicted_revenue: float) -> str:
    if predicted_revenue >= 3000:
        return "High Value"
    if predicted_revenue >= 1000:
        return "Medium Value"
    return "Low Value"


def assign_customer_segment(
    churn_probability: float,
    predicted_revenue: float
) -> str:
    churn_risk = classify_churn_risk(churn_probability)
    revenue_segment = classify_revenue_segment(predicted_revenue)

    if churn_risk == "High Risk" and revenue_segment == "High Value":
        return "Critical Retention Target"

    if churn_risk == "High Risk":
        return "At-Risk Customer"

    if churn_risk == "Low Risk" and revenue_segment == "High Value":
        return "Loyal High-Value Customer"

    return "Standard Customer"


def classify_preference_strength(score: float) -> str:
    """
    Classify preference score strength.
    """
    if score >= 0.8:
        return "Strong Preference"
    if score >= 0.5:
        return "Moderate Preference"
    return "Weak Preference"