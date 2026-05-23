import pandas as pd
import joblib
import os
from sklearn.linear_model import LinearRegression


print("Model Retraining Started")

DATA = "data/weather_history.csv"

MODEL_DIR = "models/weather"
MODEL_PATH = "models/weather/weather_model.pkl"

os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATA)

X = df[["humidity"]]
y = df["temperature"]

model = LinearRegression()

model.fit(X, y)

joblib.dump(
    model,
    MODEL_PATH
)

print("Model Saved:", MODEL_PATH)
print("Model Updated")