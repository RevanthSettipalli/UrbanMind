"""
UrbanMind Predictive Analytics Engine
Advanced Predictive Intelligence Module
"""


def forecast_urban_score(current_score):
    forecast = current_score + ((100 - current_score) * 0.08)
    return round(min(forecast, 100), 1)



def forecast_aqi(current_aqi):
    forecast = current_aqi * 1.08
    return round(min(forecast, 5), 2)



def forecast_risk(current_score):
    if current_score < 50:
        return "CRITICAL"
    elif current_score < 70:
        return "HIGH"
    elif current_score < 85:
        return "MODERATE"
    return "LOW"



def early_warning(current_aqi, current_score):
    if current_aqi >= 4:
        return "Air quality deterioration expected within 24 hours."

    if current_score < 50:
        return "Urban conditions require immediate intervention."

    return "No major warning signals detected."



def resource_demand_forecast(current_score, current_aqi):
    electricity = "HIGH" if current_score < 70 else "MODERATE"
    water = "HIGH" if current_aqi >= 4 else "MODERATE"
    emergency = "HIGH" if current_score < 60 else "LOW"

    return {
        "electricity_demand": electricity,
        "water_demand": water,
        "emergency_demand": emergency,
    }



def urban_risk_intelligence(current_score, current_aqi):
    infrastructure_risk = max(0, 100 - current_score)
    pollution_risk = current_aqi * 20
    traffic_risk = 40 if current_score < 70 else 20
    weather_risk = 35 if current_aqi >= 4 else 15

    overall = round(
        (
            infrastructure_risk
            + pollution_risk
            + traffic_risk
            + weather_risk
        ) / 4,
        1,
    )

    return {
        "infrastructure_risk": round(infrastructure_risk, 1),
        "pollution_risk": round(pollution_risk, 1),
        "traffic_risk": round(traffic_risk, 1),
        "weather_risk": round(weather_risk, 1),
        "overall_risk": overall,
    }



def executive_recommendations(current_score, current_aqi):
    recommendations = []

    if current_aqi >= 4:
        recommendations.append(
            "Increase air quality monitoring and citizen alerts."
        )

    if current_score < 70:
        recommendations.append(
            "Prioritize infrastructure and public service improvements."
        )

    recommendations.append(
        "Optimize urban resources using predictive intelligence."
    )

    recommendations.append(
        "Expand green initiatives and sustainability programs."
    )

    return recommendations



def predictive_intelligence_score(current_score, current_aqi):
    future_health = round(
        (forecast_urban_score(current_score) * 0.8)
        + ((5 - current_aqi) * 4),
        1,
    )

    confidence = min(98, max(85, int(current_score)))

    return {
        "future_city_health": future_health,
        "future_risk": forecast_risk(current_score),
        "confidence": confidence,
    }



def predictive_report(current_score, current_aqi):
    return {
        "urban_score_forecast": forecast_urban_score(current_score),
        "aqi_forecast": forecast_aqi(current_aqi),
        "risk_forecast": forecast_risk(current_score),
        "warning": early_warning(current_aqi, current_score),
        "resource_demand": resource_demand_forecast(
            current_score,
            current_aqi,
        ),
        "risk_intelligence": urban_risk_intelligence(
            current_score,
            current_aqi,
        ),
        "recommendations": executive_recommendations(
            current_score,
            current_aqi,
        ),
        "predictive_intelligence": predictive_intelligence_score(
            current_score,
            current_aqi,
        ),
    }


if __name__ == "__main__":
    print(
        predictive_report(
            current_score=82,
            current_aqi=3,
        )
    )