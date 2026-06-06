import psycopg2
import json
import time
import pandas as pd

from pathlib import Path
from kafka import KafkaConsumer

BROKER = "urbanmind-kafka:9092"
TOPIC = "weather"

ROOT = Path(__file__).resolve().parents[2]

STREAM = ROOT / "data" / "weather_stream.csv"
PROCESSED = ROOT / "data" / "processed_weather.csv"
HISTORY = ROOT / "data" / "weather_history.csv"

FILES = [
    STREAM,
    PROCESSED,
    HISTORY
]

print("🚀 STARTING CONSUMER")

consumer = None

while consumer is None:

    try:

        consumer = KafkaConsumer(
            TOPIC,

            bootstrap_servers=BROKER,

            auto_offset_reset="earliest",

            group_id="urbanmind",

            enable_auto_commit=True,

            value_deserializer=lambda x:
            json.loads(
                x.decode("utf-8")
            )
        )

        print("✅ CONSUMER CONNECTED")

    except Exception as e:

        print("WAITING FOR KAFKA...")
        print(e)

        time.sleep(5)

print("📡 CONSUMER RUNNING")
db = psycopg2.connect(
    host="urbanmind-postgres",
    database="urbanmind",
    user="admin",
    password="admin123",
    port="5432"
)

cursor = db.cursor()

print("✅ DATABASE CONNECTED")

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    city VARCHAR(100),
    temperature FLOAT,
    humidity INTEGER,
    condition VARCHAR(50)
)
""")

db.commit()

print("✅ TABLE VERIFIED")

for file in FILES:

    file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not file.exists():

        pd.DataFrame(
            columns=[
                "time",
                "city",
                "temperature",
                "humidity",
                "condition",
                "aqi",
                "pm25",
                "pm10",
                "co",
                "no2"
            ]
        ).to_csv(
            file,
            index=False
        )


while True:

    try:

        msg = next(consumer)

        data = msg.value

        print("📥 RECEIVED")
        print(data)

        df = pd.DataFrame([data])

        for file in FILES:

            df.to_csv(
                file,
                mode="a",
                header=False,
                index=False
            )

        cursor.execute(
            """
            INSERT INTO weather_data
            (
                time,
                city,
                temperature,
                humidity,
                condition,
                aqi,
                pm25,
                pm10,
                co,
                no2
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                data["time"],
                data["city"],
                data["temperature"],
                data["humidity"],
                data["condition"],
                data.get("aqi"),
                data.get("pm25"),
                data.get("pm10"),
                data.get("co"),
                data.get("no2")
            )
        )

        db.commit()

        print("✅ INSERTED INTO POSTGRES")

    except Exception as e:

        db.rollback()

        print("❌ CONSUMER ERROR")
        print(e)

        time.sleep(2)