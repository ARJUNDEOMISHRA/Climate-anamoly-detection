
# ============================================================
# forecast.py — Linear Regression with 95% Confidence Bands
# ============================================================
import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_temperature(df, days: int = 14):
    """
    Returns (predictions, lower_bound, upper_bound) arrays for `days` future days.
    Falls back to ([], [], []) if data is insufficient.
    """
    df = df.dropna(subset=["temperature"])
    if len(df) < 10:
        return [], [], []

    df = df.copy()
    df["day"] = range(len(df))
    X = df[["day"]].values
    y = df["temperature"].values

    model = LinearRegression()
    model.fit(X, y)

    residuals = y - model.predict(X)
    resid_std = np.std(residuals)

    future_X   = np.arange(len(df), len(df) + days).reshape(-1, 1)
    preds      = model.predict(future_X)
    lower      = preds - 1.96 * resid_std
    upper      = preds + 1.96 * resid_std

    return preds, lower, upper