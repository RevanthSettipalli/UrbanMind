import pandas as pd
import random
import time

from datetime import datetime
from pathlib import Path


# ===================================
# PATH
# ===================================

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT / "data" / "processed_weather.csv"


# ===================================
# CITY BASE WEATHER
# ===================================

CITY_BASE = {

    "Vijayawada": 34,

    "Hyderabad": 32,

    "Bangalore": 26,

    "Chennai": 33,

    "Mumbai": 29,

    "Delhi": 31
}


cities = list(
    CITY_BASE.keys()
)


# ===================================
# GENERATOR
# ===================================

while True:

    city = random.choice(
        cities
    )


    humidity = random.randint(
        35,
        90
    )


    hour = datetime.now().hour


    base_temp = CITY_BASE[
        city
    ]


    # Day/Night Effect

    if 11 <= hour <= 16:

        sunlight = 4

    elif 17 <= hour <= 20:

        sunlight = 2

    else:

        sunlight = -2


    # Realistic relation

    temperature = (

        base_temp

        +

        sunlight

        +

        ((100 - humidity) * 0.12)

        +

        random.uniform(
            -1.5,
            1.5
        )

    )


    temperature = round(
        temperature,
        1
    )


    row = {

        "time":
        datetime.now(),

        "city":
        city,

        "temperature":
        temperature,

        "humidity":
        humidity
    }


    df = pd.DataFrame(
        [row]
    )


    if CSV.exists():

        df.to_csv(

            CSV,

            mode="a",

            index=False,

            header=False
        )

    else:

        df.to_csv(

            CSV,

            index=False
        )


    print()

    print("🌍 New Weather Record")

    print(row)

    print()


    time.sleep(
        2
    )