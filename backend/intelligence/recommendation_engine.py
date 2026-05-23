def get_recommendation(temp, hum):

    if temp >= 42:
        return {
            "risk": "Extreme",
            "message": "🔥 Avoid outdoor exposure"
        }

    elif temp >= 36:
        return {
            "risk": "Moderate",
            "message": "☀ Stay hydrated"
        }

    elif hum >= 85:
        return {
            "risk": "Humidity",
            "message": "🌧 Flood preparedness advised"
        }

    return {
        "risk": "Safe",
        "message": "✅ Conditions stable"
    }