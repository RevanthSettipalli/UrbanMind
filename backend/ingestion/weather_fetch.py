import requests
import json
from pathlib import Path
from datetime import datetime

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=16.5062"
    "&longitude=80.6480"
    "&current=temperature_2m,relative_humidity_2m"
)

try:
    response = requests.get(URL, timeout=10)

    if response.status_code == 200:

        data = response.json()

        data["fetched_at"] = str(datetime.now())

        Path("data/raw").mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            "data/raw/weather.json",
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        print("Weather data stored successfully")

    else:
        print("API error:", response.status_code)

except Exception as e:
    print("Error:", e)