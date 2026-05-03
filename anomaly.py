
# ============================================================
# anomaly.py — Upgraded: IsolationForest + Z-score + Type + Severity
# ============================================================
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np


def classify_anomaly_type(z_temp: float, z_precip: float, is_anomaly: bool) -> str:
    if not is_anomaly:
        return "NORMAL"
    abs_t = abs(z_temp)
    abs_p = abs(z_precip)
    if abs_t >= abs_p:
        if z_temp > 2.0:
            return "HEAT_WAVE"
        elif z_temp < -2.0:
            return "COLD_SNAP"
    else:
        if z_precip > 2.0:
            return "EXTREME_RAIN"
        elif z_precip < -1.5 and z_temp > 0:
            return "DROUGHT"
    return "COMPOUND"


def calculate_severity(z_temp: float, z_precip: float, is_anomaly: bool) -> int:
    if not is_anomaly:
        return 0
    max_z = max(abs(z_temp), abs(z_precip))
    return min(100, int((max_z / 4.5) * 100))


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if len(df) < 10:
        df["z_temp"]       = 0.0
        df["z_precip"]     = 0.0
        df["anomaly"]      = 1
        df["anomaly_type"] = "NORMAL"
        df["severity"]     = 0
        return df

    # Z-scores (per full dataset — single city pipeline)
    t_std = df["temperature"].std()
    p_std = df["precipitation"].std()
    df["z_temp"]   = (df["temperature"]   - df["temperature"].mean())   / (t_std   if t_std   > 0 else 1)
    df["z_precip"] = (df["precipitation"] - df["precipitation"].mean()) / (p_std if p_std > 0 else 1)

    # IsolationForest
    features       = df[["temperature", "precipitation"]].fillna(0)
    model          = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"]  = model.fit_predict(features)

    # Type & severity
    df["anomaly_type"] = df.apply(
        lambda r: classify_anomaly_type(r["z_temp"], r["z_precip"], r["anomaly"] == -1), axis=1
    )
    df["severity"] = df.apply(
        lambda r: calculate_severity(r["z_temp"], r["z_precip"], r["anomaly"] == -1), axis=1
    )

    return df