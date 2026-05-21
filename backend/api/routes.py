from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/weather")

def weather():

    df = pd.read_csv(
        "data/processed/weather_clean.csv"
    )

    return df.to_dict(
        orient="records"
    )