
from __future__ import annotations

from typing import Iterable

import pandas as pd


def validate_required_features(
    input_df: pd.DataFrame,
    required_features: Iterable[str]
) -> None:
    """
    Ensure all required features exist in the input data.
    """
    missing_features = [
        feature for feature in required_features
        if feature not in input_df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )


def validate_no_missing_values(input_df: pd.DataFrame) -> None:
    """
    Ensure the input data contains no missing values.
    """
    missing_columns = input_df.columns[input_df.isnull().any()].tolist()

    if missing_columns:
        raise ValueError(
            f"Missing values found in columns: {missing_columns}"
        )


def validate_numeric_features(
    input_df: pd.DataFrame,
    feature_names: Iterable[str]
) -> None:
    """
    Ensure the required feature columns are numeric.
    """
    non_numeric_features = [
        feature for feature in feature_names
        if not pd.api.types.is_numeric_dtype(input_df[feature])
    ]

    if non_numeric_features:
        raise ValueError(
            f"Non-numeric features found: {non_numeric_features}"
        )


def validate_prediction_input(
    input_df: pd.DataFrame,
    required_features: Iterable[str]
) -> pd.DataFrame:
    """
    Full validation pipeline for prediction input:
    1. Check required features
    2. Check missing values
    3. Check numeric types
    4. Return reordered DataFrame
    """
    validate_required_features(input_df, required_features)
    validate_no_missing_values(input_df[required_features])
    validate_numeric_features(input_df, required_features)

    return input_df[list(required_features)].copy()