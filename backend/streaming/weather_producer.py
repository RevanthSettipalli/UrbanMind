import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

BROKER = "127.0.0.1:19092"
TOPIC = "weather"

cities = [
    "Delhi",
    "Mumbai",
    "Hyderabad",
    "Chennai",
    "Bangalore",
    "Kolkata"
]

conditions = [
    "Sunny",
    "Cloudy",
    "Rainy",
    "Windy"
]

producer = None

print("🚀 STARTING PRODUCER")

while producer is None:
    try:
        producer = KafkaProducer(
            bootstrap_servers=[BROKER],
            value_serializer=lambda x: json.dumps(x).encode(),
            request_timeout_ms=10000
        )

        print("✅ PRODUCER CONNECTED")

    except Exception as e:
        print("WAITING FOR KAFKA...")
        print(e)
        time.sleep(3)

print("📡 PRODUCER RUNNING")

while True:

    weather = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": random.choice(cities),
        "temperature": round(random.uniform(20, 40), 1),
        "humidity": random.randint(40, 90),
        "condition": random.choice(conditions)
    }

    try:

        producer.send(
            TOPIC,
            weather
        )

        producer.flush()

        print("\n📤 SENT")
        print(weather)

        time.sleep(3)

    except Exception as e:

        print("SEND FAILED")
        print(e)

        time.sleep(3)