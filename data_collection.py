
# ============================================================
# data_collection.py — Open-Meteo API + Indian Cities + Fallback
# ============================================================
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta

INDIAN_CITIES = {
    "🌸 Bhopal":     {"lat": 23.26, "lon": 77.41, "state": "Madhya Pradesh"},
    "🏛️ Delhi":      {"lat": 28.61, "lon": 77.20, "state": "Delhi"},
    "🌊 Mumbai":     {"lat": 19.07, "lon": 72.87, "state": "Maharashtra"},
    "🏖️ Chennai":    {"lat": 13.08, "lon": 80.27, "state": "Tamil Nadu"},
    "🌺 Kolkata":    {"lat": 22.57, "lon": 88.36, "state": "West Bengal"},
    "🌆 Bangalore":  {"lat": 12.97, "lon": 77.59, "state": "Karnataka"},
    "💎 Hyderabad":  {"lat": 17.38, "lon": 78.49, "state": "Telangana"},
    "🏰 Jaipur":     {"lat": 26.91, "lon": 75.79, "state": "Rajasthan"},
    "🌊 Ahmedabad":  {"lat": 23.02, "lon": 72.57, "state": "Gujarat"},
    "🌾 Patna":      {"lat": 25.59, "lon": 85.13, "state": "Bihar"},
    "⛰️ Lucknow":    {"lat": 26.85, "lon": 80.95, "state": "Uttar Pradesh"},
    "🍇 Pune":       {"lat": 18.52, "lon": 73.85, "state": "Maharashtra"},
}


def fetch_openmeteo_data(city_key: str, lat: float, lon: float, days: int = 365):
    """Fetch real historical climate data — Open-Meteo Archive API (no key needed)."""
    end_date   = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": start_date, "end_date": end_date,
        "daily": "temperature_2m_mean,precipitation_sum,windspeed_10m_max",
        "timezone": "Asia/Kolkata",
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        d = r.json()["daily"]
        city_name = city_key.split(" ", 1)[-1]          # strip emoji
        df = pd.DataFrame({
            "date":          pd.to_datetime(d["time"]),
            "temperature":   d["temperature_2m_mean"],
            "precipitation": d["precipitation_sum"],
            "wind_speed":    d["windspeed_10m_max"],
            "lat": lat, "lon": lon, "city": city_name,
            "data_source": "🌐 Open-Meteo API (Live)",
        })
        df = df.dropna(subset=["temperature"])
        df["precipitation"] = df["precipitation"].fillna(0)
        df["wind_speed"]    = df["wind_speed"].fillna(0)
        return df
    except Exception:
        return None


def generate_synthetic_data(city_key: str, lat: float, lon: float, days: int = 365):
    """Realistic synthetic fallback (monsoon-aware, latitude-adjusted)."""
    np.random.seed(abs(int(lat * 100)) % 256)
    dates      = pd.date_range(end=datetime.now().date(), periods=days, freq="D")
    doy        = np.array([d.timetuple().tm_yday for d in dates])
    seasonal   = 10 * np.sin((doy - 80) * 2 * np.pi / 365)
    base_temp  = 30 - (lat - 13) * 0.4
    temp       = base_temp + seasonal + np.random.normal(0, 2.5, days)
    monsoon    = np.where((doy > 150) & (doy < 280), 8, 1).astype(float)
    precip     = np.random.exponential(monsoon, days)
    wind       = np.abs(np.random.normal(12, 5, days))
    city_name  = city_key.split(" ", 1)[-1]
    return pd.DataFrame({
        "date": dates, "temperature": temp, "precipitation": precip,
        "wind_speed": wind, "lat": lat, "lon": lon, "city": city_name,
        "data_source": "🧪 Synthetic (API unavailable)",
    })


def collect_city_data(city_key: str = "🌸 Bhopal") -> pd.DataFrame:
    info = INDIAN_CITIES.get(city_key, INDIAN_CITIES["🌸 Bhopal"])
    lat, lon = info["lat"], info["lon"]
    df = fetch_openmeteo_data(city_key, lat, lon)
    if df is None or len(df) < 30:
        df = generate_synthetic_data(city_key, lat, lon)
    return df


# Backward compatibility
def collect_multi_location_data() -> pd.DataFrame:
    return collect_city_data("🌸 Bhopal")