from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
TARGET_COLUMN = "future_revenue"


def build_final_linear_model() -> Pipeline:
    lin_reg = Pipeline([
        ("scaler", StandardScaler()),
        ("lr", LinearRegression())
    ])
    return lin_reg


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "processed" / "revenue_dataset.csv"
    models_dir = project_root / "models"
    reports_dir = project_root / "reports"

    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    print("Loading revenue dataset...")
    df = pd.read_csv(data_path)

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    feature_names = X.columns.tolist()

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )


    print("Building final linear regression model...")
    lin_reg = build_final_linear_model()

    print("Running cross-validation on training set...")
    cv_scores = cross_val_score(
        lin_reg,
        X_train,
        y_train,
        cv=5,
        scoring="neg_root_mean_squared_error"
    )
    cv_rmse_scores = -cv_scores

    cv_metrics = {
        "cv_rmse_scores": cv_rmse_scores.tolist(),
        "cv_rmse_mean": float(np.mean(cv_rmse_scores)),
        "cv_rmse_std": float(np.std(cv_rmse_scores)),
        "cv_rmse_min": float(np.min(cv_rmse_scores)),
        "cv_rmse_max": float(np.max(cv_rmse_scores)),
    }

    print(
        f"CV RMSE -> Mean: {cv_metrics['cv_rmse_mean']:.4f}, "
        f"Std: {cv_metrics['cv_rmse_std']:.4f}"
    )

    print("Fitting final model on full training set...")
    lin_reg.fit(X_train, y_train)

    print("Evaluating on test set...")
    y_test_pred = lin_reg.predict(X_test)
    test_rmse = float(np.sqrt(mean_squared_error(y_test, y_test_pred)))
    test_mae = float(mean_absolute_error(y_test, y_test_pred))

    test_metrics = {
        "test_rmse": test_rmse,
        "test_mae": test_mae,
    }

    print("=== Final Test Metrics ===")
    for key, value in test_metrics.items():
        print(f"{key}: {value}")

    linear_model = lin_reg.named_steps["lr"]
    coefficients = linear_model.coef_

    coefficients_output = [
        {
            "feature": feature,
            "coefficient": float(coef)
        }
        for feature, coef in zip(feature_names, coefficients)
    ]

    model_output_path = models_dir / "revenue_linear_model.joblib"
    metrics_output_path = reports_dir / "revenue_test_metrics.json"
    cv_metrics_output_path = reports_dir / "revenue_cv_metrics.json"
    features_output_path = models_dir / "revenue_features.json"
    coefficients_output_path = reports_dir / "revenue_coefficients.json"

    print("Saving model and artifacts...")
    joblib.dump(lin_reg, model_output_path)

    with open(metrics_output_path, "w", encoding="utf-8") as f:
        json.dump(test_metrics, f, indent=2)

    with open(cv_metrics_output_path, "w", encoding="utf-8") as f:
        json.dump(cv_metrics, f, indent=2)

    with open(features_output_path, "w", encoding="utf-8") as f:
        json.dump(feature_names, f, indent=2)

    with open(coefficients_output_path, "w", encoding="utf-8") as f:
        json.dump(coefficients_output, f, indent=2)

    print("Done.")
    print(f"Model saved to: {model_output_path}")
    print(f"Test metrics saved to: {metrics_output_path}")
    print(f"CV metrics saved to: {cv_metrics_output_path}")
    print(f"Features saved to: {features_output_path}")
    print(f"Coefficients saved to: {coefficients_output_path}")


if __name__ == "__main__":
    main()