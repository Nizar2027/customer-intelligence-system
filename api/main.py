
from fastapi import FastAPI
from api.routers.health import router as health_router
from api.routers.predictions import router as predictions_router
from api.routers.preferences import router as preferences_router

app = FastAPI(
    title="Customer Intelligence API",
    description="API for churn prediction, revenue forecasting, and customer preference analysis",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Customer Intelligence API is running"
    }


app.include_router(health_router)
app.include_router(predictions_router)
app.include_router(preferences_router)