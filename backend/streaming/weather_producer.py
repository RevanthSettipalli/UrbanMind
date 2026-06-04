import json
import time
import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

load_dotenv()

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)

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

def get_aqi(lat, lon):

    try:

        url = (
            "https://api.openweathermap.org/data/2.5/air_pollution"
        )

        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        if "list" not in data:
            return {}

        pollution = data["list"][0]

        return {
            "aqi": pollution["main"]["aqi"],
            "pm25": pollution["components"].get("pm2_5", 0),
            "pm10": pollution["components"].get("pm10", 0),
            "co": pollution["components"].get("co", 0),
            "no2": pollution["components"].get("no2", 0)
        }

    except Exception as e:

        print(f"AQI API Error")
        print(e)

        return {}

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

def get_weather(city):

    try:

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
        )

        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        weather = response.json()

        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]

        aqi_data = get_aqi(
            lat,
            lon
        )

        return {
            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "city": city,
            "temperature": weather["main"]["temp"],
            "humidity": weather["main"]["humidity"],
            "condition": weather["weather"][0]["main"],
            "aqi": aqi_data.get("aqi", 0),
            "pm25": aqi_data.get("pm25", 0),
            "pm10": aqi_data.get("pm10", 0),
            "co": aqi_data.get("co", 0),
            "no2": aqi_data.get("no2", 0)
        }

    except Exception as e:

        print(f"Weather API Error: {city}")
        print(e)

        return None

print("🚀 STARTING PRODUCER")

producer = None

while producer is None:
    try:

        producer = KafkaProducer(
            bootstrap_servers=[BROKER],

            value_serializer=lambda x:
            json.dumps(x).encode("utf-8"),

            retries=10,

            acks=1,

            linger_ms=100,

            batch_size=16384,

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

        for city in cities:

            data = get_weather(city)

            if not data:
                continue

            producer.send(
                TOPIC,
                value=data
            )

            print("📤 SENT")
            print(data)

        producer.flush()

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