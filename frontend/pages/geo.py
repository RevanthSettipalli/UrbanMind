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

from datetime import datetime
from streamlit_folium import st_folium
from utils.load_weather import load_weather

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
from backend.intelligence.urban_score import calculate_score

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

df = load_weather()

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

    urban_result = calculate_score(
        r.get("temperature", 0),
        r.get("humidity", 0),
        r.get("temperature", 0),
        r.get("aqi", 1),
        r.get("pm25", 0),
        r.get("pm10", 0),
        r.get("co", 0),
        r.get("no2", 0)
    )

    score = urban_result["score"]

    health.append(score)

    level, color = calculate_risk(
        r["temperature"],
        r["humidity"]
    )

    risk.append(level)
    colors.append(color)

latest["health"] = health
latest["risk"] = risk
latest["color"] = colors


avg = latest.health.mean()

rank = latest.sort_values(
    "health",
    ascending=False
)

if rank.empty:
    st.warning("No geo data available")
    st.stop()

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

<div id="geo-live-clock" style="font-size:28px;font-weight:800;color:#124f9d;white-space:nowrap;line-height:1;">
Loading...
</div>

<script>
function updateGeoClock(){
const now=new Date();
const time=now.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:true});
const el=document.getElementById('geo-live-clock');
if(el){el.innerHTML=time.replace(' AM','AM').replace(' PM','PM');}
}
updateGeoClock();
setInterval(updateGeoClock,1000);
</script>

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

📈 Rank: #{list(rank['city']).index(city_name)+1}

🛰 Geo Status: Active
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

#
# ==================================
# DIGITAL TWIN COMPARISON
# ==================================
#

st.subheader("🏙 Smart City Digital Twin Comparison")

compare_cols = [c for c in ["city", "temperature", "humidity", "health"] if c in rank.columns]

st.dataframe(
    rank[compare_cols].head(5),
    use_container_width=True
)

st.subheader(
    "🏆 City Ranking"
)

ranking_display = rank.copy()

if len(ranking_display) >= 1:
    ranking_display.iloc[0, ranking_display.columns.get_loc("city")] = f"🥇 {ranking_display.iloc[0]['city']}"

if len(ranking_display) >= 2:
    ranking_display.iloc[1, ranking_display.columns.get_loc("city")] = f"🥈 {ranking_display.iloc[1]['city']}"

if len(ranking_display) >= 3:
    ranking_display.iloc[2, ranking_display.columns.get_loc("city")] = f"🥉 {ranking_display.iloc[2]['city']}"

st.dataframe(

    ranking_display[[
        "city",
        "temperature",
        "humidity",
        "health",
        "risk"
    ]],

    use_container_width=True

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
    fig,
    use_container_width=True
)

# ==================================
# GEO INTELLIGENCE CENTER
# ==================================

st.subheader("🌍 Geo Intelligence Center")

s1, s2, s3, s4 = st.columns(4)

s1.success("🟢 Geo Engine")
s2.success("🟢 Map Service")
s3.success("🟢 Forecast Engine")
s4.success("🟢 AI Copilot")

best_city = rank.iloc[0]["city"]
worst_city = rank.iloc[-1]["city"]

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏆 Safest City", best_city)
c2.metric("⚠ Risk City", worst_city)
c3.metric("❤️ National Health", f"{avg:.0f}%")
c4.metric("📍 Active Cities", len(rank))

st.info(
    f"UrbanMind Geo Engine identifies {best_city} as the healthiest city while {worst_city} requires closer monitoring."
)

# ==================================
# INSIGHT
# ==================================

#
# ==================================
# RISK DISTRIBUTION
# ==================================
#

st.subheader("🚨 Risk Distribution")

risk_chart = px.pie(
    rank,
    names="risk",
    title="Urban Risk Breakdown"
)


st.plotly_chart(
    risk_chart,
    use_container_width=True
)

# ==================================
# CLIMATE RISK ANALYSIS
# ==================================

st.subheader("🌡 Climate Risk Intelligence")

climate_fig = px.scatter(
    rank,
    x="temperature",
    y="humidity",
    color="risk",
    size="health",
    hover_name="city",
    title="Climate Risk Distribution"
)

st.plotly_chart(
    climate_fig,
    use_container_width=True
)

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
# AI GEO RECOMMENDATIONS
# ==================================

st.subheader("🧠 Geo AI Recommendations")

st.info(
    f"Prioritize intervention in {worst_city}. Replicate sustainability practices from {best_city}. Continue monitoring temperature and humidity anomalies across all cities."
)

# ==================================
# NATIONAL GEO INTELLIGENCE
# ==================================

st.subheader("🌍 National Geo Intelligence Summary")

st.success(
    f"India-wide geo intelligence indicates {best_city} is the benchmark smart city while {worst_city} requires the highest monitoring priority. National urban health currently stands at {avg:.0f}%."
)

# ==================================
# AQI HEATMAP READINESS LAYER
# ==================================

st.subheader("🌫 Pollution Hotspot Intelligence")

if "aqi" in rank.columns:

    hotspot_df = rank.sort_values(
        "aqi",
        ascending=False
    )

    hotspot_fig = px.bar(
        hotspot_df,
        x="city",
        y="aqi",
        color="aqi",
        title="Pollution Hotspots"
    )

    st.plotly_chart(
        hotspot_fig,
        use_container_width=True
    )

# ==================================
# GEO FORECAST MAP
# ==================================

st.subheader("🔮 Geo Forecast Intelligence")

forecast_df = rank.copy()

forecast_df["forecast_health"] = (
    forecast_df["health"] * 0.98
).round(1)

forecast_fig = px.bar(
    forecast_df,
    x="city",
    y="forecast_health",
    color="risk",
    title="Next-Cycle Urban Health Forecast"
)

st.plotly_chart(
    forecast_fig,
    use_container_width=True
)

# ==================================
# NATIONAL RESILIENCE INDEX
# ==================================

st.subheader("🛡 National Resilience Index")

resilience_score = round(
    avg * 0.85,
    1
)

r1, r2, r3 = st.columns(3)

r1.metric(
    "🛡 Resilience Score",
    resilience_score
)

r2.metric(
    "🏆 Benchmark City",
    best_city
)

r3.metric(
    "⚠ Priority Zone",
    worst_city
)

# ==================================
# POLICY IMPACT SIMULATOR
# ==================================

st.subheader("🏛 Geo Policy Impact Simulator")

policy = st.selectbox(
    "Policy Scenario",
    [
        "Green Infrastructure",
        "Pollution Reduction",
        "Smart Mobility",
        "Climate Adaptation"
    ],
    key="geo_policy"
)

impact = avg

if policy == "Green Infrastructure":
    impact += 5
elif policy == "Pollution Reduction":
    impact += 8
elif policy == "Smart Mobility":
    impact += 4
elif policy == "Climate Adaptation":
    impact += 6

st.success(
    f"Projected National Urban Health: {min(100, round(impact,1))}%"
)

# ==================================
# GEO AI COPILOT
# ==================================

st.subheader("🤖 Geo AI Copilot")

geo_question = st.selectbox(
    "Ask Geo Intelligence",
    [
        "Which city is healthiest?",
        "Which city is highest risk?",
        "What should government prioritize?",
        "What is the national status?"
    ],
    key="geo_copilot"
)

if geo_question == "Which city is healthiest?":
    st.info(f"🏆 {best_city} currently leads national geo intelligence rankings.")
elif geo_question == "Which city is highest risk?":
    st.warning(f"⚠ {worst_city} requires immediate monitoring attention.")
elif geo_question == "What should government prioritize?":
    st.info(f"Prioritize intervention in {worst_city} and replicate policies from {best_city}.")
else:
    st.success(f"National geo health remains at {avg:.0f}% across monitored cities.")