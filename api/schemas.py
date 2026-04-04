
from pydantic import BaseModel, Field
from typing import List


class CustomerFeatures(BaseModel):
    recency_days: float = Field(..., ge=0, description="Days since last purchase")
    frequency_orders: float = Field(..., ge=0, description="Number of unique orders")
    monetary_total: float = Field(..., ge=0, description="Total amount spent")
    total_items: float = Field(..., ge=0, description="Total number of purchased items")
    unique_products: float = Field(..., ge=0, description="Number of unique products purchased")
    avg_order_value: float = Field(..., ge=0, description="Average order value")


class PredictionResponse(BaseModel):
    churn_probability: float
    churn_prediction: int
    threshold: float
    churn_risk: str
    predicted_revenue: float
    revenue_segment: str
    customer_segment: str


class PreferenceItem(BaseModel):
    description: str
    preference_score: float
    preference_strength: str
    frequency: int
    monetary: float
    recency_days: int


class PreferencesResponse(BaseModel):
    customer_id: float
    top_preferences: List[PreferenceItem]


class HealthResponse(BaseModel):
    status: str
    message: str