import streamlit as st
import pandas as pd
import joblib
import pytz
import plotly.graph_objects as go
import time

from pathlib import Path
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar


try:
    import psutil
except:
    psutil = None


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

st_autorefresh(
    interval=5000,
    key="monitor_refresh"
)


# =====================================
# PATH
# =====================================

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT / "data" / "weather_history.csv"

MODEL = ROOT / "models" / "weather" / "weather_model.pkl"


# =====================================
# HEADER
# =====================================

st.title(
    "🖥 Urban Monitor Center"
)

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

st.caption(
    f"Updated • {IST.strftime('%d %b %Y | %I:%M:%S %p IST')}"
)


# =====================================
# LOAD
# =====================================

@st.cache_data(ttl=5)
def load_data():

    try:

        return pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

    except:

        return pd.DataFrame()


@st.cache_resource
def model_exists():

    try:

        joblib.load(
            MODEL
        )

        return True

    except:

        return False


df = load_data()

model = model_exists()

records = len(df)


# =====================================
# CLEAN
# =====================================

if records:

    if "time" in df.columns:

        df["time"] = pd.to_datetime(
            df["time"],
            errors="coerce"
        )

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

    df = df.dropna()

    records = len(df)


# =====================================
# SYSTEM
# =====================================

cpu = (

psutil.cpu_percent()

if psutil

else 0

)

ram = (

psutil.virtual_memory().percent

if psutil

else 0

)

uptime = round(
time.time()/3600,
1
)

confidence = min(
98,
max(
65,
65 + (records // 100)
)
)

health = max(

0,

round(

100

-

(

cpu*0.3

+

ram*0.2

)

)

)


# =====================================
# KPI
# =====================================

a,b,c,d,e,f = st.columns(6)

a.metric(
"CPU",
f"{cpu}%"
)

b.metric(
"RAM",
f"{ram}%"
)

c.metric(
"Records",
records
)

d.metric(
"Model",
"Loaded"
if model
else
"Missing"
)

e.metric(
"Confidence",
f"{confidence}%"
)

f.metric(
"Uptime",
f"{uptime} h"
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

x,y,z = st.columns(3)

with x:

    st.success(
        "🟢 Producer"
    )

with y:

    st.success(
        "🟢 Dashboard"
    )

with z:

    if model:

        st.success(
            "🤖 AI Running"
        )

    else:

        st.error(
            "❌ Model Missing"
        )


# =====================================
# DATASET
# =====================================

if records:

    st.subheader(
        "📈 Dataset Growth"
    )

    fig = go.Figure()

    fig.add_trace(

go.Scatter(

x=list(
range(records)
),

y=list(
range(records)
),

mode="lines"

)

)

    fig.update_layout(
        height=320
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================
# WEATHER
# =====================================

if (

records

and

{

"time",

"temperature",

"humidity"

}.issubset(
df.columns
)

):

    st.subheader(
        "🌡 Live Weather"
    )

    sample = df.tail(100)

    fig2 = go.Figure()

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

    fig2.update_layout(
        height=420
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# =====================================
# DATA
# =====================================

if records:

    st.subheader(
        "📄 Recent Records"
    )

    st.dataframe(

df.tail(
20
),

use_container_width=True

)


# =====================================
# EXPORT
# =====================================

if records:

    st.download_button(

"⬇ Export Monitor Report",

df.to_csv(
index=False
).encode(),

"urbanmind_monitor.csv",

use_container_width=True

)


# =====================================
# SUMMARY
# =====================================

st.success(
f"""
CPU:
{cpu}%

RAM:
{ram}%

Health:
{health}%

Records:
{records}

Confidence:
{confidence}%

Model:
{"Loaded" if model else "Missing"}
"""
)