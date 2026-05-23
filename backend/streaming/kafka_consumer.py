from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(

    "urbanmind",

    bootstrap_servers="localhost:9092",

    value_deserializer=
    lambda x:
    json.loads(
        x.decode()
    )
)


for msg in consumer:

    print(

        "Received:",

        msg.value

    )