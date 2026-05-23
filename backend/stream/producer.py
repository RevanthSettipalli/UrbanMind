import pandas as pd
import random
import time

from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT/"data"/"weather_history.csv"


cities = [

"Delhi",
"Mumbai",
"Hyderabad",
"Chennai",
"Bangalore",
"Vijayawada"

]


print(
"\nUrbanMind Producer Started\n"
)


while True:

    row={

        "time":
        datetime.now(),

        "city":
        random.choice(
            cities
        ),

        "temperature":
        round(
            random.uniform(
                22,
                45
            ),
            1
        ),

        "humidity":
        random.randint(
            35,
            90
        )

    }

    df=pd.DataFrame(
        [row]
    )

    write_header = (

        not CSV.exists()

    )

    df.to_csv(

        CSV,

        mode="a",

        header=write_header,

        index=False

    )

    print(
        row
    )

    time.sleep(
        2
    )