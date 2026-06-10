def calculate_risk(
    temperature,
    humidity,
    aqi,
    pm25,
    pm10,
    co,
    no2,
    urban_score
):

    # Heat Risk
    if temperature >= 42:
        heat_risk = "HIGH"
    elif temperature >= 36:
        heat_risk = "MODERATE"
    else:
        heat_risk = "LOW"

    # Pollution Risk
    try:
        aqi_value = float(aqi)
    except:
        aqi_value = 0

    if aqi_value <= 5:
        aqi_component = aqi_value * 20
    else:
        aqi_component = aqi_value

    pollution_index = (
        aqi_component
        + pm25 * 0.30
        + pm10 * 0.10
        + co * 0.01
        + no2 * 2
    )

    if pollution_index >= 150:
        pollution_risk = "CRITICAL"
    elif pollution_index >= 100:
        pollution_risk = "HIGH"
    elif pollution_index >= 50:
        pollution_risk = "MODERATE"
    else:
        pollution_risk = "LOW"

    # Urban Risk
    if urban_score < 40:
        urban_risk = "CRITICAL"
    elif urban_score < 60:
        urban_risk = "HIGH"
    elif urban_score < 80:
        urban_risk = "MODERATE"
    else:
        urban_risk = "LOW"

    risk_score = 0

    risk_score += {
        "LOW": 10,
        "MODERATE": 40,
        "HIGH": 70,
        "CRITICAL": 100
    }[heat_risk]

    risk_score += {
        "LOW": 10,
        "MODERATE": 40,
        "HIGH": 70,
        "CRITICAL": 100
    }[pollution_risk]

    risk_score += {
        "LOW": 10,
        "MODERATE": 40,
        "HIGH": 70,
        "CRITICAL": 100
    }[urban_risk]

    risk_score = round(risk_score / 3)

    if urban_score < 40:
        risk_score = max(risk_score, 85)
    elif urban_score < 60:
        risk_score = max(risk_score, 65)
    elif urban_score < 80:
        risk_score = max(risk_score, 40)

    return {
        "heat_risk": heat_risk,
        "pollution_risk": pollution_risk,
        "urban_risk": urban_risk,
        "risk_score": risk_score,
        "emergency_level": (
            "CRITICAL" if risk_score >= 85 else
            "HIGH" if risk_score >= 65 else
            "MODERATE" if risk_score >= 40 else
            "LOW"
        )
    }
if __name__ == "__main__":

    print(
        calculate_risk(
            42,
            50,
            4,
            80,
            120,
            600,
            25,
            38
        )
    )