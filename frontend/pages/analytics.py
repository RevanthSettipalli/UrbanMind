import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import pytz

from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from utils.load_weather import load_weather
from utils.auth_guard import require_login
from utils.sidebar import render_sidebar

from utils.settings import (
    apply_theme,
    load_settings,
    export_data
)


# =================================
# PAGE
# =================================

st.set_page_config(
    page_title="Urban Analytics",
    page_icon="📊",
    layout="wide"
)

require_login()

render_sidebar()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

settings = load_settings()


# =================================
# PREMIUM UI
# =================================

st.markdown("""
<style>

.block-container{
padding-top:0.4rem !important;
}

.hero{
padding:40px;

border-radius:30px;

background:
linear-gradient(
135deg,
#04162a,
#0b5c93
);

color:white;

margin-bottom:24px;
}

.hero h1{
font-size:50px;
}

.hero p{
font-size:18px;
opacity:.9;
}

[data-testid="metric-container"]{

background:white;

border-radius:22px;

padding:24px;

box-shadow:
0 8px 25px
rgba(0,0,0,.05);

}

.section{

padding:22px;

background:white;

border-radius:22px;

margin-bottom:22px;

}

</style>
""",
unsafe_allow_html=True)


# =================================
# REFRESH
# =================================

refresh_rate = max(
    1,
    int(settings.get("refresh_rate", 10))
)

st_autorefresh(
    interval=refresh_rate * 1000,
    key=f"analytics_refresh_{refresh_rate}"
)

# =================================
# LOAD
# =================================

df = load_weather()

if df.empty:

    st.warning(
        "Waiting for analytics..."
    )

    st.stop()


# =================================
# CLEAN
# =================================

required = [

"time",
"city",
"temperature",
"humidity"

]

for c in required:

    if c not in df:

        df[c] = (
            "Unknown"
            if c=="city"
            else 0
        )


df["time"]=pd.to_datetime(
df["time"],
errors="coerce"
)

df["temperature"]=pd.to_numeric(
df["temperature"],
errors="coerce"
)

df["humidity"]=pd.to_numeric(
df["humidity"],
errors="coerce"
)

df=df.dropna()

df=df.tail(3000)


# =================================
# FILTER
# =================================

cities=sorted(
df["city"]
.astype(str)
.unique()
)

city=st.selectbox(

"🏙 Select City",

["All Cities"]

+

cities

)

if city!="All Cities":

    df=df[
        df["city"]
        ==
        city
    ]


# =================================
# TIME
# =================================

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

current_time = IST.strftime(
    "%I:%M:%S %p"
).replace(" AM", "AM").replace(" PM", "PM")

updated_time = IST.strftime(
    "%d %b %Y · %I:%M:%S %p"
).replace(" AM", "AM").replace(" PM", "PM")


# =================================
# SCORE
# =================================

avg_temp=round(
df.temperature.mean(),
1
)

avg_hum=round(
df.humidity.mean(),
1
)

urban=int(

max(

70,

100

-

max(
0,
avg_temp-30
)

-

max(
0,
(avg_hum-70)/2
)

)

)


# =================================
# HEADER
# =================================

left, right = st.columns([8.8,1.0])

with left:

    st.markdown("""
<div class='hero'>

<h1>
📊 Urban Analytics
</h1>

<p>
Advanced Intelligence • Ranking • Geo Analysis
</p>

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
line-height:1;
white-space:nowrap;
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


# =================================
# KPI
# =================================

a,b,c,d=st.columns(4)

a.metric(
"🏙 Urban Score",
urban
)

b.metric(
"🌡 Avg Temp",
f"{avg_temp}°C"
)

c.metric(
"💧 Avg Humidity",
f"{avg_hum}%"
)

d.metric(
"📄 Records",
len(df)
)


# =================================
# HEALTH
# =================================

st.subheader(
"🩺 Urban Health"
)

st.progress(
urban/100
)


# =================================
# RANK
# =================================

rank=(

df

.groupby(
"city"
)

.agg({

"temperature":"mean",

"humidity":"mean"

})

.round(1)

.reset_index()

)

rank["score"] = (
    100
    - abs(
        rank["temperature"]
        - 30
    )
).clip(lower=0)


rank=rank.sort_values(
    "score",
    ascending=False
)

# Insert recommendation block
latest = (
    df.sort_values("time")
    .iloc[-1]
)

if latest["temperature"] > 40:
    recommendation = "Heat Risk Increasing"
elif latest["humidity"] > 80:
    recommendation = "High Humidity Alert"
else:
    recommendation = "Conditions Stable"


st.subheader(
    "🏆 City Ranking"
)

st.dataframe(
rank,
use_container_width=True
)

# -------------------------------
# Best/Worst City Highlight
# -------------------------------
best_city = rank.iloc[0]["city"]
worst_city = rank.iloc[-1]["city"]

c1, c2 = st.columns(2)

with c1:
    st.success(f"🏆 Best Performing City: {best_city}")

with c2:
    st.error(f"⚠ City Requiring Attention: {worst_city}")

# -------------------------------
# Analytics Executive Insights
# -------------------------------
st.subheader("🧠 City Intelligence Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"🏆 Leader City: {best_city}")

with col2:
    st.warning(f"⚠ Focus City: {worst_city}")

with col3:
    st.success(f"📊 National Urban Score: {urban}")

rank_chart = px.bar(
    rank,
    x="city",
    y="score",
    color="score",
    title="Urban Intelligence Ranking"
)

st.plotly_chart(
    rank_chart,
    use_container_width=True
)


# =================================
# MAP
# =================================
# DIGITAL TWIN
# ====================================

st.subheader(
    "🗺 Urban Digital Twin"
)

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

rank["risk"] = rank.apply(
    lambda r:
    "🔥 Heat Risk"
    if r["temperature"] >= 40
    else (
        "🌧 High Humidity"
        if r["humidity"] >= 80
        else "✅ Stable"
    ),
    axis=1
)

rank["color"] = rank["score"].apply(
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

map_data = rank if city == "All Cities" else rank[
    rank["city"] == city
]

for _, r in map_data.iterrows():

    city_name = str(r["city"])

    if city_name in CITY:

        rec = (
            "Heat Risk Increasing"
            if r["temperature"] > 40
            else (
                "High Humidity Alert"
                if r["humidity"] > 80
                else "Conditions Stable"
            )
        )

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

⭐ Score: {r['score']:.0f}

🌡 Temp: {r['temperature']:.1f}°C

💧 Humidity: {r['humidity']:.1f}%

⚠ Recommendation: {rec}
"""
        ).add_to(m)

st_folium(
    m,
    height=450,
    width="stretch"
)

# -------------------------------
# Advanced Analytics & Correlation Engine
# -------------------------------
st.subheader("🧪 Advanced Analytics & Correlation Engine")

corr_df = df[["temperature", "humidity"]].corr()

corr_fig = px.imshow(
    corr_df,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(
    corr_fig,
    use_container_width=True
)

# =================================
# TREND
# =================================

st.subheader(
"📈 Trend Analysis"
)

trend_df = (
    df
    if city == "All Cities"
    else df[
        df["city"] == city
    ]
)

fig = px.area(
    trend_df.tail(200),
    x="time",
    y=[
        "temperature",
        "humidity"
    ]
)

fig.update_layout(
height=500
)

st.plotly_chart(
fig,
use_container_width=True
)


# -------------------------------
# Temperature vs Humidity Analysis
# -------------------------------
st.subheader("🌡 Climate Intelligence")

scatter_fig = px.scatter(
    df,
    x="temperature",
    y="humidity",
    color="city",
    title="Temperature vs Humidity Distribution"
)

st.plotly_chart(
    scatter_fig,
    use_container_width=True
)

# -------------------------------
# Analytics Intelligence Center
# -------------------------------
st.subheader("📊 Analytics Intelligence Center")

s1, s2, s3, s4 = st.columns(4)

s1.metric("🏙 Cities", len(rank))
s2.metric("🏆 Best City", best_city)
s3.metric("🌡 Avg Temp", f"{avg_temp}°C")
s4.metric("💧 Avg Humidity", f"{avg_hum}%")


# =================================
# INSIGHT
# =================================

st.subheader(
"🧠 AI Insight"
)

if avg_temp>40:

    st.error(
        "Heat Risk Increasing"
    )

elif avg_hum>80:

    st.warning(
        "Humidity Rising"
    )

else:

    st.success(
        "Urban Conditions Stable"
    )


# =================================
# EXPORT
# =================================

file, mime, ext = export_data(
    df
)

st.download_button(

    "⬇ Export Analytics",

    file,

    f"urbanmind_analytics{ext}",

    mime,

    use_container_width=True
)


# =================================
# SUMMARY
# =================================

st.markdown(
    f"""
### 📌 National Urban Intelligence Summary

• Best Performing City: {best_city}

• City Requiring Attention: {worst_city}

• Average Urban Score: {urban}

• Average Temperature: {avg_temp}°C

• Average Humidity: {avg_hum}%

• Total Records Analysed: {len(df)}
"""
)
