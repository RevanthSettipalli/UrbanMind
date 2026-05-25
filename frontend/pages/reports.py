import streamlit as st
import pandas as pd
import plotly.express as px
import pytz
import sys

from pathlib import Path
from datetime import datetime

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar
from utils.settings import (
    apply_theme,
    load_settings,
    export_data
)


# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="Reports Center",
    page_icon="📑",
    layout="wide"
)

require_login()

render_sidebar()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

settings = load_settings()

from streamlit_autorefresh import st_autorefresh

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
    key=f"reports_live_clock_{refresh_rate}"
)

# =====================================
# TIME
# =====================================

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

# =====================================
# STYLE
# =====================================

st.markdown("""
<style>

.hero{
padding:40px;

border-radius:30px;

background:
linear-gradient(
135deg,
#081326,
#165ba8
);

color:white;

margin-bottom:30px;
}

.hero h1{
font-size:52px;
}

.hero p{
font-size:20px;
}

</style>
""",
unsafe_allow_html=True)


# =====================================
# PATH
# =====================================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CSV = ROOT / "data" / "processed_weather.csv"


# =====================================
# LOAD
# =====================================

@st.cache_data(ttl=0)
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
        "No report data available"
    )

    st.stop()


# =====================================
# CLEAN
# =====================================

df["time"] = pd.to_datetime(
    df["time"],
    errors="coerce"
)

df = df.dropna()


# =====================================
# HEADER
# =====================================

left,right = st.columns([8.8,1.0])

with left:

    st.markdown(f"""
<div class='hero'>

<h1>
📑 Reports Center
</h1>

<p>
Analytics • Insights • Executive Reports
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


# =====================================
# KPI
# =====================================

a,b,c,d = st.columns(4)

a.metric(
"Records",
len(df)
)

b.metric(
"Cities",
df["city"].nunique()
if "city" in df
else 0
)

c.metric(
"Avg Temp",
f"{df['temperature'].mean():.1f}°C"
)

d.metric(
"Avg Humidity",
f"{df['humidity'].mean():.1f}%"
)


# =====================================
# CITY REPORT
# =====================================

if "city" in df:

    report = (
        df
        .groupby(
            "city"
        )
        [
            [
                "temperature",
                "humidity"
            ]
        ]
        .mean()
        .reset_index()
    )

else:

    report = df.copy()


st.subheader(
"🏙 City Ranking"
)

st.dataframe(
report,
use_container_width=True
)


# =====================================
# CHART
# =====================================

st.subheader(
"📊 City Comparison"
)

fig = px.bar(

report,

x="city",

y="temperature",

color="humidity"

)

fig.update_layout(
height=500
)

st.plotly_chart(
fig,
use_container_width=True
)


# =====================================
# EXEC SUMMARY
# =====================================

st.subheader(
"🧠 Executive Summary"
)

st.success(
f"""

UrbanMind analysed
{len(df)}

records across

{report['city'].nunique() if 'city' in report.columns else 0}

cities.

Average temperature:
{df['temperature'].mean():.1f}°C

Average humidity:
{df['humidity'].mean():.1f}%

"""
)


# =====================================
# EXPORT
# =====================================

st.subheader(
"⬇ Export Report"
)

file,mime,ext = export_data(
    report
)

st.download_button(

"Download Report",

file,

f"urbanmind_report{ext}",

mime,

use_container_width=True

)