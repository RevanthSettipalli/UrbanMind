

from statistics import mean


def detect_anomalies(df):
    anomalies = []
    risk_score = 0

    if df is None or len(df) < 5:
        return {
            "risk_score": 0,
            "alerts": [],
            "total_alerts": 0
        }

    try:

        latest = df.iloc[-1]

        avg_temp = mean(df["temperature"].tail(10))
        avg_humidity = mean(df["humidity"].tail(10))
        avg_aqi = mean(df["aqi"].tail(10))

        if latest["temperature"] > avg_temp + 5:
            risk_score += 25
            anomalies.append(
                {
                    "type": "Temperature",
                    "severity": "High",
                    "city": latest["city"],
                    "message": f"🔥 Temperature anomaly detected in {latest['city']}"
                }
            )

        if latest["humidity"] > avg_humidity + 15:
            risk_score += 20
            anomalies.append(
                {
                    "type": "Humidity",
                    "severity": "Moderate",
                    "city": latest["city"],
                    "message": f"💧 Humidity anomaly detected in {latest['city']}"
                }
            )

        if latest["aqi"] > avg_aqi + 2:
            risk_score += 30

            severity = "Critical" if latest["aqi"] >= 5 else "High"

            anomalies.append(
                {
                    "type": "AQI",
                    "severity": severity,
                    "city": latest["city"],
                    "message": f"🌫 AQI spike detected in {latest['city']}"
                }
            )

        if (
            "pm25" in df.columns
            and latest["pm25"] > df["pm25"].tail(10).mean() + 20
        ):
            risk_score += 15
            anomalies.append(
                {
                    "type": "PM2.5",
                    "severity": "Moderate",
                    "city": latest["city"],
                    "message": f"🏭 PM2.5 anomaly detected in {latest['city']}"
                }
            )

        if latest["temperature"] >= 40:
            risk_score += 25
            anomalies.append(
                {
                    "type": "Heatwave",
                    "severity": "Critical",
                    "city": latest["city"],
                    "message": f"🔥 Heatwave risk detected in {latest['city']}"
                }
            )

        if latest["humidity"] >= 85:
            risk_score += 10
            anomalies.append(
                {
                    "type": "Rainfall/Humidity",
                    "severity": "High",
                    "city": latest["city"],
                    "message": f"🌧 Extreme humidity event in {latest['city']}"
                }
            )

    except Exception:
        pass

    return {
        "risk_score": min(risk_score, 100),
        "alerts": anomalies,
        "total_alerts": len(anomalies)
    }


if __name__ == "__main__":

    import pandas as pd

    sample = pd.DataFrame(
        {
            "city": ["Delhi"] * 10,
            "temperature": [30, 31, 32, 31, 30, 32, 31, 30, 31, 40],
            "humidity": [50, 51, 49, 50, 52, 51, 50, 49, 50, 80],
            "aqi": [2, 2, 2, 3, 2, 2, 3, 2, 2, 6],
            "pm25": [20, 21, 19, 20, 22, 21, 20, 19, 20, 55],
        }
    )

    print(detect_anomalies(sample))