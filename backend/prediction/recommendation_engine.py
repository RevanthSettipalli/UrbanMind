def get_recommendation(temp, humidity):

    if temp >= 40:
        return "🔥 Heat Alert"

    elif humidity >= 85:
        return "🌧 Flood Monitoring"

    elif temp <= 15:
        return "❄ Cold Advisory"

    elif temp >= 35:
        return "⚠ High Temperature"

    elif humidity <= 35:
        return "💧 Low Humidity"

    return "✅ Safe Conditions"