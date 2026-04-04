
from fastapi import APIRouter, HTTPException, Query
from api.schemas import PreferencesResponse
from api.services import run_preferences_service

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.get("/", response_model=PreferencesResponse)
def get_preferences(
    customer_id: float = Query(..., description="Customer ID"),
    top_n: int = Query(5, ge=1, le=20, description="Number of top preferences to return")
):
    try:
        result = run_preferences_service(customer_id=customer_id, top_n=top_n)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preference retrieval failed: {str(e)}")