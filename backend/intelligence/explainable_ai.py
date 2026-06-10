

"""
UrbanMind Explainable AI Engine
Provides feature contribution scores for analytics dashboards.
"""


def calculate_feature_importance(
    temperature,
    humidity,
    aqi,
    risk_score
):
    """
    Generate normalized feature importance values.

    Returns:
    {
        'Temperature': value,
        'Humidity': value,
        'Air Quality': value,
        'Risk Intelligence': value
    }
    """

    temp_score = max(0, 100 - abs(float(temperature) - 28) * 2)
    hum_score = max(0, 100 - abs(float(humidity) - 55) * 1.5)
    aqi_score = max(0, 100 - float(aqi) * 5)
    risk_component = max(0, 100 - float(risk_score))

    total = (
        temp_score
        + hum_score
        + aqi_score
        + risk_component
    )

    if total == 0:
        return {
            'Temperature': 25,
            'Humidity': 25,
            'Air Quality': 25,
            'Risk Intelligence': 25
        }

    return {
        'Temperature': round((temp_score / total) * 100, 1),
        'Humidity': round((hum_score / total) * 100, 1),
        'Air Quality': round((aqi_score / total) * 100, 1),
        'Risk Intelligence': round((risk_component / total) * 100, 1)
    }