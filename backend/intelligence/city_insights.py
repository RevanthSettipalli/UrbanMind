import pandas as pd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT/"data"/"weather_history.csv"


def generate_city_insights():

    try:

        df = pd.read_csv(CSV)

    except:

        return {}


    if df.empty:

        return {}


    insights = {}

    grouped = (

        df
        .groupby("city")
        .tail(50)
        .groupby("city")

    )


    for city, data in grouped:

        temp = data["temperature"].mean()

        hum = data["humidity"].mean()


        if temp > 40:

            status = "🔥 Extreme Heat"

        elif temp > 35:

            status = "🌡 Warm"

        elif hum > 85:

            status = "🌊 Flood Risk"

        else:

            status = "✅ Stable"


        score = max(
            0,
            min(
                100,
                100
                -
                (
                    abs(temp-28)*2
                    +
                    abs(hum-65)
                )
            )
        )


        insights[city] = {

            "temperature":
            round(temp,1),

            "humidity":
            round(hum,1),

            "score":
            round(score),

            "status":
            status

        }


    return insights


if __name__ == "__main__":

    result = generate_city_insights()

    print()

    for city, info in result.items():

        print(
            city,
            "→",
            info
        )