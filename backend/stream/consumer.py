import pandas as pd

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT/"data"/"weather_history.csv"


while True:

    try:

        df=pd.read_csv(
            CSV
        )

        print(
            "\nLatest\n"
        )

        print(
            df.tail(
                5
            )
        )

    except:

        print(
            "Waiting..."
        )