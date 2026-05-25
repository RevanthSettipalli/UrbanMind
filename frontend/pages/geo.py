import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
    
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import pytz

from pathlib import Path
from datetime import datetime
from streamlit_folium import st_folium

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar
from utils.settings import (
    apply_theme,
    load_settings,
    export_data
)

from backend.intelligence.geo_engine import (
    calculate_risk
)

# ==================================
# PAGE
# ==================================

st.set_page_config(
    page_title="Geo Intelligence",
    page_icon="🌍",
    layout="wide"
)

require_login()

render_sidebar()

settings = load_settings()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

refresh_rate = max(
    1,
    int(
        settings.get(
            "refresh_rate",
            10
        )
    )
)

st_autorefresh(
    interval=refresh_rate * 1000,
    key=f"geo_live_clock_{refresh_rate}"
)

# ==================================
# STYLE
# ==================================

st.markdown("""
<style>

.block-container{
padding-top:.4rem!important;
}

.hero{
padding:40px;

border-radius:30px;

background:
linear-gradient(
135deg,
#03283c,
#0096c7
);

color:white;

margin-bottom:25px;
}

.hero h1{
font-size:56px;
margin:0;
}

</style>
""",
unsafe_allow_html=True)

CSV = ROOT / "data" / "processed_weather.csv"

CITY = {
    "Delhi": [28.61, 77.20],
    "Mumbai": [19.07, 72.87],
    "Hyderabad": [17.38, 78.48],
    "Chennai": [13.08, 80.27],
    "Bangalore": [12.97, 77.59],
    "Kolkata": [22.57, 88.36],
    "Vijayawada": [16.50, 80.64],
    "Pune": [18.52, 73.85],
    "Ahmedabad": [23.02, 72.57],
    "Jaipur": [26.91, 75.78]
}

EXPECTED_CITIES = list(CITY.keys())

# ==================================
# LOAD
# ==================================

@st.cache_data(ttl=0)
def load():

    try:

        df = pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

        return df

    except Exception:

        return pd.DataFrame()


df = load()

if df.empty:

    st.warning(
        "Waiting for Geo Stream..."
    )

    st.stop()

# ==================================
# CLEAN
# ==================================

if "temperature" in df.columns:

    df["temperature"] = pd.to_numeric(
        df["temperature"],
        errors="coerce"
    )

if "humidity" in df.columns:

    df["humidity"] = pd.to_numeric(
        df["humidity"],
        errors="coerce"
    )

if "time" in df.columns:

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce",
        format="ISO8601"
    )

else:

    df["time"] = pd.Timestamp.now()

# FIX CITY ISSUE

if "city" not in df.columns:

    if "location" in df.columns:

        df["city"] = df["location"]

    elif "name" in df.columns:

        df["city"] = df["name"]

    else:

        df["city"] = "Unknown"

df["city"] = (
    df["city"]
    .fillna("Unknown")
    .astype(str)
)

df = df.dropna(
    subset=[
        "temperature",
        "humidity",
        "time"
    ]
)

# GUARANTEE ALL CITIES

for c in EXPECTED_CITIES:

    if c not in df["city"].values:

        df.loc[len(df)] = {
            "city": c,
            "temperature": 0,
            "humidity": 0,
            "time": pd.Timestamp.now()
        }

df = df.tail(600)

# ==================================
# FILTER
# ==================================

city = st.selectbox(

    "🏙 Select City",

    ["All Cities"]

    +

    sorted(
        df["city"]
        .unique()
    )

)

if city != "All Cities":

    df = df[
        df["city"]
        ==
        city
    ]

latest = (

    df

    .sort_values(
        "time"
    )

    .groupby(
        "city"
    )

    .tail(1)

)

# ==================================
# SCORE
# ==================================

health = []

risk = []

colors = []

for _, r in latest.iterrows():

    score = max(

        0,

        100

        -

        max(
            0,
            r["temperature"] - 30
        ) * 2

        -

        max(
            0,
            r["humidity"] - 70
        )

    )

    health.append(
        score
    )

    level, color = calculate_risk(

        r["temperature"],

        r["humidity"]

    )

    risk.append(
        level
    )

    colors.append(
        color
    )

latest["health"] = health
latest["risk"] = risk
latest["color"] = colors


avg = latest.health.mean()

rank = latest.sort_values(
    "health",
    ascending=False
)

# ==================================
# TIME
# ==================================

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

current_time = IST.strftime(
    "%I:%M:%S %p"
).replace(" AM","AM").replace(" PM","PM")

updated_time = IST.strftime(
    "%d %b %Y · %I:%M:%S %p"
).replace(" AM","AM").replace(" PM","PM")

# ==================================
# HERO
# ==================================

left, right = st.columns([8.8,1.0])

with left:

    st.markdown("""
<div class='hero'>

<h1>
🌍 Urban Geo Intelligence
</h1>

<h3>
Digital Twin • Risk Zones
</h3>

</div>
""",
unsafe_allow_html=True)

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
position:relative;
">

<div style="
font-size:44px;
margin-top:0px;
margin-bottom:8px;
line-height:1;
">
🕒
</div>

<div style="
font-size:28px;
font-weight:800;
color:#124f9d;
white-space:nowrap;
line-height:1;
">
{current_time}
</div>

<div style="
margin-top:10px;
font-size:15px;
color:#5a6572;
">
Live Time
</div>

</div>
""",
unsafe_allow_html=True
)

# ==================================
# KPI
# ==================================

a,b,c,d = st.columns(4)

a.metric(
    "🏙 Cities",
    latest.city.nunique()
)

b.metric(
    "🌡 Avg Temp",
    f"{latest.temperature.mean():.1f}°C"
)

c.metric(
    "💧 Humidity",
    f"{latest.humidity.mean():.1f}%"
)

d.metric(
    "❤️ Health",
    f"{avg:.0f}%"
)

# ==================================
# MAP
# ==================================

st.subheader(
    "🗺 Urban Digital Twin"
)

m = folium.Map(
    location=[21,79],
    zoom_start=5,
    tiles="CartoDB positron"
)

for _, r in rank.iterrows():

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

⚠ Risk: {r['risk']}
"""
        ).add_to(m)

st_folium(
    m,
    height=450,
    width="stretch"
)

# ==================================
# TABLE
# ==================================

st.subheader(
    "🏆 City Ranking"
)

st.dataframe(

    rank[[
        "city",
        "temperature",
        "humidity",
        "health",
        "risk"
    ]],

    width="stretch"

)

# ==================================
# CHART
# ==================================

st.subheader(
    "🔥 Health Zones"
)

fig = px.bar(

    rank,

    x="city",

    y="health",

    color="risk"

)

st.plotly_chart(
    fig
)

# ==================================
# INSIGHT
# ==================================

st.subheader(
    "🧠 Geo Insight"
)

if avg < 60:

    st.error(
        "High Urban Risk"
    )

elif avg < 80:

    st.warning(
        "Moderate Conditions"
    )

else:

    st.success(
        "Healthy Urban Environment"
    )

# ==================================
# EXPORT
# ==================================

file, mime, ext = export_data(
    rank
)

st.download_button(

    "⬇ Export Geo Report",

    file,

    f"urbanmind_geo{ext}",

    mime

)

# ==================================
# SUMMARY
# ==================================

st.success(
f"""
Cities: {rank.city.nunique()}

Health: {avg:.0f}%

Theme: {settings["theme"]}

Export: {settings["export"]}
"""
)