import json
import pandas as pd

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT/"data"/"weather_history.csv"

ALERT = ROOT/"data"/"alerts.json"


def generate_alerts():

    try:

        df = pd.read_csv(CSV)

    except:

        return []


    if df.empty:

        return []


    latest = df.iloc[-1]

    alerts = []


    temp = float(
        latest["temperature"]
    )

    hum = float(
        latest["humidity"]
    )

    city = str(
        latest["city"]
    )


    if temp >= 30:

        alerts.append({

            "type":"heat",

            "message":
            f"🔥 Extreme Heat in {city}"

        })


    if hum >= 60:

        alerts.append({

            "type":"humidity",

            "message":
            f"🌊 Flood Risk in {city}"

        })


    if temp <= 20:

        alerts.append({

            "type":"cold",

            "message":
            f"❄️ Cold Conditions in {city}"

        })


    ALERT.parent.mkdir(
        exist_ok=True
    )


    with open(
        ALERT,
        "w"
    ) as f:

        json.dump(
            alerts,
            f,
            indent=4
        )


    return alerts


if __name__ == "__main__":

    result = generate_alerts()

    print(
        "\nAlerts Generated\n"
    )

    print(
        result
    )