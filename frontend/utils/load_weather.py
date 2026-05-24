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

    except:

        return pd.DataFrame()


    df.columns = [

        str(c)
        .strip()
        .lower()

        for c in df.columns
    ]


    if "city" not in df.columns:

        df["city"] = "Unknown"


    for col in [

        "temperature",

        "humidity"

    ]:

        if col not in df.columns:

            df[col] = 0


    df["temperature"] = pd.to_numeric(
        df["temperature"],
        errors="coerce"
    )

    df["humidity"] = pd.to_numeric(
        df["humidity"],
        errors="coerce"
    )

    try:

        df["time"] = pd.to_datetime(
            df["time"]
        )

    except:
        pass


    return df.dropna()
