import numpy as np


def generate_forecast(
    base_temp,
    base_humidity,
    hours=24
):

    forecast = []

    for hour in range(hours):

        temperature = round(

            base_temp

            +

            np.random.normal(
                0,
                1.5
            ),

            1

        )

        humidity = round(

            max(
                35,

                min(
                    95,

                    base_humidity

                    +

                    np.random.normal(
                        0,
                        3
                    )

                )

            ),

            1

        )

        confidence = round(

            max(

                80,

                98

                -

                abs(
                    temperature
                    -
                    base_temp
                )

            )

        )

        forecast.append({

            "hour": hour + 1,

            "temperature": temperature,

            "humidity": humidity,

            "confidence": confidence

        })

    return forecast