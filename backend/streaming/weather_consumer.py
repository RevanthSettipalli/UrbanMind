import requests
import pandas as pd
import time
import os


API = "http://127.0.0.1:8000/weather"

FILE = "data/weather_history.csv"


while True:

    try:

        response = requests.get(API)

        data = response.json()

        new_df = pd.DataFrame(data)

        if os.path.exists(FILE):

            try:
                old_df = pd.read_csv(FILE)

                final_df = pd.concat(
                    [old_df, new_df],
                    ignore_index=True
                )

            except:
                final_df = new_df

        else:

            final_df = new_df


        final_df.to_csv(
            FILE,
            index=False
        )

        print("Saved")


    except Exception as e:

        print("Error:", e)


    time.sleep(5)