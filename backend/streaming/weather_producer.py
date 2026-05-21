from kafka import KafkaProducer
import json
import time
import random


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v:
    json.dumps(v).encode()
)

while True:

    weather = {
        "temperature":
        random.randint(28,40),

        "humidity":
        random.randint(40,90)
    }

    producer.send(
        "weather",
        weather
    )

    print(
        "Sent:",
        weather
    )

    time.sleep(5)