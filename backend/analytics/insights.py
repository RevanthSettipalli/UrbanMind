def generate_insights(temp,humidity):

    msg=[]

    if temp>38:

        msg.append(
            "Heat emergency"
        )

    elif temp>33:

        msg.append(
            "High urban heat"
        )

    if humidity>80:

        msg.append(
            "High moisture"
        )

    if not msg:

        msg.append(
            "City conditions healthy"
        )

    return msg