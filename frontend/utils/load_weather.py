import pandas as pd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT / "data" / "processed_weather.csv"


def load_weather():

    try:

        df = pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

    except Exception as e:

        print(f"CSV Load Error: {e}")

        return pd.DataFrame()


    # Empty protection
    if df.empty:
        return df


    # Normalize columns
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )


    # Required columns
    defaults = {
        "city": "Unknown",
        "temperature": 0,
        "humidity": 0
    }


    for col, value in defaults.items():

        if col not in df.columns:

            df[col] = value


    # Numeric conversion
    numeric_cols = [
        "temperature",
        "humidity"
    ]


    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)


    # Safe datetime conversion
    if "time" in df.columns:

        df["time"] = pd.to_datetime(
            df["time"],
            errors="coerce"
        )


    # Remove completely empty rows
    df = df.dropna(
        how="all"
    )


    return df
