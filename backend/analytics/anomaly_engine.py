import pandas as pd


def detect_anomaly(df):

    temp_mean = df["temperature"].mean()
    temp_std = df["temperature"].std()

    latest = df.iloc[-1]

    z = (
        latest["temperature"]
        - temp_mean
    ) / temp_std

    if abs(z) > 2:

        return True

    return False