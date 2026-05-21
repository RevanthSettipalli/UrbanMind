from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    "weather",

    bootstrap_servers=
    "localhost:9092",

    value_deserializer=
    lambda x:
    json.loads(
        x.decode()
    )
)

print(
"Listening..."
)

for msg in consumer:

    print(
        msg.value
    )