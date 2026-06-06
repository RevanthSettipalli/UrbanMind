from kafka import KafkaProducer
import json
import random
import time


producer = KafkaProducer(

    bootstrap_servers="localhost:9092",

    value_serializer=lambda v:
    json.dumps(v).encode()

)


while True:

    data = {

        "temperature":
        round(
            random.uniform(
                25,
                42
            ),
            1
        ),

        "humidity":
        random.randint(
            40,
            90
        )
    }

    producer.send(
        "urbanmind",
        data
    )

    print(
        "Sent:",
        data
    )

    time.sleep(3)