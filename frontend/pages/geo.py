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

st_autorefresh(
    interval=settings["refresh"] * 1000,
    key="geo_refresh"
)

# ==================================
# UI
# ==================================

st.markdown("""
<style>

.block-container{
padding-top:.4rem !important;
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

margin-bottom:24px;
}

.hero h1{
font-size:48px;
}

.hero p{
font-size:18px;
}

[data-testid="metric-container"]{
padding:24px;
border-radius:20px;
}

</style>
""",
unsafe_allow_html=True)

# ==================================
# PATH
# ==================================

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT / "data" / "weather_history.csv"

CITY = {

"Delhi":[28.61,77.20],
"Mumbai":[19.07,72.87],
"Hyderabad":[17.38,78.48],
"Chennai":[13.08,80.27],
"Bangalore":[12.97,77.59],
"Vijayawada":[16.50,80.64]

}

# ==================================
# LOAD
# ==================================

@st.cache_data(ttl=5)
def load():

    try:
        return pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

    except:
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

for c in [
"time",
"temperature",
"humidity"
]:

    if c not in df:
        df[c]=0

if "city" not in df:
    df["city"]="Unknown"

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

df=df.tail(600)

# ==================================
# FILTER
# ==================================

city=st.selectbox(
"🏙 Select City",

["All Cities"]

+

sorted(
df["city"]
.astype(str)
.unique()
)
)

if city!="All Cities":

    df=df[
        df["city"]==city
    ]

if len(df)==0:

    st.warning(
        "No city records"
    )

    st.stop()

latest=(

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

latest["health"]=(
100
-
(
latest["temperature"]
-30
)
.clip(0)
*2
-
(
latest["humidity"]
-70
)
.clip(0)
)

latest["health"]=latest[
"health"
].clip(
0,
100
)

avg=float(
latest.health.mean()
)

# ==================================
# HEADER
# ==================================

left,right=st.columns([5,1])

with left:

    st.markdown("""
<div class='hero'>

<h1>
🌍 Geo Intelligence
</h1>

<p>
Urban Digital Twin • Risk Zones
</p>

</div>
""",
unsafe_allow_html=True
)

with right:

    st.info(
datetime.now(
pytz.timezone(
"Asia/Kolkata"
)
).strftime(
"%I:%M:%S %p"
)
)

# ==================================
# KPI
# ==================================

a,b,c,d=st.columns(4)

a.metric(
"🏙 Cities",
latest.city.nunique()
)

b.metric(
"🌡 Avg Temp",
f"{latest.temperature.mean():.1f}°C"
)

c.metric(
"💧 Avg Humidity",
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
"🗺 Geo Map"
)

m=folium.Map(
location=[21,79],
zoom_start=5
)

for _,r in latest.iterrows():

    if r["city"] in CITY:

        color=(
"green"
if r["health"]>80
else
"orange"
if r["health"]>60
else
"red"
)

        folium.CircleMarker(

location=
CITY[
r["city"]
],

radius=18,

fill=True,

fill_opacity=.8,

color=color,

popup=
f"""
{r["city"]}

Health:
{r["health"]:.0f}
"""

).add_to(
m
)

st_folium(
m,
height=600
)

# ==================================
# TABLE
# ==================================

rank=latest.sort_values(
"health",
ascending=False
)

st.subheader(
"🏆 Ranking"
)

st.dataframe(
rank,
use_container_width=True
)

# ==================================
# CHART
# ==================================

fig=px.bar(
rank,
x="city",
y="health",
color="health"
)

st.plotly_chart(
fig,
use_container_width=True
)

# ==================================
# AI
# ==================================

st.subheader(
"🧠 Geo Insight"
)

if avg<60:

    st.error(
        "High Urban Risk"
    )

elif avg<80:

    st.warning(
        "Moderate Risk"
    )

else:

    st.success(
        "Stable Urban Conditions"
    )

# ==================================
# EXPORT
# ==================================

st.subheader(
"⬇ Export Geo"
)

file,mime,ext=export_data(
rank
)

st.download_button(
"Download Geo Report",
file,
f"urbanmind_geo{ext}",
mime,
use_container_width=True
)

# ==================================
# SUMMARY
# ==================================

st.success(f"""
Cities: {rank.city.nunique()}
Health: {avg:.0f}%
Export: {settings["export"]}
Theme: {settings["theme"]}
""")