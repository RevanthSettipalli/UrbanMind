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
    pollution_index = (
        aqi * 20 +
        pm25 * 0.3 +
        pm10 * 0.1 +
        co * 0.01 +
        no2 * 2
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

    return {
        "heat_risk": heat_risk,
        "pollution_risk": pollution_risk,
        "urban_risk": urban_risk
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