import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
from sqlalchemy import create_engine
import os
import folium
import pytz
import json
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from datetime import datetime

from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

from frontend.utils.city_selector import city_filter
from frontend.utils.auth_guard import require_login
from frontend.utils.sidebar import render_sidebar
from frontend.utils.settings import (
    apply_theme,
    load_settings,
    export_data
)

# ====================================
# DASHBOARD COMPONENTS
# ====================================
from frontend.dashboard_components.hero import render_hero
from frontend.dashboard_components.executive_center import render_executive_center
from frontend.dashboard_components.national_center import render_national_center
from frontend.dashboard_components.governance_ai import render_governance_ai
from frontend.dashboard_components.alert_center import render_alert_center
from frontend.dashboard_components.rankings import render_rankings
from frontend.dashboard_components.analytics import render_analytics
from frontend.dashboard_components.intelligence import render_intelligence
from frontend.dashboard_components.digital_twin import render_digital_twin
from frontend.dashboard_components.copilot import render_copilot

# ====================================
# PAGE
# ====================================

st.set_page_config(
    page_title="UrbanMind Dashboard",
    page_icon="🌍",
    layout="wide"
)

require_login()
render_sidebar()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

settings = load_settings()

# ====================================
# AUTO REFRESH
# ====================================

refresh_rate = max(
    1,
    int(settings.get("refresh_rate", 60))
)

st_autorefresh(
    interval=refresh_rate * 1000,
    key=f"live_dashboard_clock_{refresh_rate}"
)

# ====================================
# ROOT
# ====================================

CSV = ROOT / "data" / "processed_weather.csv"

MODEL = (
    ROOT
    / "models"
    / "weather"
    / "weather_model.pkl"
)

ALERT = (
    ROOT
    / "data"
    / "alerts.json"
)

# ====================================
# IMPORTS
# ====================================

from backend.intelligence.urban_score import (
    calculate_score
)

from backend.intelligence.risk_engine import (
    calculate_risk
)


# Urban Anomaly Detection Engine
try:

    from backend.intelligence.anomaly_engine import (
        detect_anomalies
    )

except Exception as e:

    st.error(f"Anomaly Engine Import Error: {e}")

    def detect_anomalies(data):
        return []



# AI Forecast Engine
from backend.intelligence.forecast_ai import (
    forecast_city
)

# Predictive Analytics Engine
try:

    from backend.intelligence.predictive_analytics import (
        predictive_report
    )

except Exception:

    try:

        import importlib.util

        predictive_path = (
            ROOT
            / "backend"
            / "intelligence"
            / "predictive_analytics.py"
        )

        spec = importlib.util.spec_from_file_location(
            "predictive_analytics",
            predictive_path
        )

        predictive_module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(
            predictive_module
        )

        predictive_report = (
            predictive_module.predictive_report
        )

    except Exception as e:

        st.error(
            f"Predictive Analytics Import Error: {e}"
        )

        def predictive_report(
            score,
            aqi
        ):

            return {
                "urban_score_forecast": score,
                "aqi_forecast": aqi,
                "risk_forecast": "UNKNOWN",
                "warning": "Predictive Analytics unavailable"
            }


# Executive AI Engine
try:

    from backend.intelligence.executive_ai import (
        generate_executive_report
    )

except Exception as e:

    st.error(
        f"Executive AI Import Error: {e}"
    )

    def generate_executive_report(
        city,
        score,
        heat_risk,
        pollution_risk,
        urban_risk
    ):

        return {
            "summary": "Executive AI unavailable",
            "action": "No action available"
        }

try:

    from backend.intelligence.recommendation_engine import (
        get_recommendation
    )

    # Recommendation engine loaded

except Exception as e:

    st.error(f"Recommendation Engine Import Error: {e}")

    def get_recommendation(
        temp,
        hum,
        aqi=1,
        pm25=0,
        pm10=0,
        co=0,
        no2=0,
        score=100
    ):

        return {
            "message": "⚠ Recommendation Engine Unavailable"
        }

# ====================================
# LOAD
# ====================================

@st.cache_data(ttl=5)
def load_data():

    try:

        db_url = os.getenv("DATABASE_URL")

        if db_url:

            engine = create_engine(db_url)

            return pd.read_sql(
                """
                SELECT *
                FROM weather_data
                ORDER BY time DESC
                """,
                engine
            )

        if CSV.exists():

            return pd.read_csv(
                CSV,
                on_bad_lines="skip"
            )

    except Exception as e:

        st.error(f"Database Error: {e}")

    return pd.DataFrame()


@st.cache_resource
def load_model():

    try:

        if MODEL.exists():

            return joblib.load(
                MODEL
            )

    except:
        pass

    return None


def load_alerts():

    try:

        if ALERT.exists():

            with open(ALERT) as f:
                return json.load(f)

    except:
        pass

    return []


# ====================================
# DATA
# ====================================

df = load_data()

data_age_seconds = 0
last_dataset_update = "Unavailable"

try:
    if CSV.exists():
        data_age_seconds = int(
            datetime.now().timestamp() - CSV.stat().st_mtime
        )

        last_dataset_update = datetime.fromtimestamp(
            CSV.stat().st_mtime
        ).strftime("%d %b %Y %I:%M:%S %p")
except Exception:
    pass

df, selected_city = city_filter(df)

model = load_model()

alerts = load_alerts()

if df.empty:

    st.error(
        "No data found in PostgreSQL database"
    )

    st.stop()

# ====================================
# CLEAN
# ====================================

if "time" in df.columns:

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

df = df.dropna()

# ====================================
# SINGLE FILTER
# ====================================

city = selected_city

plot = df.tail(40)

if city == "All Cities":

    latest_cities = (
        df
        .groupby("city")
        .tail(1)
    )

    latest = pd.Series({

        "temperature":
        latest_cities["temperature"].mean(),

        "humidity":
        latest_cities["humidity"].mean(),

        "aqi":
        latest_cities["aqi"].mean(),

        "pm25":
        latest_cities["pm25"].mean(),

        "pm10":
        latest_cities["pm10"].mean(),

        "co":
        latest_cities["co"].mean(),

        "no2":
        latest_cities["no2"].mean()

    })

else:

    latest = (
        df[df["city"] == city]
        .tail(1)
        .iloc[0]
    )

# ====================================
# TIME
# ====================================

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

updated_time = IST.strftime(
    "%d %b %Y"
)

updated_clock = IST.strftime(
    "%I:%M:%S %p"
).replace(" AM", "AM").replace(" PM", "PM")

current_time = IST.strftime(
    "%I:%M:%S %p"
).replace(" AM", "AM").replace(" PM", "PM")

# ====================================
# AI
# ====================================

try:

    prediction = round(

        float(

            model.predict(

                [[
                    latest[
                        "humidity"
                    ]
                ]]

            )[0]

        ),

        1

    )

except:

    prediction = round(
        latest[
            "temperature"
        ],
        1
    )

urban = calculate_score(

    latest[
        "temperature"
    ],

    latest[
        "humidity"
    ],

    prediction,

    latest[
        "aqi"
    ],

    latest[
        "pm25"
    ],

    latest[
        "pm10"
    ],

    latest[
        "co"
    ],

    latest[
        "no2"
    ]

)

rec = get_recommendation(

    latest[
        "temperature"
    ],

    latest[
        "humidity"
    ],

    latest[
        "aqi"
    ],

    latest[
        "pm25"
    ],

    latest[
        "pm10"
    ],

    latest[
        "co"
    ],

    latest[
        "no2"
    ],

    urban["score"]

)

recommendation = rec.get(
    "message",
    "No recommendation available"
)

health = urban["score"]

# ====================================
# CITY RANKINGS
# ====================================

city_scores = []

for city_name in df["city"].unique():

    city_df = df[df["city"] == city_name]

    row = city_df.tail(1).iloc[0]

    score = calculate_score(
        row["temperature"],
        row["humidity"],
        prediction,
        row["aqi"],
        row["pm25"],
        row["pm10"],
        row["co"],
        row["no2"]
    )["score"]

    city_scores.append({
        "City": city_name,
        "Score": score
    })

ranking_df = pd.DataFrame(city_scores)

ranking_df = ranking_df.sort_values(
    "Score",
    ascending=False
)

render_hero(current_time)

st.subheader("📡 Data Freshness Center")

f1, f2, f3, f4 = st.columns(4)

f1.metric(
    "🕒 Last Update",
    last_dataset_update.split()[-2] + " " + last_dataset_update.split()[-1]
    if last_dataset_update != "Unavailable"
    else "N/A"
)

f2.metric(
    "⚡ Data Age",
    f"{data_age_seconds}s"
)

f3.metric(
    "📄 Records",
    len(df)
)

f4.metric(
    "🔄 Refresh",
    f"{refresh_rate}s"
)

render_executive_center(df, ranking_df, alerts)

render_national_center(df, ranking_df)

render_governance_ai(df, ranking_df)


render_alert_center(
    plot,
    alerts,
    latest,
    urban,
    selected_city,
    detect_anomalies,
    calculate_risk,
    generate_executive_report
)

# ====================================
# KPI
# ====================================

a,b,c,d,e,f = st.columns(6)

aqi_value = latest["aqi"] if "aqi" in latest.index else "N/A"

a.metric(
"🏙 Score",
urban["score"]
)

b.metric(
"🌡 Temp",
f"{latest['temperature']}°C"
)

c.metric(
"💧 Humidity",
f"{latest['humidity']}%"
)

d.metric(
"🌫 AQI",
aqi_value
)

e.metric(
"📄 Records",
len(df)
)

f.metric(
"🔮 Prediction",
f"{prediction}°C"
)

# ====================================
# HEALTH
# ====================================

st.subheader(
"🩺 Urban Health"
)

st.progress(
health/100
)


pollution_rows = []
for city_name in df["city"].unique():
    city_df = df[df["city"] == city_name]
    row = city_df.tail(1).iloc[0]
    pollution_score = (
        float(row.get("aqi", 0))
        + float(row.get("pm25", 0))
        + float(row.get("pm10", 0))
        + float(row.get("co", 0))
        + float(row.get("no2", 0))
    )
    pollution_rows.append({
        "City": city_name,
        "Pollution": round(pollution_score, 2)
    })
pollution_df = pd.DataFrame(pollution_rows)
pollution_df = pollution_df.sort_values(
    "Pollution",
    ascending=False
)
render_rankings(
    df,
    ranking_df,
    prediction
)

# ====================================
# RECOMMEND
# ====================================

st.subheader(
"🧠 Smart Recommendation"
)

st.info(
recommendation
)

# ====================================
# CHARTS
# ====================================

l,r,x = st.columns(3)

with l:

    fig=go.Figure()

    fig.add_trace(

        go.Scatter(

            x=plot["time"],

            y=plot["temperature"],

            fill="tozeroy"

        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with r:

    fig=go.Figure()

    fig.add_trace(

        go.Scatter(

            x=plot["time"],

            y=plot["humidity"],

            fill="tozeroy"

        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
