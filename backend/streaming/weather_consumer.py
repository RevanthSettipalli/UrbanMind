from kafka import KafkaConsumer
import json
import pandas as pd
import os
from pathlib import Path


# ==========================
# PATH
# ==========================

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT / "data" / "weather_history.csv"


# ==========================
# KAFKA
# ==========================

consumer = KafkaConsumer(

    "weather",

    bootstrap_servers="urbanmind-kafka:9092",

    auto_offset_reset="latest",

    value_deserializer=lambda x:
    json.loads(
        x.decode("utf-8")
    )
)

print("Consumer Started")


# ==========================
# CREATE CSV
# ==========================

if not CSV.exists():

    pd.DataFrame(

        columns=[

            "time",

            "city",

            "temperature",

            "humidity"

        ]

    ).to_csv(

        CSV,

        index=False

    )


# ==========================
# CONSUME
# ==========================

for message in consumer:

    try:

        data = message.value

        row = pd.DataFrame([{

            "time":
            data.get(
                "timestamp"
            ),

            "city":
            data.get(
                "city",
                "Unknown"
            ),

            "temperature":
            data.get(
                "temperature"
            ),

            "humidity":
            data.get(
                "humidity"
            )

        }])

        row.to_csv(

            CSV,

            mode="a",

            header=False,

            index=False

        )

        print("\nWeather Received")
        print(
            f"City: {data.get('city')}"
        )

        print(
            f"Temp: {data.get('temperature')}°C"
        )

        print(
            f"Humidity: {data.get('humidity')}%"
        )

        print(
            f"Saved → {CSV}"
        )

    except Exception as e:

        print(
            f"Error: {e}"
        )