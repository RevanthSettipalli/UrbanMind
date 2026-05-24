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

    # Stop if empty
    if df.empty:
        return df

    # Clean column names
    df.columns = [
        str(c).strip().lower()
        for c in df.columns
    ]

    # Create required columns if missing
    required = [
        "city",
        "temperature",
        "humidity"
    ]

    for col in required:

        if col not in df.columns:

            if col == "city":
                df[col] = "Unknown"

            else:
                df[col] = 0

    # Convert numeric safely
    df["temperature"] = pd.to_numeric(
        df["temperature"],
        errors="coerce"
    ).fillna(0)

    df["humidity"] = pd.to_numeric(
        df["humidity"],
        errors="coerce"
    ).fillna(0)

    # Parse time safely
    if "time" in df.columns:

        try:

            df["time"] = pd.to_datetime(
                df["time"],
                errors="coerce",
                infer_datetime_format=True
            )

        except Exception:
            pass

    # Remove only fully empty rows
    df = df.dropna(
        how="all"
    )

    return df
