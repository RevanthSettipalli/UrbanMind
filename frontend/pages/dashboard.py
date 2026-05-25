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

from utils.city_selector import city_filter
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

updated_time = IST.strftime(
    "%d %b %Y"
)

updated_clock = IST.strftime(
    "%I:%M:%S %p"
).replace(" AM", "AM").replace(" PM", "PM")

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
margin-top:0px;
line-height:1;
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

map_data = (
    df
    if city == "All Cities"
    else df[
        df["city"] == city
    ]
)

m = folium.Map(
    location=[21,79],
    zoom_start=5
)

for _, r in (
    map_data
    .groupby("city")
    .tail(1)
    .iterrows()
):

    city_name = str(r["city"])

    if city_name not in CITY:
        continue

    rec = get_recommendation(
        float(r["temperature"]),
        float(r["humidity"])
    )["message"]

    folium.Marker(

        location=CITY[city_name],

        tooltip=f"📍 {city_name}",

        popup=f"""
City:
{city_name}

Temp:
{r['temperature']}

Humidity:
{r['humidity']}

{rec}
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


analytics 

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

st_autorefresh(
    interval=1000,
    key="analytics_live_clock"
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

rank["score"]=(
100
-
abs(
rank["temperature"]
-
30
)
)

rank=rank.sort_values(
"score",
ascending=False
)


st.subheader(
"🏆 City Ranking"
)

st.dataframe(
rank,
use_container_width=True
)


# =================================
# MAP
# =================================

coords={

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

m=folium.Map(

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

radius=16,

fill=True,

fill_opacity=.8,

color="red",

popup=
f"""
{r["city"]}

Score:
{r["score"]:.0f}
"""

).add_to(
m
)

st_folium(
m,
height=450
)


# =================================
# TREND
# =================================

st.subheader(
"📈 Trend Analysis"
)

fig=px.area(

df.tail(200),

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
### 📌 Analytics Summary

- Urban Score → {urban}
- Records → {len(df)}
- Avg Temp → {avg_temp}°C
- Avg Humidity → {avg_hum}%

"""
)