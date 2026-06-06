import json
import pandas as pd
from pathlib import Path

RAW = "data/raw/weather.json"

OUTPUT = "data/processed/weather_clean.csv"

with open(RAW, "r") as f:
    data = json.load(f)

current = data["current"]

clean = {
    "time": current["time"],
    "temperature": current["temperature_2m"],
    "humidity": current["relative_humidity_2m"],
    "fetched_at": data["fetched_at"]
}

df = pd.DataFrame([clean])

Path(
    "data/processed"
).mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT,
    index=False
)

print(df)

print("\nProcessed dataset created")