
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
    StackingClassifier,
    VotingClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_val_predict, train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


RANDOM_STATE = 42
TARGET_COLUMN = "churn_label"
DESIRED_RECALL = 0.70


def build_final_stacking_model():

    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    log_reg = Pipeline([
        ("scaler", StandardScaler()),
        ("lr", LogisticRegression(max_iter=1000, random_state=42))
    ])

    svc = Pipeline([
        ("scaler", StandardScaler()),
        ("svc", SVC(probability=True, random_state=42))
    ])

    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    stack_clf = StackingClassifier(
        estimators=[
            ("lr", log_reg),
            ("rf", rf),
            ("svc", svc),
        ],
        final_estimator=LogisticRegression(max_iter=1000, random_state=42),
        cv=5
    )

    return stack_clf


def find_threshold_for_target_recall(
    y_true: pd.Series | np.ndarray,
    y_scores: np.ndarray,
    target_recall: float = DESIRED_RECALL,
) -> tuple[float, float, float, float]:
    """
    Find the threshold that achieves at least the target recall
    while keeping the threshold as high as possible.
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_scores)

    valid_idx = np.where(recalls >= target_recall)[0]
    if len(valid_idx) == 0:
        # fallback: use default threshold if target recall is not reachable
        threshold = 0.5
        y_pred = (y_scores >= threshold).astype(int)
        return (
            threshold,
            precision_score(y_true, y_pred),
            recall_score(y_true, y_pred),
            f1_score(y_true, y_pred),
        )

    # pick the last valid index to keep threshold as high as possible
    idx_recall = valid_idx[-1]

    # thresholds has length = len(recalls) - 1, so protect edge case
    if idx_recall >= len(thresholds):
        idx_recall = len(thresholds) - 1

    threshold = float(thresholds[idx_recall])
    y_pred = (y_scores >= threshold).astype(int)

    return (
        threshold,
        precision_score(y_true, y_pred),
        recall_score(y_true, y_pred),
        f1_score(y_true, y_pred),
    )


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "processed" / "churn_dataset.csv"
    models_dir = project_root / "models"
    reports_dir = project_root / "reports"

    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    print("Loading churn dataset...")
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

    print("Building final stacking model...")
    stack_clf = build_final_stacking_model()

    print("Generating cross-validated probabilities on training set...")
    y_train_scores = cross_val_predict(
        stack_clf,
        X_train,
        y_train,
        cv=5,
        method="predict_proba",
    )[:, 1]

    print("Selecting threshold based on target recall...")
    (
        threshold,
        train_precision_tuned,
        train_recall_tuned,
        train_f1_tuned,
    ) = find_threshold_for_target_recall(
        y_true=y_train,
        y_scores=y_train_scores,
        target_recall=DESIRED_RECALL,
    )

    print(f"Selected threshold: {threshold:.6f}")
    print(
        f"Train tuned metrics -> Precision: {train_precision_tuned:.4f}, "
        f"Recall: {train_recall_tuned:.4f}, F1: {train_f1_tuned:.4f}"
    )

    print("Fitting final model on full training set...")
    stack_clf.fit(X_train, y_train)

    print("Evaluating on test set...")
    y_test_scores = stack_clf.predict_proba(X_test)[:, 1]
    y_test_pred = (y_test_scores >= threshold).astype(int)

    test_metrics = {
        "accuracy": float(accuracy_score(y_test, y_test_pred)),
        "precision": float(precision_score(y_test, y_test_pred)),
        "recall": float(recall_score(y_test, y_test_pred)),
        "f1": float(f1_score(y_test, y_test_pred)),
        "confusion_matrix": confusion_matrix(y_test, y_test_pred).tolist(),
    }

    print("=== Final Test Metrics ===")
    for key, value in test_metrics.items():
        print(f"{key}: {value}")

    model_output_path = models_dir / "churn_stacking_model.joblib"
    threshold_output_path = models_dir / "churn_threshold.json"
    metrics_output_path = reports_dir / "churn_test_metrics.json"
    features_output_path = models_dir / "churn_features.json"

    print("Saving model and artifacts...")
    joblib.dump(stack_clf, model_output_path)

    with open(threshold_output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "threshold": threshold,
                "target_recall": DESIRED_RECALL,
                "train_precision_tuned": train_precision_tuned,
                "train_recall_tuned": train_recall_tuned,
                "train_f1_tuned": train_f1_tuned,
            },
            f,
            indent=2,
        )

    with open(metrics_output_path, "w", encoding="utf-8") as f:
        json.dump(test_metrics, f, indent=2)

    with open(features_output_path, "w", encoding="utf-8") as f:
        json.dump(feature_names, f, indent=2)

    print("Done.")
    print(f"Model saved to: {model_output_path}")
    print(f"Threshold saved to: {threshold_output_path}")
    print(f"Metrics saved to: {metrics_output_path}")
    print(f"Features saved to: {features_output_path}")


if __name__ == "__main__":
    main()