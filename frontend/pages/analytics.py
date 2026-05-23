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

# =================================
# REFRESH
# =================================

st_autorefresh(
    interval=5000,
    key="analytics"
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

            if c == "city"

            else 0

        )

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

df = df.tail(
3000
)

if len(df) == 0:

    st.warning(
        "No analytics records"
    )

    st.stop()

# =================================
# FILTER
# =================================

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

# =================================
# TIME
# =================================

IST = datetime.now(

pytz.timezone(
"Asia/Kolkata"
)

)

# =================================
# SCORE
# =================================

avg_temp = round(
df.temperature.mean(),
1
)

avg_hum = round(
df.humidity.mean(),
1
)

urban = max(

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

urban = int(
urban
)

# =================================
# HEADER
# =================================

left,right = st.columns([4,1])

with left:

    st.title(
        "📊 Urban Analytics"
    )

with right:

    st.info(
        IST.strftime(
            "%I:%M:%S %p"
        )
    )

# =================================
# KPI
# =================================

a,b,c,d = st.columns(4)

a.metric(
"Urban Score",
urban
)

b.metric(
"Avg Temp",
f"{avg_temp}°C"
)

c.metric(
"Avg Humidity",
f"{avg_hum}%"
)

d.metric(
"Records",
len(df)
)

# =================================
# HEALTH
# =================================

st.subheader(
"🖥 System Health"
)

st.progress(
urban/100
)

st.success(
f"Health • {urban}%"
)

# =================================
# RANKING
# =================================

rank = (

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

-

abs(

rank[
"temperature"
]

-

30

)

)

rank = rank.sort_values(
"score",
ascending=False
)

st.subheader(
"🏆 Urban Ranking"
)

st.dataframe(
rank,
use_container_width=True
)

# =================================
# MAP
# =================================

coords = {

"Delhi":[28.61,77.20],
"Mumbai":[19.07,72.87],
"Hyderabad":[17.38,78.48],
"Chennai":[13.08,80.27],
"Bangalore":[12.97,77.59],
"Vijayawada":[16.50,80.64]

}

st.subheader(
"🗺 Urban Heat Map"
)

m = folium.Map(

location=[
21,
79
],

zoom_start=5

)

for _,r in rank.iterrows():

    if r["city"] in coords:

        folium.CircleMarker(

location=
coords[
r["city"]
],

radius=12,

popup=
f"""
{r["city"]}

Score:
{r["score"]:.0f}
""",

fill=True,

fill_opacity=0.8,

color="red"

).add_to(
m
)

st_folium(

m,

height=420,

key="analytics_map"

)

# =================================
# TREND
# =================================

st.subheader(
"📈 Trend"
)

fig = px.line(

df.tail(150),

x="time",

y=[

"temperature",

"humidity"

]

)

fig.update_layout(
height=450
)

st.plotly_chart(
fig,
use_container_width=True
)

# =================================
# AI
# =================================

st.subheader(
"🧠 AI Insight"
)

if avg_temp > 40:

    st.error(
        "Heat Risk Increasing"
    )

elif avg_hum > 80:

    st.warning(
        "Humidity Rising"
    )

else:

    st.success(
        "Urban Stable"
    )

# =================================
# EXPORT
# =================================

st.download_button(

"⬇ Export Analytics",

df.to_csv(
index=False
).encode(),

"urbanmind_analytics.csv"

)

# =================================
# SUMMARY
# =================================

st.success(
f"""
Urban Score:
{urban}

Records:
{len(df)}

Temperature:
{avg_temp}°C

Humidity:
{avg_hum}%
"""
)