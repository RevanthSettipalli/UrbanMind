from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import pytz
import sys

from backend.intelligence.forecast_engine import (
    generate_forecast
)

from pathlib import Path
from datetime import datetime

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
    page_title="Forecast Intelligence",
    page_icon="🔮",
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
    key=f"forecast_live_clock_{refresh_rate}"
)


# =================================
# STYLE
# =================================

st.markdown("""
<style>

.block-container{
padding-top:.4rem !important;
}

.hero{
padding:35px;

border-radius:30px;

background:
linear-gradient(
135deg,
#19073d,
#5a189a
);

color:white;

margin-bottom:25px;
}

.hero h1{
font-size:52px;
margin:0;
}

.card{

padding:20px;

background:white;

border-radius:20px;

box-shadow:
0 10px 30px
rgba(0,0,0,.05);

}

</style>
""",
unsafe_allow_html=True)


# =================================
# ROOT
# =================================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CSV = ROOT/"data"/"processed_weather.csv"
MODEL = ROOT/"models"/"weather"/"weather_model.pkl"

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


# =================================
# LOAD
# =================================

@st.cache_data(ttl=0)
def load():

    try:
        return pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

    except:
        return pd.DataFrame()


@st.cache_resource
def load_model():

    try:
        return joblib.load(
            MODEL
        )

    except:
        return None


df=load()
model=load_model()

if df.empty:

    st.warning(
        "Waiting for Forecast Data..."
    )

    st.stop()


# =================================
# CLEAN
# =================================

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


# =================================
# FILTER
# =================================

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


if df.empty:

    st.warning(
        "No forecast data available"
    )

    st.stop()

latest = df.iloc[-1]


# =================================
# FORECAST
# =================================

forecast=generate_forecast(

latest["temperature"],

latest["humidity"],

24

)

forecast=pd.DataFrame(
forecast
)


peak=float(
forecast.temperature.max()
)

confidence=int(
forecast.confidence.mean()
)

risk="Safe"

if peak>42:

    risk="Extreme"

elif peak>36:

    risk="Moderate"


# =================================
# HERO
# =================================

left, right = st.columns([8.8,1.0])

with left:

    st.markdown(f"""
<div class='hero'>

<h1>
🔮 Forecast Intelligence
</h1>

<h3>
AI Prediction • Future Monitoring
</h3>

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


# =================================
# KPI
# =================================

a,b,c,d=st.columns(4)

a.metric(
"🌡 Current",
f'{latest["temperature"]:.1f}°C'
)

b.metric(
"🔥 Peak",
f'{peak:.1f}°C'
)

c.metric(
"🎯 Confidence",
f'{confidence}%'
)

d.metric(
"⚠ Risk",
risk
)


# =================================
# ALERT
# =================================

st.subheader(
"🚨 Forecast Alert"
)

if risk=="Extreme":

    st.error(
        "Extreme Heat Expected"
    )

elif risk=="Moderate":

    st.warning(
        "Moderate Weather Risk"
    )

else:

    st.success(
        "Conditions Stable"
    )


# =================================
# HEALTH
# =================================

st.subheader(
"🩺 Forecast Health"
)

st.progress(
confidence/100
)


# =================================
# CHART
# =================================

st.subheader(
"📈 24 Hour Forecast"
)

fig=go.Figure()

fig.add_trace(

go.Scatter(

x=forecast["hour"],

y=forecast["temperature"],

name="Temperature"

)

)

fig.add_trace(

go.Scatter(

x=forecast["hour"],

y=forecast["humidity"],

name="Humidity"

)

)

fig.update_layout(
height=550
)

st.plotly_chart(
fig,
use_container_width=True
)


# =================================
# TABLE
# =================================

st.subheader(
"📄 Forecast Data"
)

st.dataframe(

forecast,

use_container_width=True

)


# =================================
# EXPORT
# =================================

st.subheader(
"⬇ Export Forecast"
)

file,mime,ext=export_data(
forecast
)

st.download_button(

"Download Forecast",

file,

f"urbanmind_forecast{ext}",

mime,

use_container_width=True

)


# =================================
# INSIGHTS
# =================================

st.subheader(
"🧠 AI Insights"
)

st.info(
f"""
Average Temp:
{forecast.temperature.mean():.1f}°C

Average Humidity:
{forecast.humidity.mean():.1f}%

Peak:
{peak:.1f}°C
"""
)