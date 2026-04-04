
from src.predict import predict_customer_profile, get_customer_preferences


def run_prediction_service(features: dict) -> dict:
    """
    Run full customer profile prediction using the existing project logic.
    """
    return predict_customer_profile(features)


def run_preferences_service(customer_id: int | float, top_n: int = 5) -> dict:
    """
    Retrieve customer top preferences using the existing project logic.
    """
    return get_customer_preferences(customer_id=customer_id, top_n=top_n)