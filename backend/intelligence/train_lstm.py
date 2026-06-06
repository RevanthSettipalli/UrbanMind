import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

DATA_PATH = "data/weather_stream.csv"
MODEL_PATH = "backend/models/lstm_weather.keras"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")
    return df


def create_sequences(data, sequence_length=24):
    X, y = [], []

    for i in range(sequence_length, len(data)):
        X.append(data[i - sequence_length:i])
        y.append(data[i, 0])

    return np.array(X), np.array(y)


def train_lstm_model():
    df = load_data()

    features = [
        "temperature",
        "humidity",
        "aqi",
        "pm25",
        "pm10",
        "co",
        "no2",
    ]

    dataset = df[features].astype(float)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(dataset)

    joblib.dump(
        scaler,
        "backend/models/lstm_scaler.pkl"
    )

    X, y = create_sequences(scaled, sequence_length=24)

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(16, activation="relu"),
        Dense(1)
    ])

    model.compile(
        optimizer="adam",
        loss="mse",
        metrics=["mae"]
    )

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    model.fit(
        X,
        y,
        epochs=25,
        batch_size=32,
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=1,
    )

    model.save(MODEL_PATH)

    print("Scaler saved to: backend/models/lstm_scaler.pkl")
    print(f"LSTM model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_lstm_model()