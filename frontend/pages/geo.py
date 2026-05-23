import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import pytz

from pathlib import Path
from datetime import datetime
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar


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

st_autorefresh(
    interval=5000,
    key="geo_refresh"
)


# ==================================
# PATH
# ==================================

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT / "data" / "weather_history.csv"


# ==================================
# CITY MAP
# ==================================

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
        "Waiting for stream..."
    )

    st.stop()


# ==================================
# CLEAN
# ==================================

for col in [

"time",
"temperature",
"humidity"

]:

    if col not in df.columns:
        df[col] = 0


if "city" not in df.columns:
    df["city"] = "Unknown"


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

df = df.tail(500)


# ==================================
# FILTER
# ==================================

cities = sorted(
    df["city"]
    .astype(str)
    .unique()
)

selected = st.selectbox(

    "🏙 Select City",

    ["All Cities"]

    +

    cities

)

if selected != "All Cities":

    df = df[
        df["city"]
        ==
        selected
    ]


if len(df) == 0:

    st.warning(
        "No geo records"
    )

    st.stop()


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
# HEALTH
# ==================================

latest["health"] = (

100

-

(
latest["temperature"]
-
30
)

.clip(0)

*2

-

(
latest["humidity"]
-
70
)

.clip(0)

)

latest["health"] = (

latest["health"]

.clip(
0,
100
)

.round()

)


# ==================================
# HEADER
# ==================================

left,right=st.columns([4,1])

with left:

    st.title(
        "🌍 Geo Intelligence"
    )

    st.caption(
        "Urban Digital Twin • Risk Zones"
    )

with right:

    st.info(

datetime.now(

pytz.timezone(
"Asia/Kolkata")

).strftime(
"%I:%M:%S %p"
)

)


# ==================================
# KPI
# ==================================

a,b,c,d=st.columns(4)

a.metric(
"Cities",
latest.city.nunique()
)

b.metric(
"Avg Temp",
f"{latest.temperature.mean():.1f}°C"
)

c.metric(
"Avg Humidity",
f"{latest.humidity.mean():.1f}%"
)

d.metric(
"Urban Health",
f"{latest.health.mean():.0f}%"
)


# ==================================
# MAP
# ==================================

st.subheader(
"🗺 Geo Digital Twin"
)

m = folium.Map(

location=[21,79],

zoom_start=5

)

for _,r in latest.iterrows():

    if r["city"] in CITY:

        color=(

"green"

if r["temperature"]<30

else

"orange"

if r["temperature"]<36

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

fill_opacity=0.8,

color=color,

popup=
f"""
{r["city"]}

🌡 {r["temperature"]:.1f}°C

💧 {r["humidity"]:.1f}%

❤️ {r["health"]:.0f}
"""

).add_to(
m
)

st_folium(
m,
height=550,
key="geo_map"
)


# ==================================
# RANK
# ==================================

st.subheader(
"🏆 City Ranking"
)

rank = latest.sort_values(
"health",
ascending=False
)

st.dataframe(

rank[[

"city",
"temperature",
"humidity",
"health"

]],

use_container_width=True

)


# ==================================
# CHARTS
# ==================================

st.subheader(
"🔥 Temperature Zones"
)

fig = px.bar(

rank,

x="city",

y="temperature",

color="temperature"

)

st.plotly_chart(
fig,
use_container_width=True
)


st.subheader(
"💧 Humidity Zones"
)

fig2 = px.line(

rank,

x="city",

y="humidity",

markers=True

)

st.plotly_chart(
fig2,
use_container_width=True
)


# ==================================
# AI
# ==================================

st.subheader(
"🧠 Geo AI Insight"
)

avg = rank[
"health"
].mean()

if avg < 60:

    st.error(
        "Heat Risk Increasing"
    )

elif avg < 80:

    st.warning(
        "Moderate Urban Risk"
    )

else:

    st.success(
        "Stable Conditions"
    )


# ==================================
# EXPORT
# ==================================

st.download_button(

"⬇ Export Geo Report",

rank.to_csv(
index=False
).encode(),

"urbanmind_geo.csv"

)


# ==================================
# SUMMARY
# ==================================

st.success(
f"""
Cities:
{rank.city.nunique()}

Average Health:
{avg:.0f}

Last Update:
{datetime.now().strftime('%I:%M:%S %p')}
"""
)