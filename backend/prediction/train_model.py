import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

FILE = "data/processed/weather_clean.csv"

df = pd.read_csv(FILE)

X = df[["humidity"]]
y = df["temperature"]

model = LinearRegression()

model.fit(X, y)

joblib.dump(
    model,
    "models/weather/weather_model.pkl"
)

print("\nModel trained successfully")