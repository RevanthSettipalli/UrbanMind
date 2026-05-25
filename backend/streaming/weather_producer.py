import json
import time
import random
import os
from pathlib import Path
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

BROKER = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:9092"
)

TOPIC = "weather"
ROOT = Path(__file__).resolve().parents[2]

SETTINGS = (
    ROOT
    / "data"
    / "settings.json"
)


def get_refresh_rate():

    try:

        if SETTINGS.exists():

            with open(
                SETTINGS
            ) as f:

                settings = json.load(f)

            rate = settings.get(
                "refresh_rate",
                settings.get(
                    "refresh",
                    10
                )
            )

            return max(
                1,
                int(rate)
            )

    except:
        pass

    return 10

print(f"Using broker: {BROKER}")
print("🚀 STARTING PRODUCER")

cities = [
    "Delhi",
    "Mumbai",
    "Hyderabad",
    "Chennai",
    "Bangalore",
    "Kolkata",
    "Vijayawada",
    "Pune",
    "Ahmedabad",
    "Jaipur"
]

conditions = [
    "Sunny",
    "Cloudy",
    "Rainy",
    "Windy"
]

print("🚀 STARTING PRODUCER")

producer = None

while producer is None:
    try:

        producer = KafkaProducer(
            bootstrap_servers=[BROKER],

            value_serializer=lambda x:
            json.dumps(x).encode("utf-8"),

            retries=10,

            request_timeout_ms=30000,

            api_version_auto_timeout_ms=30000,

            max_block_ms=60000
        )

        print("✅ PRODUCER CONNECTED")

    except Exception as e:

        print("⏳ WAITING FOR KAFKA...")
        print(e)

        time.sleep(5)

print("📡 PRODUCER RUNNING")

while True:

    try:

        data = {
            "time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "city":
            random.choice(
                cities
            ),

            "temperature":
            round(
                random.uniform(
                    22,
                    40
                ),
                1
            ),

            "humidity":
            random.randint(
                40,
                90
            ),

            "condition":
            random.choice(
                conditions
            )
        }

        future = producer.send(
            TOPIC,
            value=data
        )

        future.get(
            timeout=10
        )

        producer.flush()

        print("📤 SENT")
        print(data)

        refresh_rate = get_refresh_rate()

        print(
            f"⏱ Refresh: {refresh_rate}s"
        )

        time.sleep(
            refresh_rate
        )

    except KafkaError as e:

        print("❌ SEND FAILED")
        print(e)

        time.sleep(5)

    except Exception as e:

        print("⚠️ ERROR")
        print(e)

        time.sleep(5)