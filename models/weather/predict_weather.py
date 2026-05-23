from sklearn.ensemble import RandomForestRegressor
import pandas as pd


def forecast(df):

    df = df.copy()

    df["temperature"] = pd.to_numeric(
        df["temperature"],
        errors="coerce"
    )

    df["humidity"] = pd.to_numeric(
        df["humidity"],
        errors="coerce"
    )

    df = df.dropna()

    if len(df) < 20:

        return None

    df["index"] = range(len(df))

    X = df[["index"]]

    y_temp = df["temperature"]

    y_hum = df["humidity"]

    temp_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    hum_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    temp_model.fit(X, y_temp)
    hum_model.fit(X, y_hum)

    future = pd.DataFrame(
        {
            "index":
            range(
                len(df),
                len(df)+24
            )
        }
    )

    return pd.DataFrame({

        "Hour":
        range(1,25),

        "Temperature":
        temp_model.predict(future),

        "Humidity":
        hum_model.predict(future)

    })