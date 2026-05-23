def calculate_risk(
    temp,
    humidity
):

    if temp >= 42:

        return (
            "Extreme",
            "red"
        )

    elif temp >= 36:

        return (
            "Moderate",
            "orange"
        )

    elif humidity >= 85:

        return (
            "Humidity",
            "blue"
        )

    return (
        "Safe",
        "green"
    )