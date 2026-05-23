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
    interval=settings.get("refresh", 5) * 1000,
    key="dashboard"
)

# ====================================
# ROOT
# ====================================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ====================================
# PATHS
# ====================================

CSV = ROOT / "data" / "weather_history.csv"

MODEL = (
    ROOT
    / "models"
    / "weather"
    / "weather_model.pkl"
)

ALERT = ROOT / "data" / "alerts.json"

# ====================================
# IMPORTS
# ====================================

from backend.intelligence.urban_score import (
    calculate_score
)

try:

    from backend.intelligence.city_insights import (
        generate_city_insights
    )

except:

    def generate_city_insights(df):
        return {}

try:

    from backend.intelligence.recommendation_engine import (
        get_recommendation
    )

except:

    def get_recommendation(temp, hum):

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


df = load_data()
model = load_model()
alerts = load_alerts()

# ====================================
# CHECK
# ====================================

if df.empty:

    st.warning(
        "Waiting for Producer..."
    )

    st.write(
        "CSV:",
        CSV
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
# FILTER
# ====================================

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

# ====================================
# AI
# ====================================

try:

    prediction = round(

        float(

            model.predict(
                [[latest["humidity"]]]
            )[0]

        ),

        1

    )

except:

    prediction = round(
        latest["temperature"],
        1
    )

rec = get_recommendation(

    latest["temperature"],

    latest["humidity"]

)

recommendation = (

    rec["message"]

    if isinstance(rec, dict)

    else str(rec)

)

urban = calculate_score(

    latest["temperature"],

    latest["humidity"],

    prediction

)

health = urban["score"]

# ====================================
# HERO
# ====================================

left, right = st.columns([5, 1])

with left:

    st.markdown(
        """
<div style="
padding:55px;
border-radius:35px;
background:linear-gradient(135deg,#021224,#0d5a8a);
color:white;
margin-bottom:25px;
">

<div style="
font-size:68px;
font-weight:900;
">

🌍 Urban Dashboard

</div>

<br>

<div style="
font-size:24px;
opacity:.95;
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
padding:30px;
border-radius:18px;
font-size:18px;
font-weight:700;
text-align:center;
margin-top:10px;
">

{IST.strftime("%I:%M:%S %p")}

</div>
""",
        unsafe_allow_html=True
    )
    
# ====================================
# KPI
# ====================================

a,b,c,d,e=st.columns(5)

a.metric(
"🏙 Urban Score",
urban["score"]
)

b.metric(
"🌡 Avg Temp",
f"{latest['temperature']}°C"
)

c.metric(
"💧 Avg Humidity",
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
# ALERT
# ====================================

if alerts:

    st.subheader(
        "🚨 Alerts"
    )

    for a in alerts:

        st.warning(
            a.get(
                "message",
                ""
            )
        )

# ====================================
# RECOMMENDATION
# ====================================

st.subheader(
"🧠 Smart Recommendation"
)

st.info(
recommendation
)

# ====================================
# KPI
# ====================================

a,b,c,d,e=st.columns(5)

a.metric(
"🌡 Temperature",
f"{latest['temperature']}°C"
)

b.metric(
"💧 Humidity",
f"{latest['humidity']}%"
)

c.metric(
"🔮 Prediction",
f"{prediction}°C"
)

d.metric(
"❤️ Health",
f"{health}%"
)

e.metric(
"🏙 Urban Score",
urban["score"]
)

# ====================================
# HEALTH
# ====================================

st.subheader(
"🖥 System Health"
)

st.progress(
health/100
)

# ====================================
# ALERTS
# ====================================

if alerts:

    st.subheader(
        "🚨 Alerts"
    )

    for a in alerts:

        st.warning(
            a.get(
                "message",
                ""
            )
        )

# ====================================
# AI
# ====================================

st.subheader(
"🤖 Recommendation"
)

st.info(
recommendation
)

# ====================================
# CHARTS
# ====================================

left,right=st.columns(2)

with left:

    st.subheader(
        "🌡 Temperature"
    )

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

with right:

    st.subheader(
        "💧 Humidity"
    )

    fig2=go.Figure()

    fig2.add_trace(

        go.Scatter(

            x=plot["time"],

            y=plot["humidity"],

            fill="tozeroy"

        )

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ====================================
# MAP
# ====================================

st.subheader(
"🗺 Urban Digital Twin"
)

m=folium.Map(
location=[20.5,78.9],
zoom_start=5
)

folium.Marker(
location=[16.5,80.64],
popup=recommendation
).add_to(m)

st_folium(
m,
height=450
)

# ====================================
# DATA
# ====================================

st.subheader(
"📄 Live Dataset"
)

st.dataframe(
plot.iloc[::-1],
use_container_width=True
)

# ====================================
# EXPORT
# ====================================

st.subheader(
"⬇ Export Dashboard"
)

file,mime,ext=export_data(
plot
)

st.download_button(
"Download Dashboard Report",
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

### 📌 Dashboard Summary

- Records → {len(df)}
- Prediction → {prediction}°C
- Urban Score → {urban["score"]}
- Health → {health}%
- Export → {settings.get("export")}

"""
)