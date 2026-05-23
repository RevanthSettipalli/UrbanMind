import pandas as pd


def create_report(df):

    report = pd.DataFrame({

        "Average Temp": [

            round(
                df.temperature.mean(),
                1
            )

        ],

        "Max Temp": [

            round(
                df.temperature.max(),
                1
            )

        ],

        "Average Humidity": [

            round(
                df.humidity.mean(),
                1
            )

        ]

    })

    return report