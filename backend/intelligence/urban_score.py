def calculate_score(
    temp,
    hum,
    forecast
):

    score = 100


    if temp > 35:

        score -= (
            temp - 35
        ) * 2


    if hum > 80:

        score -= (
            hum - 80
        )


    if forecast > 38:

        score -= 10


    score = max(
        0,
        round(score)
    )


    if score >= 85:

        level = "Excellent"

    elif score >= 70:

        level = "Good"

    elif score >= 50:

        level = "Moderate"

    else:

        level = "Critical"


    return {

        "score": score,

        "level": level

    }