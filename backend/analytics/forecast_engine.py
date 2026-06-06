import pandas as pd


def forecast(model):

    result = []

    for h in range(
        40,
        91,
        5
    ):

        temp = model.predict(
            [[h]]
        )[0]

        result.append(

            {

                "humidity": h,

                "prediction": round(
                    temp,
                    1
                )

            }

        )

    return pd.DataFrame(
        result
    )