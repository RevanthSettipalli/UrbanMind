import pandas as pd


def ask_urbanmind(
    question,
    df
):

    q = question.lower()


    if "temperature" in q:

        return (

            f"Average temperature: "

            f"{df['temperature'].mean():.1f}°C"

        )


    elif "humidity" in q:

        return (

            f"Average humidity: "

            f"{df['humidity'].mean():.1f}%"

        )


    elif "city" in q:

        hottest = (

            df

            .groupby("city")

            ["temperature"]

            .mean()

            .idxmax()

        )

        return (

            f"Hottest city: "

            f"{hottest}"

        )


    elif "health" in q:

        return (

            "Urban Health: 87%"

        )


    elif "risk" in q:

        return (

            "Current Risk: Moderate"

        )


    elif "forecast" in q:

        return (

            "Forecast: Stable"

        )


    return """

Try asking:

• temperature

• humidity

• hottest city

• health

• forecast

"""