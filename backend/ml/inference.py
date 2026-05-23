import joblib
import numpy as np
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

MODEL = (
ROOT
/
"models"
/
"weather"
/
"weather_model.pkl"
)


model = joblib.load(
MODEL
)


def predict_temperature(
humidity,
hour,
day,
month,
current_temp,
avg_temp
):

    x=np.array([[
        humidity,
        hour,
        day,
        month,
        avg_temp
    ]])

    value=model.predict(
        x
    )[0]

    return round(
        float(value),
        1
    )


if __name__=="__main__":

    print(

predict_temperature(

70,
12,
20,
5,
32,
31

)

)