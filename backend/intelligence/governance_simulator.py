

"""
UrbanMind Governance Simulation Engine
Evaluates policy interventions and estimates future urban outcomes.
"""


def simulate_policy(
    pollution_reduction,
    traffic_reduction,
    green_space_increase,
    policy_budget
):
    """
    Simulate governance actions.

    Parameters
    ----------
    pollution_reduction : float
    traffic_reduction : float
    green_space_increase : float
    policy_budget : float

    Returns
    -------
    dict
    """

    pollution_gain = float(pollution_reduction) * 0.20
    traffic_gain = float(traffic_reduction) * 0.15
    green_gain = float(green_space_increase) * 0.25
    budget_gain = float(policy_budget) * 0.02

    total_gain = round(
        pollution_gain
        + traffic_gain
        + green_gain
        + budget_gain,
        1
    )

    future_score = round(
        min(100, 70 + total_gain),
        1
    )

    roi = round(
        (total_gain / max(float(policy_budget), 1)) * 100,
        2
    )

    if future_score >= 90:
        recommendation = (
            "Excellent governance outlook. Continue sustainability investments."
        )
    elif future_score >= 80:
        recommendation = (
            "Positive trajectory. Prioritize pollution and mobility improvements."
        )
    elif future_score >= 70:
        recommendation = (
            "Moderate improvement expected. Increase policy investment."
        )
    else:
        recommendation = (
            "Urban resilience remains at risk. Immediate intervention recommended."
        )

    return {
        "future_score": future_score,
        "policy_gain": total_gain,
        "roi": roi,
        "recommendation": recommendation
    }