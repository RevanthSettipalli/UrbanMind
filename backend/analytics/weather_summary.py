import pandas as pd

FILE = "data/processed/weather_clean.csv"

df = pd.read_csv(FILE)

temp = df["temperature"].mean()
humidity = df["humidity"].mean()

print("\nUrbanMind Weather Summary\n")

print(f"Average Temperature: {temp:.1f} °C")

print(f"Average Humidity: {humidity:.0f}%")

if temp > 30:
    print("Status: Hot Weather")

else:
    print("Status: Moderate Weather")