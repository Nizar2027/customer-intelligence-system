
from fastapi import APIRouter, HTTPException
from api.schemas import CustomerFeatures, PredictionResponse
from api.services import run_prediction_service

router = APIRouter(prefix="/predict", tags=["Predictions"])


@router.post("/", response_model=PredictionResponse)
def predict_customer(features: CustomerFeatures):
    try:
        result = run_prediction_service(features.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")