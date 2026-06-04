def get_recommendation(
    temp,
    hum,
    aqi=1,
    pm25=0,
    pm10=0,
    co=0,
    no2=0,
    score=100
):

    messages = []
    risk = "Healthy"

    if aqi >= 5:
        risk = "Critical AQI"
        messages.append("🚨 AQI critical. Avoid outdoor activities.")
    elif aqi >= 4:
        risk = "Poor AQI"
        messages.append("🌫 Air quality is poor. Limit outdoor exposure.")

    if pm25 >= 75:
        risk = "PM2.5 High"
        messages.append("😷 PM2.5 elevated. Mask recommended.")
    elif pm25 >= 35:
        messages.append("😷 Sensitive groups should reduce outdoor activity.")

    if pm10 >= 100:
        risk = "PM10 High"
        messages.append("🌫 High particulate pollution detected.")

    if co >= 500:
        risk = "CO Alert"
        messages.append("⚠ Carbon monoxide levels are elevated.")

    if no2 >= 20:
        risk = "NO₂ Alert"
        messages.append("⚠ Nitrogen dioxide levels are elevated.")

    if temp >= 42:
        risk = "Extreme Heat"
        messages.append("🔥 Extreme heat detected. Avoid outdoor exposure.")
    elif temp >= 36:
        messages.append("☀ Stay hydrated and avoid peak afternoon heat.")

    if hum >= 85:
        messages.append("🌧 High humidity detected. Flood preparedness advised.")

    if score < 50:
        risk = "Urban Stress"
        messages.append("🏙 Urban health score is poor. Conditions need attention.")
    elif score < 70:
        messages.append("⚠ Urban conditions are moderate. Exercise caution.")
    elif score >= 85:
        messages.append("🌿 Air quality healthy. Outdoor activities recommended.")
        messages.append("🚶 Good conditions for walking and recreation.")

    if not messages:
        messages.append("🌿 Conditions are stable across the city.")

    return {
        "risk": risk,
        "message": "\n".join(messages)
    }