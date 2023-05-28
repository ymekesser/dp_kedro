from typing import Tuple
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline as sklPipeline
import sklearn.metrics as metrics


def select_data():
    pass


def split_data(feature_set: pd.DataFrame) -> Tuple:
    X = feature_set[
        [
            "storey_median",
            "floor_area_sqm",
            "lease_commence_date",
            "remaining_lease_in_months",
            "distance_to_closest_mrt",
            "distance_to_closest_mall",
            "distance_to_cbd",
        ]
    ].to_numpy()
    y = feature_set[["resale_price"]].to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, random_state=1337, test_size=0.25
    )

    return X_train, X_test, y_train, y_test


def train_model(X_train: np.ndarray, y_train: np.ndarray) -> sklPipeline:
    pipe = sklPipeline(
        [("scaler", StandardScaler()), ("linreg", RandomForestRegressor())]
    )

    pipe.fit(X_train, y_train.ravel())

    return pipe


def evaluate_model(
    model: RandomForestRegressor,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> pd.DataFrame:
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    df_metrics = pd.DataFrame()

    df_metrics["r2_train"] = [metrics.r2_score(y_train, y_train_pred)]
    df_metrics["r2_test"] = [metrics.r2_score(y_test, y_test_pred)]
    df_metrics["MAE"] = [metrics.mean_absolute_error(y_test, y_test_pred)]
    df_metrics["MSE"] = [metrics.mean_squared_error(y_test, y_test_pred)]
    df_metrics["RMSE"] = [np.sqrt(metrics.mean_squared_error(y_test, y_test_pred))]
    mape = np.mean(np.abs((y_test - y_test_pred) / np.abs(y_test)))
    df_metrics["MAPE"] = [round(mape * 100, 2)]
    df_metrics["Accuracy"] = [round(100 * (1 - mape), 2)]

    _print_metrics(df_metrics)

    return df_metrics


def _print_metrics(df_metrics: pd.DataFrame):
    formatted_metrics = f"""Result Metrics:
R^2 Score on Training:{df_metrics["r2_train"]}
R^2 Score on Test:{df_metrics["r2_test"]}

Mean Absolute Error (MAE): {df_metrics["MAE"]}
Mean Squared Error (MSE): {df_metrics["MSE"]}
Root Mean Squared Error (RMSE): {df_metrics["RMSE"]}

Mean Absolute Percentage Error (MAPE): {df_metrics["MAPE"]}
Accuracy: {df_metrics["Accuracy"]}
    """

    print(formatted_metrics)
