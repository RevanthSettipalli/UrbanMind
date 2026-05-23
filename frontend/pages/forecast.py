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


# =================================
# ROOT
# =================================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT)
    )


# =================================
# HEADER
# =================================

st.title(
    "🔮 Forecast Intelligence"
)

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

st.caption(
f"""
Generated •
{IST.strftime('%d %b %Y | %I:%M %p IST')}
"""
)


# =================================
# PATHS
# =================================

CSV = ROOT/"data"/"weather_history.csv"

MODEL = ROOT/"models"/"weather"/"weather_model.pkl"


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

        return joblib.load(
            MODEL
        )

    except:

        return None


df = load()

model = load_model()


if df.empty:

    st.warning(
        "Weather dataset missing"
    )

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
        df[c] = 0


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
# CITY
# =================================

if "city" in df.columns:

    selected = st.selectbox(

        "🏙 Select City",

        ["All Cities"]

        +

        sorted(
            df["city"]
            .astype(str)
            .unique()
        )

    )

    if selected != "All Cities":

        df = df[
            df["city"]
            ==
            selected
        ]


if len(df) < 10:

    st.warning(
        "Insufficient forecast data"
    )

    st.stop()


latest = df.iloc[-1]

base_temp = float(
latest["temperature"]
)

base_hum = float(
latest["humidity"]
)

avg_temp = (
df["temperature"]
.tail(50)
.mean()
)


# =================================
# FORECAST
# =================================

future=[]

for h in range(1,25):

    t=IST+timedelta(
        hours=h
    )

    hum=np.clip(

base_hum

+

np.random.normal(
0,
2
),

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

base_temp

+

np.random.normal(
0,
1
)

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

peak = forecast[
"temperature"
].max()

risk = min(
100,
int(
peak*2.2
)
)

confidence = int(
forecast[
"confidence"
].mean()
)

a,b,c,d=st.columns(4)

a.metric(
"Current",
f"{base_temp:.1f}°C"
)

b.metric(
"Peak",
f"{peak:.1f}°C"
)

c.metric(
"Confidence",
f"{confidence}%"
)

d.metric(
"Risk",
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
"🖥 Forecast Health"
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

name="Temperature"

)

)

fig.add_trace(

go.Scatter(

x=forecast["time"],

y=forecast["humidity"],

name="Humidity"

)

)

fig.update_layout(
height=500
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

st.download_button(

"⬇ Export Forecast",

forecast.to_csv(
index=False
).encode(),

"urbanmind_forecast.csv"

)


# =================================
# SUMMARY
# =================================

st.success(
f"""
Records:
{len(df)}

Peak:
{peak:.1f}°C

Confidence:
{confidence}%

Risk:
{risk}/100
"""
)