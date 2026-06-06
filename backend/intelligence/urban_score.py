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

    score = 95

    # Temperature
    if temp > 35:
        score -= min(15, (temp - 35) * 1.5)
    elif temp < 10:
        score -= min(10, (10 - temp) * 1.0)

    # Humidity
    if hum > 85:
        score -= min(8, (hum - 85) * 0.3)
    elif hum < 20:
        score -= min(8, (20 - hum) * 0.3)

    # Forecast risk
    if forecast > 38:
        score -= 5

    # AQI (dominant factor but less extreme)
    aqi_penalty = {
        1: 0,
        2: 8,
        3: 18,
        4: 30,
        5: 45
    }
    score -= aqi_penalty.get(int(aqi), 0)

    # PM2.5 impact
    if pm25 > 15:
        score -= min(20, (pm25 - 15) * 0.20)

    # PM10 impact
    if pm10 > 45:
        score -= min(15, (pm10 - 45) * 0.08)

    # CO impact
    if co > 300:
        score -= min(8, (co - 300) / 200)

    # NO2 impact
    if no2 > 40:
        score -= min(12, (no2 - 40) * 0.20)

    score = max(25, min(95, round(score)))

    if score >= 80:
        level = "Excellent"
    elif score >= 60:
        level = "Good"
    elif score >= 40:
        level = "Moderate"
    else:
        level = "Critical"

    return {
        "score": score,
        "level": level
    }