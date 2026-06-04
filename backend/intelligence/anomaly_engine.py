

from statistics import mean


def detect_anomalies(df):

    anomalies = []

    if df is None or len(df) < 5:
        return anomalies

    try:

        latest = df.iloc[-1]

        avg_temp = mean(df["temperature"].tail(10))
        avg_humidity = mean(df["humidity"].tail(10))
        avg_aqi = mean(df["aqi"].tail(10))

        if latest["temperature"] > avg_temp + 5:
            anomalies.append(
                f"🔥 Temperature anomaly detected in {latest['city']}"
            )

        if latest["humidity"] > avg_humidity + 15:
            anomalies.append(
                f"💧 Humidity anomaly detected in {latest['city']}"
            )

        if latest["aqi"] > avg_aqi + 2:
            anomalies.append(
                f"🌫 AQI spike detected in {latest['city']}"
            )

        if (
            "pm25" in df.columns
            and latest["pm25"] > df["pm25"].tail(10).mean() + 20
        ):
            anomalies.append(
                f"🏭 PM2.5 anomaly detected in {latest['city']}"
            )

    except Exception:
        pass

    return anomalies


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