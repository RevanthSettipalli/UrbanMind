def calculate_score(
    temp,
    hum,
    forecast,
    aqi,
    pm25,
    pm10,
    co,
    no2
):

    score = 100

    # Temperature
    if temp > 35:
        score -= min(20, (temp - 35) * 2)
    elif temp < 10:
        score -= min(15, (10 - temp) * 1.5)

    # Humidity
    if hum > 80:
        score -= min(10, (hum - 80) * 0.5)
    elif hum < 20:
        score -= min(10, (20 - hum) * 0.5)

    # Forecast risk
    if forecast > 38:
        score -= 10

    # AQI (dominant factor)
    aqi_penalty = {
        1: 0,
        2: 10,
        3: 25,
        4: 40,
        5: 60
    }
    score -= aqi_penalty.get(int(aqi), 0)

    # PM2.5 impact
    if pm25 > 15:
        score -= min(20, (pm25 - 15) * 0.35)

    # PM10 impact
    if pm10 > 45:
        score -= min(10, (pm10 - 45) * 0.10)

    # CO impact
    if co > 300:
        score -= min(10, (co - 300) / 100)

    # NO2 impact
    if no2 > 40:
        score -= min(10, (no2 - 40) * 0.25)

    score = max(0, min(100, round(score)))

    if score >= 85:
        level = "Excellent"
    elif score >= 70:
        level = "Good"
    elif score >= 50:
        level = "Moderate"
    else:
        level = "Critical"

    return {
        "score": score,
        "level": level
    }