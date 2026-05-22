import pandas as pd

df = pd.read_csv(
    "data/weather_history.csv"
)

summary = {

    "avg_temp":
    df["temperature"].mean(),

    "max_temp":
    df["temperature"].max(),

    "avg_humidity":
    df["humidity"].mean()

}

print(summary)