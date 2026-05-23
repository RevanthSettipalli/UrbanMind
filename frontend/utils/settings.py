import json
import io
import pandas as pd

from pathlib import Path


# ====================================
# PATH
# ====================================

ROOT = Path(__file__).resolve().parents[2]

SETTINGS = ROOT / "data" / "settings.json"


# ====================================
# DEFAULT
# ====================================

DEFAULT = {

    "theme": "Dark",

    "refresh": 10,

    "notify": True,

    "export": "CSV"

}


# ====================================
# LOAD
# ====================================

def load_settings():

    try:

        with open(
            SETTINGS
        ) as f:

            return json.load(
                f
            )

    except:

        return DEFAULT.copy()


# ====================================
# SAVE
# ====================================

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


# ====================================
# THEME
# ====================================

def apply_theme():

    s = load_settings()

    if s["theme"] == "Dark":

        return """
<style>

.stApp{
background:#071320;
color:white;
}

[data-testid="stMetric"]{
background:#0d1f36;
padding:14px;
border-radius:14px;
}

[data-testid="stDataFrame"]{
border-radius:14px;
}

.stButton>button{
border-radius:14px;
}

</style>
"""

    return """
<style>

.stApp{
background:white;
color:black;
}

[data-testid="stMetric"]{
background:#f5f7fb;
padding:14px;
border-radius:14px;
}

</style>
"""


# ====================================
# EXPORT
# ====================================

def export_data(df):

    settings = load_settings()

    mode = settings.get(
        "export",
        "CSV"
    )

    export_df = df.copy()

    # remove timezone for excel compatibility
    for col in export_df.columns:

        try:

            if str(
                export_df[col].dtype
            ).startswith(
                "datetime64[ns,"
            ):

                export_df[col] = (

                    export_df[col]

                    .dt

                    .tz_localize(
                        None
                    )

                )

        except:
            pass


    # CSV
    if mode == "CSV":

        return (

            export_df.to_csv(
                index=False
            ).encode(),

            "text/csv",

            ".csv"

        )


    # JSON
    elif mode == "JSON":

        return (

            export_df.to_json(
                orient="records"
            ).encode(),

            "application/json",

            ".json"

        )


    # EXCEL
    elif mode == "Excel":

        output = io.BytesIO()

        with pd.ExcelWriter(

            output,

            engine="openpyxl"

        ) as writer:

            export_df.to_excel(

                writer,

                index=False

            )

        return (

            output.getvalue(),

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            ".xlsx"

        )


    # FALLBACK
    return (

        export_df.to_csv(
            index=False
        ).encode(),

        "text/csv",

        ".csv"

    )