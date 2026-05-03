
# ============================================================
# risk_score.py — Composite Risk Score Calculator
# ============================================================
import numpy as np

RISK_COLORS = {
    "CRITICAL": "#FF4B4B",
    "HIGH":     "#FF9000",
    "MODERATE": "#FFD700",
    "LOW":      "#00C851",
    "UNKNOWN":  "#888888",
}
RISK_ICONS = {
    "CRITICAL": "🔴",
    "HIGH":     "🟠",
    "MODERATE": "🟡",
    "LOW":      "🟢",
    "UNKNOWN":  "⚪",
}


def calculate_risk_score(df) -> tuple:
    """
    Composite risk score 0–100:
      Anomaly frequency  → 30%
      Severity magnitude → 40%
      Recent 30-day trend→ 30%
    Returns (score: int, level: str)
    """
    if len(df) == 0:
        return 0, "UNKNOWN"

    anomaly_df = df[df["anomaly"] == -1]
    n_total = len(df)
    n_anom  = len(anomaly_df)

    # Component 1 — frequency (0-100)
    freq_score = min(100, (n_anom / n_total) * 1000)

    # Component 2 — severity (0-100)
    severity_score = float(anomaly_df["severity"].mean()) if n_anom > 0 else 0

    # Component 3 — recent trend (last 30 days)
    df_sorted   = df.sort_values("date")
    recent      = df_sorted.tail(30)
    recent_anom = recent[recent["anomaly"] == -1]
    trend_score = min(100, (len(recent_anom) / max(len(recent), 1)) * 1000)

    composite = round(min(100, 0.30 * freq_score + 0.40 * severity_score + 0.30 * trend_score))

    if composite >= 75:
        level = "CRITICAL"
    elif composite >= 50:
        level = "HIGH"
    elif composite >= 25:
        level = "MODERATE"
    else:
        level = "LOW"

    return composite, level
