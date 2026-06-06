import pandas as pd
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT / "data" / "processed_weather.csv"

OUTPUT = ROOT / "data" / "alerts.json"


TEMP_HIGH = 38

TEMP_CRITICAL = 42

HUMIDITY_HIGH = 85


def build_alerts():

    try:

        df = pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

    except:

        return


    if len(df) == 0:

        return


    latest = df.iloc[-1]

    alerts = []


    temp = float(
        latest["temperature"]
    )

    hum = float(
        latest["humidity"]
    )


    if temp >= TEMP_CRITICAL:

        alerts.append({

            "type":
            "CRITICAL",

            "message":
            f"Extreme heat detected ({temp}°C)"
        })


    elif temp >= TEMP_HIGH:

        alerts.append({

            "type":
            "WARNING",

            "message":
            f"High temperature ({temp}°C)"
        })


    if hum >= HUMIDITY_HIGH:

        alerts.append({

            "type":
            "WARNING",

            "message":
            f"Humidity spike ({hum}%)"
        })


    if len(alerts) == 0:

        alerts.append({

            "type":
            "OK",

            "message":
            "City Stable"
        })


    with open(

        OUTPUT,

        "w"

    ) as f:

        json.dump(

            alerts,

            f,

            indent=4
        )


if __name__ == "__main__":

    build_alerts()

    print(
        "Alerts Updated"
    )