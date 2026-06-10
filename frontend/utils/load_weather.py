import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "processed_weather.csv"


def load_weather():
    try:
        print(f"LOOKING FOR CSV: {CSV}")
        print(f"CSV EXISTS: {CSV.exists()}")
        if not CSV.exists():
            print("processed_weather.csv not found")
            return pd.DataFrame()

        df = pd.read_csv(CSV)
        print(f"ROWS LOADED: {len(df)}")
        print(f"COLUMNS: {list(df.columns)}")

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

        print(f"FINAL ROWS: {len(df)}")
        return df

    except Exception as e:
        print(f"LOAD_WEATHER ERROR: {e}")
        raise
