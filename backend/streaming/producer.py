import pandas as pd
import time
import os

path = "../../data/weather_stream.csv"

while True:

    row = {
        "city": "Hyderabad",
        "temperature": 30,
        "humidity": 60,
        "time": pd.Timestamp.now()
    }

    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame()

    df = pd.concat(
        [df, pd.DataFrame([row])],
        ignore_index=True
    )

    df.to_csv(
        path,
        index=False
    )

    print(row)

    time.sleep(5)