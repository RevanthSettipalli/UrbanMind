import json
import pandas as pd

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT/"data"/"processed_weather.csv"

ALERT = ROOT/"data"/"alerts.json"


def generate_alerts():

    try:

        df = pd.read_csv(CSV)

    except:

        return []


    if df.empty:

        return []


    alerts = []


    latest_cities = (
        df.groupby("city")
        .tail(1)
    )

    for _, latest in latest_cities.iterrows():

        temp = float(latest.get("temperature", 0))
        hum = float(latest.get("humidity", 0))
        aqi = float(latest.get("aqi", 0))
        pm25 = float(latest.get("pm25", 0))
        pm10 = float(latest.get("pm10", 0))
        co = float(latest.get("co", 0))
        no2 = float(latest.get("no2", 0))
        city = str(latest.get("city", "Unknown"))

        if temp >= 40:
            alerts.append({
                "type": "heat",
                "message": f"🔥 Extreme Heat Alert - {city}"
            })

        if hum >= 85:
            alerts.append({
                "type": "flood",
                "message": f"🌊 Flood Risk Alert - {city}"
            })

        if temp <= 10:
            alerts.append({
                "type": "cold",
                "message": f"❄ Cold Weather Alert - {city}"
            })

        if aqi >= 4:
            alerts.append({
                "type": "aqi",
                "message": f"🌫 Poor AQI Alert - {city}"
            })

        if pm25 >= 75:
            alerts.append({
                "type": "pm25",
                "message": f"😷 PM2.5 Alert - {city}"
            })

        if pm10 >= 100:
            alerts.append({
                "type": "pm10",
                "message": f"🌫 PM10 Alert - {city}"
            })

        if co >= 500:
            alerts.append({
                "type": "co",
                "message": f"⚠ CO Alert - {city}"
            })

        if no2 >= 20:
            alerts.append({
                "type": "no2",
                "message": f"⚠ NO₂ Alert - {city}"
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