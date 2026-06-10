

import numpy as np
import pandas as pd

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense
    from sklearn.preprocessing import MinMaxScaler
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False


def forecast_lstm(df, target_column="temperature", forecast_days=30):
    """
    LSTM forecasting engine for UrbanMind.
    Returns future predictions and model status.
    """

    try:
        if not TF_AVAILABLE:
            return {
                "forecast": [],
                "model": "LSTM Unavailable",
                "rmse": 0
            }

        if target_column not in df.columns:
            return {
                "forecast": [],
                "model": "Invalid Target",
                "rmse": 0
            }

        series = pd.to_numeric(
            df[target_column],
            errors="coerce"
        ).dropna()

        if len(series) < 50:
            return {
                "forecast": [],
                "model": "Insufficient Data",
                "rmse": 0
            }

        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(
            series.values.reshape(-1, 1)
        )

        X = []
        y = []

        lookback = 10

        for i in range(lookback, len(scaled)):
            X.append(scaled[i-lookback:i, 0])
            y.append(scaled[i, 0])

        X = np.array(X)
        y = np.array(y)

        X = X.reshape(
            X.shape[0],
            X.shape[1],
            1
        )

        model = Sequential([
            LSTM(32, input_shape=(lookback, 1)),
            Dense(16, activation="relu"),
            Dense(1)
        ])

        model.compile(
            optimizer="adam",
            loss="mse"
        )

        model.fit(
            X,
            y,
            epochs=10,
            batch_size=8,
            verbose=0
        )

        window = scaled[-lookback:].flatten()
        future = []

        for _ in range(forecast_days):
            x_input = window.reshape(1, lookback, 1)

            pred = model.predict(
                x_input,
                verbose=0
            )[0][0]

            future.append(pred)

            window = np.append(
                window[1:],
                pred
            )

        forecast = scaler.inverse_transform(
            np.array(future).reshape(-1, 1)
        ).flatten()

        return {
            "forecast": forecast.tolist(),
            "model": "LSTM",
            "rmse": round(float(model.evaluate(X, y, verbose=0)), 4)
        }

    except Exception as e:
        return {
            "forecast": [],
            "model": f"Error: {str(e)}",
            "rmse": 0
        }