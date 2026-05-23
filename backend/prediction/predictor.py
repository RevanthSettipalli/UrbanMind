import joblib
import numpy as np


MODEL = "models/weather/weather_model.pkl"


def predict_temperature(humidity):

    model = joblib.load(MODEL)

    value = model.predict(
        np.array([[humidity]])
    )[0]

    return round(float(value), 2)