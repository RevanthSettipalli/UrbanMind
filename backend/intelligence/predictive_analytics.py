

"""
UrbanMind Predictive Analytics Engine
"""


def forecast_urban_score(current_score):

    return round(current_score + 2, 1)



def forecast_aqi(current_aqi):

    return round(current_aqi + 0.5, 2)



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
        return "AQI expected to worsen within 24 hours"

    if current_score < 50:
        return "Urban conditions require immediate intervention"

    return "No major warning signals detected"



def predictive_report(current_score, current_aqi):

    return {
        "urban_score_forecast": forecast_urban_score(
            current_score
        ),
        "aqi_forecast": forecast_aqi(
            current_aqi
        ),
        "risk_forecast": forecast_risk(
            current_score
        ),
        "warning": early_warning(
            current_aqi,
            current_score
        )
    }


if __name__ == "__main__":

    print(
        predictive_report(
            current_score=82,
            current_aqi=3
        )
    )