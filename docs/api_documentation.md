# API Documentation

## Overview

The Customer Intelligence API provides endpoints for:

- Customer prediction (churn & revenue)
- Customer preference retrieval
- System health monitoring

The API is built using FastAPI and serves as the backend layer for model inference and business logic.

---

## Base URL

http://127.0.0.1:8000

---

## 1. Root Endpoint

### GET /

Description: Check if the API is running.

Response:
```json
{
  "message": "Customer Intelligence API is running"
}
```

---

## 2. Health Check

### GET /health

Description: Verify system health.

Response:
```json
{
  "status": "ok"
}
```

---

## 3. Customer Prediction

### POST /predict/

Description: Generate predictions for a single customer.

Request Body:
```json
{
  "recency_days": 30,
  "frequency_orders": 5,
  "monetary_total": 250.0,
  "total_items": 20,
  "unique_products": 8,
  "avg_order_value": 50.0
}
```

Response:
```json
{
  "churn_probability": 0.72,
  "churn_risk": "High Risk",
  "predicted_revenue": 850.0,
  "revenue_segment": "Medium Value",
  "customer_segment": "At-Risk Customer"
}
```

---

## 4. Customer Preferences

### GET /preferences/

Description: Retrieve top preferred products for a specific customer.

Query Parameters:

- customer_id (float): Customer ID
- top_n (int): Number of top products (default = 5)

Example:
```
/preferences/?customer_id=12352&top_n=5
```

Response:
```json
{
  "customer_id": 12352,
  "top_preferences": [
    {
      "description": "PINK HEART SHAPE EGG FRYING PAN",
      "preference_score": 0.74,
      "frequency": 3,
      "monetary": 59.4,
      "preference_strength": "Strong"
    }
  ]
}
```

---

## 5. API Structure

```
api/
├── main.py
├── routers/
│   ├── health.py
│   ├── predictions.py
│   ├── preferences.py
├── services.py
├── schemas.py
```

---

## 6. Technologies Used

- FastAPI
- Pydantic
- Scikit-learn
- Joblib

---

## 7. Error Handling

All endpoints return HTTP 500 on failure.

```json
{
  "detail": "Error message"
}
```

---

## 8. Running the API

```bash
uvicorn api.main:app --reload
```

---

## 9. Notes

- Designed for local development
- Power BI uses precomputed outputs
- API is modular and extendable

---

## 10. Future Improvements

- Batch prediction endpoint
- Authentication
- Cloud deployment
- Real-time integration