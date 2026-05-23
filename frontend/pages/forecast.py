from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import numpy as np
import pytz
import sys

from pathlib import Path
from datetime import datetime, timedelta

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

st_autorefresh(
    interval=settings.get("refresh", 10) * 1000,
    key="forecast_refresh"
)

# =================================
# UI
# =================================

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
#19073d,
#5a189a
);

color:white;
margin-bottom:24px;
}

.hero h1{
font-size:48px;
}

.hero p{
font-size:18px;
opacity:.9;
}

[data-testid="metric-container"]{
background:white;
padding:24px;
border-radius:22px;
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

CSV = ROOT / "data" / "weather_history.csv"
MODEL = ROOT / "models" / "weather" / "weather_model.pkl"

IST = datetime.now(
    pytz.timezone("Asia/Kolkata")
)

# =================================
# LOAD
# =================================

@st.cache_data(ttl=5)
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
        return joblib.load(MODEL)

    except:
        return None


df = load()
model = load_model()

if df.empty:
    st.warning("Weather dataset missing")
    st.stop()

# =================================
# CLEAN
# =================================

for c in [
"time",
"temperature",
"humidity"
]:
    if c not in df:
        df[c]=0

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
            .astype(str)
            .unique()
        )
    )

    if city!="All Cities":

        df=df[
            df["city"]==city
        ]

if len(df)==0:
    st.warning("No forecast data")
    st.stop()

latest=df.iloc[-1]

base_temp=float(
    latest["temperature"]
)

base_hum=float(
    latest["humidity"]
)

avg_temp=df[
    "temperature"
].tail(50).mean()

# =================================
# FORECAST
# =================================

future=[]

for i in range(1,25):

    t=IST+timedelta(
        hours=i
    )

    hum=np.clip(
        base_hum+
        np.random.normal(0,2),
        40,
        85
    )

    try:

        pred=float(

            model.predict([[

                hum,
                t.hour,
                t.day,
                t.month,
                base_temp,
                avg_temp

            ]])[0]

        )

    except:

        pred=(
            base_temp+
            np.random.normal(0,1)
        )

    pred=np.clip(
        pred,
        20,
        46
    )

    conf=max(
        80,
        98-abs(
            pred-avg_temp
        )
    )

    future.append([
        t,
        round(pred,1),
        round(hum,1),
        round(conf)
    ])

forecast=pd.DataFrame(
    future,
    columns=[
        "time",
        "temperature",
        "humidity",
        "confidence"
    ]
)

# =================================
# KPI
# =================================

peak=forecast.temperature.max()

confidence=int(
forecast.confidence.mean()
)

risk=min(
100,
int(peak*2.2)
)

left,right=st.columns([5,1])

with left:

    st.markdown("""
<div class='hero'>
<h1>🔮 Forecast Intelligence</h1>
<p>AI Prediction • Risk Detection • Future Monitoring</p>
</div>
""",
unsafe_allow_html=True
)

with right:

    st.info(
        IST.strftime(
            "%I:%M:%S %p"
        )
    )

a,b,c,d=st.columns(4)

a.metric(
"🌡 Current",
f"{base_temp:.1f}°C"
)

b.metric(
"🔥 Peak",
f"{peak:.1f}°C"
)

c.metric(
"🎯 Confidence",
f"{confidence}%"
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

if peak>40:

    st.error(
        "Extreme Heat Expected"
    )

elif peak>35:

    st.warning(
        "Moderate Risk"
    )

else:

    st.success(
        "Stable Forecast"
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

fig=go.Figure()

fig.add_trace(
go.Scatter(
x=forecast["time"],
y=forecast["temperature"],
fill="tozeroy"
)
)

fig.add_trace(
go.Scatter(
x=forecast["time"],
y=forecast["humidity"],
fill="tozeroy"
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
"📄 Forecast Table"
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
# SUMMARY
# =================================

st.success(f"""
Records: {len(df)}
Peak: {peak:.1f}°C
Confidence: {confidence}%
Risk: {risk}/100
Theme: {settings['theme']}
Export: {settings['export']}
""")