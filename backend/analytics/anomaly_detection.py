def calculate_risk(temp, humidity):

    score = 100
    alerts = []

    if temp > 38:
        score -= 40
        alerts.append("Extreme Heat")

    elif temp > 34:
        score -= 20
        alerts.append("High Temperature")

    if humidity > 85:
        score -= 25
        alerts.append("Humidity Spike")

    elif humidity > 70:
        score -= 10
        alerts.append("High Humidity")

    risk = (
        "LOW"
        if score >= 80
        else "MEDIUM"
        if score >= 50
        else "HIGH"
    )

    return score, risk, alerts