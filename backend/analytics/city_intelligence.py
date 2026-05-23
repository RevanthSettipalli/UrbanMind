def city_intelligence(temp, humidity):

    heat = temp + humidity / 20

    comfort = max(
        0,
        100 - abs(heat - 26) * 3
    )

    if heat > 40:
        action = "Avoid Outdoor Activity"

    elif heat > 35:
        action = "Hydrate"

    else:
        action = "Normal"

    return {

        "heat_index": round(
            heat,
            1
        ),

        "comfort": round(
            comfort,
            1
        ),

        "action": action
    }