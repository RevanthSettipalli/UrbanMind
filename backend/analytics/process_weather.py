import pandas as pd

df = pd.read_csv("data/weather_history.csv")

df["temperature_f"] = (
    df["temperature"] * 9/5
) + 32

df["humidity_level"] = df["humidity"].apply(
    lambda x:
    "High"
    if x > 70
    else "Normal"
)

df.to_csv(
    "data/processed_weather.csv",
    index=False
)

print("Weather processed")