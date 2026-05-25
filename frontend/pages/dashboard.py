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

from frontend.utils.city_selector import city_filter
from utils.auth_guard import require_login
from utils.sidebar import render_sidebar
from utils.settings import (
    apply_theme,
    load_settings,
    export_data
)

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

st_autorefresh(
    interval=1000,
    key="live_dashboard_clock"
)

# ====================================
# ROOT
# ====================================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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

try:

    from backend.intelligence.recommendation_engine import (
        get_recommendation
    )

except:

    def get_recommendation(
        temp,
        hum
    ):

        if temp >= 42:
            return {
                "message":
                "🔥 Extreme Heat Alert"
            }

        if hum >= 85:
            return {
                "message":
                "🌧 Flood Risk"
            }

        return {
            "message":
            "✅ Conditions Stable"
        }

# ====================================
# LOAD
# ====================================

@st.cache_data(ttl=5)
def load_data():

    try:

        if CSV.exists():

            return pd.read_csv(
                CSV,
                on_bad_lines="skip"
            )

    except:
        pass

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

df, selected_city = city_filter(df)

model = load_model()

alerts = load_alerts()

if df.empty:

    st.warning(
        "Waiting for Producer..."
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

latest = plot.iloc[-1]

# ====================================
# TIME
# ====================================

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

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

rec = get_recommendation(

    latest[
        "temperature"
    ],

    latest[
        "humidity"
    ]

)

recommendation = rec["message"]

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

# ====================================
# HERO
# ====================================

left, right = st.columns([8, 1.5])

with left:

    st.markdown(
        """
<div style="
padding:55px;
height:260px;
border-radius:30px;
background:linear-gradient(135deg,#021224,#0d5a8a);
color:white;
display:flex;
flex-direction:column;
justify-content:center;
">

<div style="
font-size:72px;
font-weight:900;
">
🌍 Urban Dashboard
</div>

<div style="
font-size:24px;
margin-top:15px;
">
Advanced Intelligence • Ranking • Geo Analysis
</div>

</div>
""",
        unsafe_allow_html=True
    )

with right:

    st.markdown(
        f"""
<div style="
background:#dfe8f5;
height:260px;
border-radius:22px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
text-align:center;
padding:18px;
">

<div style="
font-size:42px;
margin-bottom:12px;
line-height:1;
">
🕒
</div>

<div style="
font-size:26px;
font-weight:800;
color:#124f9d;
line-height:1.1;
white-space:nowrap;
">
{current_time}
</div>

<div style="
margin-top:8px;
font-size:15px;
color:#5a6572;
line-height:1;
">
Live Time
</div>

</div>
""",
        unsafe_allow_html=True
    )

# ====================================
# KPI
# ====================================

a,b,c,d,e = st.columns(5)

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
"📄 Records",
len(df)
)

e.metric(
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

l,r=st.columns(2)

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

# ====================================
# DIGITAL TWIN
# ====================================

st.subheader(
"🗺 Urban Digital Twin"
)

CITY = {

"Delhi":[28.61,77.20],

"Mumbai":[19.07,72.87],

"Hyderabad":[17.38,78.48],

"Chennai":[13.08,80.27],

"Bangalore":[12.97,77.59],

"Kolkata":[22.57,88.36],

"Vijayawada":[16.50,80.64],

"Pune":[18.52,73.85],

"Ahmedabad":[23.02,72.57],

"Jaipur":[26.91,75.78]

}

coords = CITY.get(
latest["city"],
[20.5,78.9]
)

m = folium.Map(
location=coords,
zoom_start=8
)

folium.Marker(

location=coords,

tooltip=
latest["city"],

popup=f"""
City:
{latest["city"]}

Temp:
{latest["temperature"]}

Humidity:
{latest["humidity"]}

{recommendation}
"""

).add_to(m)

st_folium(
m,
height=550
)

# ====================================
# DATA
# ====================================

st.subheader(
"📄 Dataset"
)

st.dataframe(
plot.iloc[::-1],
use_container_width=True
)

# ====================================
# EXPORT
# ====================================

file,mime,ext = export_data(
plot
)

st.download_button(

"⬇ Download Report",

file,

f"urbanmind{ext}",

mime,

use_container_width=True
)

# ====================================
# SUMMARY
# ====================================

st.markdown(
f"""

### 📌 Summary

Records:
{len(df)}

Prediction:
{prediction}°C

Urban Score:
{urban["score"]}

Health:
{health}%

"""
)