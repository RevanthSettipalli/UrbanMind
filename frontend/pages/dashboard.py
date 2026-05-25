import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import joblib
import folium
import pytz
import json
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

refresh_rate = max(
    1,
    int(
        settings.get(
            "refresh_rate",
            1
        )
    )
)

# ====================================
# AUTO REFRESH
# ====================================

st_autorefresh(
    interval=refresh_rate * 1000,
    key=f"live_dashboard_clock_{refresh_rate}"
)


LIVE_CSV = ROOT / "data" / "weather_stream.csv"
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

@st.cache_data(ttl=0)
def load_data():

    try:

        if LIVE_CSV.exists():
            return pd.read_csv(
                LIVE_CSV,
                on_bad_lines="skip"
            )

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

if df.empty:

    st.warning("Waiting for live stream data...")

    try:

        if LIVE_CSV.exists():
            df = pd.read_csv(LIVE_CSV)

        elif CSV.exists():
            df = pd.read_csv(CSV)

        else:
            st.stop()

    except Exception:
        st.stop()

else:

    st.success(f"🟢 Live Stream Connected • {len(df)} records")

if not df.empty:
    df, selected_city = city_filter(df)
else:
    selected_city = "All Cities"

model = load_model()
alerts = load_alerts()

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

plot = (
    df
    if city == "All Cities"
    else df[
        df["city"]
        ==
        city
    ]
).tail(40)

if plot.empty:
    st.warning("No weather records available.")
    st.stop()

latest = plot.iloc[-1]

# ====================================
# TIME
# ====================================

IST = pd.Timestamp.now(
    tz="Asia/Kolkata"
).to_pydatetime()

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

    components.html(
        f"""
<div style='
background:#dfe8f5;
height:260px;
border-radius:22px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
text-align:center;
padding:18px;
'>

<div style='font-size:42px;'>🕒</div>

<div
id='urban_clock'
style='
font-size:26px;
font-weight:800;
color:#124f9d;
margin-top:10px;
'>
{current_time}
</div>

<div
style='
margin-top:8px;
font-size:15px;
color:#5a6572;
'>
Live Time
</div>

</div>

<script>
function tick() {{
const d = new Date();
let h = d.getHours();
const ap = h >= 12 ? 'PM' : 'AM';
h = h % 12 || 12;
const m = String(d.getMinutes()).padStart(2,'0');
const s = String(d.getSeconds()).padStart(2,'0');
document.getElementById('urban_clock').innerText =
`${{String(h).padStart(2,'0')}}:${{m}}:${{s}}${{ap}}`;
}}

tick();
setInterval(tick,1000);
</script>
        """,
        height=260
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

rank = (
    df
    .groupby("city")
    .agg({
        "temperature":"mean",
        "humidity":"mean"
    })
    .round(1)
    .reset_index()
)

rank["health"] = rank.apply(
    lambda r: calculate_score(
        r["temperature"],
        r["humidity"],
        r["temperature"]
    )["score"],
    axis=1
)

rank["risk"] = rank.apply(
    lambda r:
    "🔥 Heat Risk"
    if r["temperature"] >= 40
    else (
        "🌧 Flood Risk"
        if r["humidity"] >= 85
        else "✅ Stable"
    ),
    axis=1
)

rank["color"] = rank["health"].apply(
    lambda x:
    "green"
    if x >= 90
    else (
        "orange"
        if x >= 75
        else "red"
    )
)

m = folium.Map(
location=[21,79],
zoom_start=5,
tiles="CartoDB positron"
)

if city == "All Cities":
    map_data = rank
else:
    map_data = rank[
        rank["city"] == city
    ]

for _, r in map_data.iterrows():

    city_name = str(r["city"])

    if city_name in CITY:

        folium.CircleMarker(
            location=CITY[city_name],
            radius=18,
            fill=True,
            fill_opacity=.9,
            color=r["color"],
            fill_color=r["color"],
            tooltip=city_name,
            popup=f"""
🏙 {city_name}

❤️ Health: {r['health']:.0f}

🌡 Temp: {r['temperature']:.1f}°C

💧 Humidity: {r['humidity']:.1f}%

⚠ Recommendation:
{get_recommendation(r['temperature'], r['humidity'])['message']}
"""
        ).add_to(m)

st_folium(
m,
height=450,
width="stretch"
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