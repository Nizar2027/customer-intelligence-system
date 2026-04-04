
from fastapi import APIRouter
from api.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
def health_check():
    return {
        "status": "ok",
        "message": "Customer Intelligence API is running"
    }