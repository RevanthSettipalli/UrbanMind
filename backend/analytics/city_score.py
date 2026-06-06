def city_health(temp, humidity):

    score = 100

    if temp > 38:
        score -= 40

    elif temp > 34:
        score -= 20

    if humidity > 85:
        score -= 20

    elif humidity > 70:
        score -= 10

    return max(score, 0)