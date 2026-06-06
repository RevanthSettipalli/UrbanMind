import joblib
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = "backend/models/lstm_weather.keras"
SCALER_PATH = "backend/models/lstm_scaler.pkl"

try:
    model = load_model(MODEL_PATH)
    print("LSTM MODEL LOADED")
except Exception as e:
    print("LSTM MODEL ERROR:", e)
    model = None

try:
    scaler = joblib.load(SCALER_PATH)
    print("LSTM SCALER LOADED")
except Exception as e:
    print("LSTM SCALER ERROR:", e)
    scaler = None


def lstm_forecast(
    temperature,
    humidity,
    aqi,
    pm25,
    pm10,
    co,
    no2,
):
    print("STEP 1 - Calling LSTM")

    if model is None or scaler is None:
        print("LSTM model/scaler missing -> fallback")
        return {
            "next_temperature": round(float(temperature) + 1, 1),
            "confidence": 80,
            "model": "Fallback",
            "trend": "Stable",
        }

    features = np.array([
        [
            temperature,
            humidity,
            aqi,
            pm25,
            pm10,
            co,
            no2,
        ]
    ])

    try:
        scaled_row = scaler.transform(features)
    except Exception as e:
        print("SCALER ERROR:", e)
        return {
            "next_temperature": round(float(temperature) + 1, 1),
            "confidence": 80,
            "model": "Fallback",
            "trend": "Stable",
        }

    sequence = np.repeat(
        scaled_row,
        24,
        axis=0,
    ).reshape(1, 24, 7)

    try:
        print("LSTM prediction running")
        print("Sequence shape:", sequence.shape)

        prediction = model(
            sequence,
            training=False
        ).numpy()

        print("Raw prediction:", prediction)

        prediction_scaled = prediction[0][0]

        print("Prediction value:", prediction_scaled)
    except Exception as e:
        print("PREDICTION ERROR:", e)
        return {
            "next_temperature": round(float(temperature) + 1, 1),
            "confidence": 80,
            "model": "Fallback",
            "trend": "Stable",
        }

    dummy = scaled_row.copy()
    dummy[0][0] = prediction_scaled

    predicted_temp = scaler.inverse_transform(dummy)[0][0]

    trend = (
        "Rising"
        if predicted_temp >= temperature
        else "Falling"
    )
    print(f"LSTM prediction completed: {predicted_temp}")

    return {
        "next_temperature": round(float(predicted_temp), 1),
        "confidence": 96,
        "model": "LSTM v1",
        "trend": trend,
    }


if __name__ == "__main__":
    print(
        lstm_forecast(
            temperature=35.0,
            humidity=60,
            aqi=3,
            pm25=40,
            pm10=60,
            co=0.8,
            no2=12,
        )
    )