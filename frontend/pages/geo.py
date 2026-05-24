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

st_autorefresh(
    interval=settings["refresh"] * 1000,
    key="geo_refresh"
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

# ==================================
# PATH
# ==================================

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT / "data" / "processed_weather.csv"

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


df=load()

if df.empty:

    st.warning(
        "Waiting for Geo Stream..."
    )

    st.stop()


# ==================================
# CLEAN
# ==================================

df["temperature"]=pd.to_numeric(
df["temperature"],
errors="coerce"
)

df["humidity"]=pd.to_numeric(
df["humidity"],
errors="coerce"
)

df["time"]=pd.to_datetime(
df["time"],
errors="coerce"
)

df=df.dropna()

df=df.tail(600)


# ==================================
# FILTER
# ==================================

if "city" in df.columns:

    city=st.selectbox(

"🏙 Select City",

["All Cities"]

+

sorted(
df["city"]
.unique()
)

)

    if city!="All Cities":

        df=df[
            df["city"]
            ==
            city
        ]


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

health=[]

risk=[]

colors=[]

for _,r in latest.iterrows():

    score=max(

0,

100-

max(
0,
r["temperature"]-30
)*2

-

max(
0,
r["humidity"]-70
)

)

    health.append(
score
)

    level,color=calculate_risk(

r["temperature"],

r["humidity"]

)

    risk.append(
level
)

    colors.append(
color
)

latest["health"]=health
latest["risk"]=risk
latest["color"]=colors

avg=latest.health.mean()


# ==================================
# HERO
# ==================================

left,right=st.columns([5,1])

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

m=folium.Map(

location=[21,79],

zoom_start=5

)

for _,r in latest.iterrows():

    if r["city"] in CITY:

        folium.CircleMarker(

location=
CITY[
r["city"]
],

radius=18,

fill=True,

fill_color=
r["color"],

color=
r["color"],

popup=f"""

{r["city"]}

🌡 {r["temperature"]:.1f}

💧 {r["humidity"]:.1f}

❤️ {r["health"]:.0f}

⚠ {r["risk"]}

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

use_container_width=True

)


# ==================================
# CHART
# ==================================

st.subheader(
"🔥 Health Zones"
)

fig=px.bar(

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
# INSIGHT
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
        "Moderate Conditions"
    )

else:

    st.success(
        "Healthy Urban Environment"
    )


# ==================================
# EXPORT
# ==================================

file,mime,ext=export_data(
rank
)

st.download_button(

"⬇ Export Geo Report",

file,

f"urbanmind_geo{ext}",

mime,

use_container_width=True

)


# ==================================
# SUMMARY
# ==================================

st.success(
f"""

Cities:
{rank.city.nunique()}

Health:
{avg:.0f}%

Theme:
{settings["theme"]}

Export:
{settings["export"]}

"""
)