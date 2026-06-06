import joblib
import pandas as pd


MODEL = "models/weather/weather_model.pkl"

model = joblib.load(MODEL)

humidity = float(
    input(
        "Enter humidity (%): "
    )
)

sample = pd.DataFrame(
    {
        "humidity": [humidity]
    }
)

prediction = model.predict(
    sample
)

print("\nUrbanMind Prediction")

print(
    f"Predicted Temperature: "
    f"{prediction[0]:.2f} °C"
)