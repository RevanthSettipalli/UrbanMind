import csv
import json
import os
import time

from kafka import KafkaConsumer

BROKER = "127.0.0.1:19092"
TOPIC = "weather"

CSV = "data/weather_stream.csv"

os.makedirs("data", exist_ok=True)

print("🚀 STARTING CONSUMER")

consumer = None

while consumer is None:

    try:

        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=[BROKER],
            value_deserializer=lambda x: json.loads(
                x.decode()
            ),
            auto_offset_reset="latest",
            consumer_timeout_ms=0
        )

        print("✅ CONSUMER CONNECTED")

    except Exception as e:

        print("WAITING...")
        print(e)

        time.sleep(3)

print("📡 CONSUMER RUNNING")

with open(
    CSV,
    "a",
    newline=""
) as f:

    writer = csv.writer(f)

    if os.stat(CSV).st_size == 0:

        writer.writerow([
            "timestamp",
            "city",
            "temperature",
            "humidity",
            "condition"
        ])

    for msg in consumer:

        row = msg.value

        print("\n📥 RECEIVED")
        print(row)

        writer.writerow([
            row["timestamp"],
            row["city"],
            row["temperature"],
            row["humidity"],
            row["condition"]
        ])

        f.flush()

        print("✅ SAVED")