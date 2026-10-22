"""Preprocessing, training, and prediction for the cost estimator model."""

import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

REGION_CATEGORIES = ["northeast", "northwest", "southeast", "southwest"]


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    encoded = df.copy()
    encoded["smoker"] = encoded["smoker"].map({"yes": 1, "no": 0})
    encoded["sex"] = encoded["sex"].map({"male": 1, "female": 0})
    encoded = pd.get_dummies(encoded, columns=["region"], drop_first=True)
    return encoded


@st.cache_resource
def train_model(df: pd.DataFrame) -> dict:
    encoded = encode_features(df)
    X = encoded.drop(columns=["charges"])
    y = encoded["charges"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    coefficients = pd.DataFrame({"feature": X.columns, "weight": model.coef_})

    return {
        "model": model,
        "feature_columns": list(X.columns),
        "X_test": X_test,
        "y_test": y_test,
        "predictions": predictions,
        "r2": r2_score(y_test, predictions),
        "mae": mean_absolute_error(y_test, predictions),
        "coefficients": coefficients,
    }


def predict_charges(
    model: LinearRegression,
    feature_columns: list[str],
    age: int,
    sex: str,
    bmi: float,
    children: int,
    smoker: str,
    region: str,
) -> float:
    row = {col: 0 for col in feature_columns}
    row["age"] = age
    row["bmi"] = bmi
    row["children"] = children
    row["sex"] = 1 if sex == "male" else 0
    row["smoker"] = 1 if smoker == "yes" else 0

    dummy_col = f"region_{region}"
    if dummy_col in row:
        row[dummy_col] = 1

    input_df = pd.DataFrame([row])[feature_columns]
    return float(model.predict(input_df)[0])


if __name__ == "__main__":
    from data_loader import get_clean_data

    clean = get_clean_data()
    result = train_model(clean)

    print(f"R-squared: {result['r2']:.4f}")
    print(f"MAE: ${result['mae']:.2f}")
    print("\n--- Coefficients ---")
    print(result["coefficients"].sort_values(by="weight", ascending=False))

    sample_pred = predict_charges(
        result["model"],
        result["feature_columns"],
        age=19,
        sex="female",
        bmi=27.9,
        children=0,
        smoker="yes",
        region="southwest",
    )
    print(f"\nSample prediction (first row of dataset): ${sample_pred:.2f}")
