import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "processed_weather.csv"


def load_weather():
    try:
        if not CSV.exists():
            return pd.DataFrame()

        df = pd.read_csv(CSV)

        if df.empty:
            return df

        # Required columns
        required_defaults = {
            "city": "Unknown",
            "temperature": 0,
            "humidity": 0,
            "aqi": 0,
            "pm25": 0,
            "pm10": 0,
            "co": 0,
            "no2": 0,
        }

        for col, default in required_defaults.items():
            if col not in df.columns:
                df[col] = default

        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"], errors="coerce")

        for col in ["temperature", "humidity", "aqi", "pm25", "pm10", "co", "no2"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        return df

    except Exception:
        return pd.DataFrame()
