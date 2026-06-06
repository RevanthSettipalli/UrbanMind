import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score


# ====================================
# PATHS
# ====================================

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data" / "processed_weather.csv"

MODEL = ROOT / "models" / "weather" / "weather_model.pkl"


try:

    print("\nLoading Dataset...\n")

    df = pd.read_csv(DATA)

    if len(df) < 300:
        raise Exception(
            "Need at least 300 records"
        )


    # ====================================
    # CLEAN
    # ====================================

    df = df.dropna()

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    df = df.dropna()


    # ====================================
    # FEATURE ENGINEERING
    # ====================================

    df["hour"] = df["time"].dt.hour

    df["day"] = df["time"].dt.day

    df["month"] = df["time"].dt.month


    # Temperature history

    df["temp_prev"] = (
        df["temperature"]
        .shift(1)
    )

    df["temp_avg"] = (
        df["temperature"]
        .rolling(5)
        .mean()
    )


    df = df.dropna()


    # ====================================
    # FEATURES
    # ====================================

    FEATURES = [

        "humidity",

        "hour",

        "day",

        "month",

        "temp_prev",

        "temp_avg"
    ]


    X = df[
        FEATURES
    ]

    y = df[
        "temperature"
    ]


    # ====================================
    # SPLIT
    # ====================================

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=42
    )


    # ====================================
    # MODEL
    # ====================================

    model = RandomForestRegressor(

        n_estimators=1000,

        max_depth=20,

        min_samples_split=4,

        min_samples_leaf=2,

        max_features="sqrt",

        random_state=42,

        n_jobs=-1
    )


    # ====================================
    # TRAIN
    # ====================================

    model.fit(

        X_train,

        y_train
    )


    pred = model.predict(

        X_test
    )


    score = r2_score(

        y_test,

        pred
    )


    # ====================================
    # SAVE
    # ====================================

    MODEL.parent.mkdir(

        parents=True,

        exist_ok=True
    )


    joblib.dump(

        model,

        MODEL
    )


    # ====================================
    # RESULT
    # ====================================

    print()

    print("✅ Model Trained")

    print()

    print(
        f"Dataset: {len(df)} rows"
    )

    print()

    print(
        f"Accuracy: {score*100:.2f}%"
    )

    print()

    if score > 0.80:

        print(
            "🏆 Excellent Model"
        )

    elif score > 0.60:

        print(
            "✅ Good Model"
        )

    else:

        print(
            "⚠ Collect more data"
        )


except Exception as e:

    print()

    print(
        "❌ Training Error"
    )

    print()

    print(e)