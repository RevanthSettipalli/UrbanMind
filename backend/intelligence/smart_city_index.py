

"""
UrbanMind National Smart City Index Engine
Combines multiple intelligence layers into a single national index.
"""


def calculate_national_index(
    urban_score,
    sdg_score,
    governance_score,
    forecast_score,
    risk_score
):
    """
    Calculate a composite Smart City Index.

    Parameters
    ----------
    urban_score : float
    sdg_score : float
    governance_score : float
    forecast_score : float
    risk_score : float

    Returns
    -------
    float
    """

    urban_score = float(urban_score)
    sdg_score = float(sdg_score)
    governance_score = float(governance_score)
    forecast_score = float(forecast_score)
    risk_score = float(risk_score)

    index_score = (
        urban_score * 0.35
        + sdg_score * 0.20
        + governance_score * 0.20
        + forecast_score * 0.15
        + (100 - risk_score) * 0.10
    )

    return round(index_score, 1)


def classify_city(index_score):
    """
    Classify city maturity based on index.
    """

    score = float(index_score)

    if score >= 90:
        return "Smart Leader"

    if score >= 80:
        return "Sustainable City"

    if score >= 70:
        return "Emerging Smart City"

    if score >= 60:
        return "Developing City"

    return "Priority Intervention"


def generate_city_profile(index_score):
    """
    Generate executive interpretation.
    """

    category = classify_city(index_score)

    profiles = {
        "Smart Leader": "Excellent urban performance with strong governance, sustainability and resilience indicators.",
        "Sustainable City": "Strong city performance with opportunities for innovation and long-term resilience.",
        "Emerging Smart City": "Positive trajectory with moderate intelligence and sustainability readiness.",
        "Developing City": "Requires targeted investment in governance, infrastructure and environmental performance.",
        "Priority Intervention": "High-risk urban profile requiring immediate policy and operational intervention."
    }

    return {
        "category": category,
        "description": profiles[category]
    }