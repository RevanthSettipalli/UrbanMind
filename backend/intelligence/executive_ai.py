

"""
UrbanMind Executive AI Advisor
"""


def generate_executive_report(
    city,
    score,
    heat_risk,
    pollution_risk,
    urban_risk
):

    summary = (
        f"{city} currently has an Urban Score of {score}. "
        f"Heat Risk is {heat_risk}, Pollution Risk is {pollution_risk}, "
        f"and overall Urban Risk is {urban_risk}."
    )

    if urban_risk == "CRITICAL":

        action = (
            "Immediate intervention recommended. Increase monitoring, "
            "issue public advisories and deploy mitigation measures."
        )

    elif urban_risk == "HIGH":

        action = (
            "Enhanced monitoring recommended. Review environmental "
            "conditions and preparedness plans."
        )

    elif urban_risk == "MODERATE":

        action = (
            "Conditions are manageable but should continue to be monitored."
        )

    else:

        action = (
            "Urban conditions are stable. Maintain routine monitoring."
        )

    return {
        "summary": summary,
        "action": action
    }


if __name__ == "__main__":

    report = generate_executive_report(
        city="Delhi",
        score=46,
        heat_risk="HIGH",
        pollution_risk="CRITICAL",
        urban_risk="CRITICAL"
    )

    print(report)