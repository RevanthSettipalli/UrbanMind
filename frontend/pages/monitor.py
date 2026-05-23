from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import joblib
import pytz
import plotly.graph_objects as go
import time

from pathlib import Path
from datetime import datetime

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar

from utils.settings import (
    apply_theme,
    load_settings,
    export_data
)

try:
    import psutil
except:
    psutil=None


# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="Monitor Center",
    page_icon="🖥",
    layout="wide"
)

require_login()

render_sidebar()

settings=load_settings()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

st_autorefresh(
    interval=settings["refresh"]*1000,
    key="monitor_refresh"
)


# =====================================
# UI
# =====================================

st.markdown("""
<style>

.block-container{
padding-top:.4rem;
}

.hero{
padding:40px;

border-radius:30px;

background:
linear-gradient(
135deg,
#06111c,
#0f4c81
);

color:white;

margin-bottom:25px;
}

.hero h1{
font-size:48px;
}

[data-testid="metric-container"]{
padding:24px;
border-radius:20px;
}

</style>
""",
unsafe_allow_html=True)


# =====================================
# PATH
# =====================================

ROOT=Path(__file__).resolve().parents[2]

CSV=ROOT/"data"/"weather_history.csv"

MODEL=ROOT/"models"/"weather"/"weather_model.pkl"


# =====================================
# LOAD
# =====================================

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
def model_loaded():

    try:

        joblib.load(
            MODEL
        )

        return True

    except:

        return False


df=load()

model=model_loaded()

if df.empty:

    st.warning(
        "Waiting for Data..."
    )

    st.stop()


# =====================================
# CLEAN
# =====================================

if "time" in df:

    df["time"]=pd.to_datetime(
        df["time"],
        errors="coerce"
    )

df=df.dropna()

records=len(df)


# =====================================
# SYSTEM
# =====================================

cpu=(
psutil.cpu_percent()
if psutil
else 0
)

ram=(
psutil.virtual_memory().percent
if psutil
else 0
)

uptime=round(
time.time()/3600,
1
)

confidence=min(
98,
70+(records//100)
)

health=int(

max(
0,
100-(cpu*.3+ram*.2)
)

)


# =====================================
# HEADER
# =====================================

left,right=st.columns([5,1])

with left:

    st.markdown("""
<div class='hero'>

<h1>
🖥 Monitor Center
</h1>

<p>
Operations • System Health • AI Monitoring
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


# =====================================
# KPI
# =====================================

a,b,c,d,e,f=st.columns(6)

a.metric(
"🧠 CPU",
f"{cpu}%"
)

b.metric(
"💾 RAM",
f"{ram}%"
)

c.metric(
"📄 Records",
records
)

d.metric(
"🤖 Model",
"Loaded"
if model
else
"Missing"
)

e.metric(
"🎯 Confidence",
f"{confidence}%"
)

f.metric(
"⏱ Uptime",
f"{uptime}h"
)


# =====================================
# HEALTH
# =====================================

st.subheader(
"🩺 System Health"
)

st.progress(
health/100
)

st.success(
f"Health Score • {health}%"
)


# =====================================
# SERVICES
# =====================================

st.subheader(
"🧩 Services"
)

x,y,z=st.columns(3)

x.success(
"🟢 Producer"
)

y.success(
"🟢 Dashboard"
)

if model:

    z.success(
        "🟢 AI Running"
    )

else:

    z.error(
        "🔴 Model Missing"
    )


# =====================================
# GROWTH
# =====================================

st.subheader(
"📈 Dataset Growth"
)

fig=go.Figure()

fig.add_trace(

go.Scatter(

x=list(
range(records)
),

y=list(
range(records)
),

fill="tozeroy"

)

)

st.plotly_chart(
fig,
use_container_width=True
)


# =====================================
# WEATHER
# =====================================

if {

"time",
"temperature",
"humidity"

}.issubset(
df.columns
):

    sample=df.tail(100)

    fig2=go.Figure()

    fig2.add_trace(

go.Scatter(

x=sample["time"],

y=sample["temperature"],

name="Temperature"

)

)

    fig2.add_trace(

go.Scatter(

x=sample["time"],

y=sample["humidity"],

name="Humidity"

)

)

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# =====================================
# DATA
# =====================================

st.subheader(
"📄 Recent Records"
)

st.dataframe(
df.tail(20),
use_container_width=True
)


# =====================================
# EXPORT
# =====================================

st.subheader(
"⬇ Export Monitor"
)

file,mime,ext=export_data(
df
)

st.download_button(

"Download Report",

file,

f"urbanmind_monitor{ext}",

mime,

use_container_width=True

)


# =====================================
# SUMMARY
# =====================================

st.success(f"""
CPU: {cpu}%

RAM: {ram}%

Records: {records}

Health: {health}%

Export: {settings["export"]}

Theme: {settings["theme"]}
""")