def forecast_city(temp, hum, aqi):
    next_hour_temp = round(temp + 0.5, 1)
    next_day_temp = round(temp + 2.0, 1)

    if aqi <= 2:
        aqi_forecast = "Good"
    elif aqi <= 4:
        aqi_forecast = "Moderate"
    else:
        aqi_forecast = "Poor"

    if temp >= 40:
        summary = "Heat levels likely to increase. Stay hydrated."
    elif hum >= 80:
        summary = "High humidity expected. Possible discomfort."
    elif aqi > 4:
        summary = "Air quality may deteriorate."
    else:
        summary = "Urban conditions expected to remain stable."

    return {
        "next_hour_temp": next_hour_temp,
        "next_day_temp": next_day_temp,
        "aqi_forecast": aqi_forecast,
        "summary": summary
    }


if __name__ == "__main__":
    print(forecast_city(34, 55, 3))