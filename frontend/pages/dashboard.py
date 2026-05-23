import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import folium
import pytz
import json
import sys

from pathlib import Path
from datetime import datetime
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar

# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="UrbanMind Dashboard",
    page_icon="🌍",
    layout="wide"
)

require_login()

render_sidebar()

# =====================================
# ROOT
# =====================================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# =====================================
# IMPORT
# =====================================

from backend.intelligence.urban_score import calculate_score

try:

    from prediction.recommendation_engine import (
        get_recommendation
    )

except:

    def get_recommendation(
        temp,
        hum
    ):

        if temp >= 40:
            return "🔥 Heat Alert"

        elif hum >= 90:
            return "🌊 Flood Risk"

        return "✅ Safe Conditions"

# =====================================
# REFRESH
# =====================================

st_autorefresh(
    interval=5000,
    key="dashboard"
)

# =====================================
# PATHS
# =====================================

CSV = ROOT / "data" / "weather_history.csv"

MODEL = ROOT / "models" / "weather" / "weather_model.pkl"

ALERT = ROOT / "data" / "alerts.json"

# =====================================
# LOAD
# =====================================

@st.cache_data(ttl=5)
def load_data():

    try:

        return pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

    except:

        return pd.DataFrame()

@st.cache_resource
def load_model():

    try:

        return joblib.load(
            MODEL
        )

    except:

        return None

def load_alerts():

    try:

        with open(ALERT) as f:

            return json.load(
                f
            )

    except:

        return []

df = load_data()

model = load_model()

alerts = load_alerts()

if df.empty:

    st.warning(
        "Waiting for Producer..."
    )

    st.stop()

# =====================================
# CLEAN
# =====================================

for c in [

"time",
"temperature",
"humidity"

]:

    if c not in df:
        df[c] = 0

df["time"] = pd.to_datetime(
    df["time"],
    errors="coerce"
)

df["temperature"] = pd.to_numeric(
    df["temperature"],
    errors="coerce"
)

df["humidity"] = pd.to_numeric(
    df["humidity"],
    errors="coerce"
)

df = df.dropna()

# =====================================
# FILTER
# =====================================

if "city" in df.columns:

    city = st.selectbox(

        "🏙 Select City",

        ["All Cities"]

        +

        sorted(
            df["city"]
            .astype(str)
            .unique()
        )

    )

    if city != "All Cities":

        df = df[
            df["city"]
            ==
            city
        ]

if len(df) == 0:

    st.warning(
        "No records available"
    )

    st.stop()

plot = df.tail(40)

latest = plot.iloc[-1]

# =====================================
# TIME
# =====================================

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

# =====================================
# AI
# =====================================

try:

    prediction = round(

        float(

            model.predict([[

                latest[
                    "humidity"
                ]

            ]])[0]

        ),

        1

    )

except:

    prediction = round(

        float(

            latest[
                "temperature"
            ]

        ),

        1

    )

recommendation = get_recommendation(

latest[
"temperature"
],

latest[
"humidity"
]

)

urban = calculate_score(

latest[
"temperature"
],

latest[
"humidity"
],

prediction

)

health = urban["score"]

# =====================================
# HEADER
# =====================================

left,right = st.columns([4,1])

with left:

    st.title(
        "🌍 UrbanMind Dashboard"
    )

with right:

    st.info(
        IST.strftime(
            "%I:%M:%S %p"
        )
    )

# =====================================
# KPI
# =====================================

a,b,c,d,e = st.columns(5)

a.metric(
"Temperature",
f"{latest['temperature']}°C"
)

b.metric(
"Humidity",
f"{latest['humidity']}%"
)

c.metric(
"Prediction",
f"{prediction}°C"
)

d.metric(
"Health",
f"{health}%"
)

e.metric(
"Urban Score",
urban["score"]
)

# =====================================
# HEALTH
# =====================================

st.subheader(
"🖥 System Health"
)

st.progress(
health/100
)

# =====================================
# ALERTS
# =====================================

if alerts:

    st.subheader(
        "🚨 Alerts"
    )

    for alert in alerts:

        st.warning(

            alert.get(
                "message",
                ""
            )

        )

# =====================================
# RECOMMENDATION
# =====================================

st.subheader(
"🤖 Recommendation"
)

st.info(
recommendation
)

# =====================================
# CHARTS
# =====================================

left,right = st.columns(2)

with left:

    fig = go.Figure()

    fig.add_trace(

go.Scatter(

x=plot["time"],

y=plot["temperature"]

)

)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig2 = go.Figure()

    fig2.add_trace(

go.Scatter(

x=plot["time"],

y=plot["humidity"]

)

)

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================
# MAP
# =====================================

st.subheader(
"🗺 Urban Digital Twin"
)

m = folium.Map(

location=[
20.5,
78.9
],

zoom_start=5

)

folium.CircleMarker(

location=[
16.5,
80.64
],

radius=18,

popup=
recommendation,

fill=True

).add_to(
m
)

st_folium(

m,

height=450,

key="dashboard_map"

)

# =====================================
# DATA
# =====================================

st.subheader(
"📄 Live Dataset"
)

st.dataframe(

plot.iloc[::-1],

use_container_width=True

)

# =====================================
# SUMMARY
# =====================================

st.success(
f"""
Records:
{len(df)}

Prediction:
{prediction}

Urban Score:
{urban["score"]}
"""
)