import json
import io
import pandas as pd

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SETTINGS = ROOT / "frontend" / "settings.json"


DEFAULT = {

    "theme": "Dark",

    "refresh_rate": 10,

    "notify": True,

    "export": "CSV"

}


def load_settings():

    try:

        with open(SETTINGS) as f:

            data = json.load(f)

        if "refresh" in data and "refresh_rate" not in data:
            data["refresh_rate"] = data.pop("refresh")

        return {
            **DEFAULT,
            **data
        }

    except:

        return DEFAULT.copy()


def save_settings(data):

    SETTINGS.parent.mkdir(
        exist_ok=True
    )

    with open(
        SETTINGS,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def apply_theme():

    s = load_settings()

    if s.get("theme") == "Dark":

        return """
<style>

.stApp{
background:#071320;
color:white;
}

</style>
"""

    return """
<style>

.stApp{
background:#f5f7fb;
color:black;
}

</style>
"""


def export_data(df):

    mode = load_settings().get(
        "export",
        "CSV"
    )

    if mode == "JSON":

        return (
            df.to_json(
                orient="records"
            ).encode(),
            "application/json",
            ".json"
        )

    if mode == "Excel":

        output = io.BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                index=False
            )

        return (
            output.getvalue(),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xlsx"
        )

    return (

        df.to_csv(
            index=False
        ).encode(),

        "text/csv",

        ".csv"

    )