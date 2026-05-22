from fastapi import APIRouter
from datetime import datetime
import random

router = APIRouter()

# -------------------------
# STORE WEATHER HISTORY
# -------------------------

weather_history = []


# -------------------------
# WEATHER API
# -------------------------

@router.get("/weather")
def weather():

    new_data = {

        "time": datetime.now().strftime(
            "%H:%M:%S"
        ),

        "temperature": round(
            random.uniform(
                25,
                40
            ),
            1
        ),

        "humidity": random.randint(
            40,
            90
        ),

        "fetched_at": str(
            datetime.now()
        )

    }

    # Save history
    weather_history.append(
        new_data
    )

    # Keep only latest 50 records
    if len(weather_history) > 50:
        weather_history.pop(0)

    return weather_history