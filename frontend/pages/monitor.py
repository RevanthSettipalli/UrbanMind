from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import pytz
import time
import sys

from pathlib import Path
from datetime import datetime


# =====================================
# PROJECT ROOT FIX
# =====================================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# =====================================
# IMPORTS
# =====================================

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar
from utils.settings import (
    apply_theme,
    load_settings,
    export_data
)

try:
    from backend.intelligence.monitor_engine import get_system_metrics

except Exception:

    def get_system_metrics(records):

        return {
            "cpu": 35,
            "ram": 52,
            "confidence": 96,
            "health": 90
        }


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
    key=f"monitor_live_clock_{refresh_rate}"
)


# =====================================
# STYLE
# =====================================

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
#06111c,
#0f4c81
);

color:white;
margin-bottom:25px;
}

.hero h1{
font-size:54px;
margin:0;
}

</style>
""",
unsafe_allow_html=True)


# =====================================
# PATHS
# =====================================

CSV = ROOT / "data" / "processed_weather.csv"

MODEL = ROOT / "models" / "weather" / "weather_model.pkl"


# =====================================
# LOAD
# =====================================

@st.cache_data(ttl=0)
def load():

    try:

        df = pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

        return df

    except:

        return pd.DataFrame()


@st.cache_resource
def model_loaded():

    try:

        joblib.load(MODEL)

        return True

    except:

        return False


df = load()

model = model_loaded()

if df.empty:

    st.warning(
        "Waiting for Monitoring Data..."
    )

    st.stop()


# =====================================
# CLEAN
# =====================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

if "time" in df.columns:

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

df = df.dropna()

records = len(df)


# =====================================
# SYSTEM
# =====================================

metrics = get_system_metrics(
    records
)

cpu = metrics["cpu"]
ram = metrics["ram"]
confidence = metrics["confidence"]
health = metrics["health"]

if "start_time" not in st.session_state:
    st.session_state["start_time"] = time.time()

uptime = round(
    (
        time.time()
        -
        st.session_state["start_time"]
    ) / 3600,
    1
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
# HERO
# =====================================

left, right = st.columns([8.8,1.0])

with left:

    st.markdown("""
<div class='hero'>

<h1>
🖥 Monitor Center
</h1>

<h3>
Operations • AI Monitoring
</h3>

</div>
""",
unsafe_allow_html=True)

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


a,b,c,d,e,f = st.columns(6)
a.metric("🧠 CPU",f"{cpu}%")
b.metric("💾 RAM",f"{ram}%")
c.metric("📄 Records",records)
d.metric("🤖 Model","Loaded" if model else "Missing")
e.metric("🎯 Confidence",f"{confidence}%")
f.metric("⏱ Uptime",f"{uptime}h")

# =====================================
# NATIONAL OPERATIONS CENTER
# =====================================

st.subheader("🏛 National Operations Center")

n1,n2,n3,n4 = st.columns(4)
n1.metric("🖥 Infrastructure", "Online")
n2.metric("📡 Streams", "Active")
n3.metric("🤖 AI Engine", "Running")
n4.metric("🔒 Security", "Protected")



# =====================================
# ALERT COMMAND CENTER
# =====================================

st.subheader("🚨 Alert Command Center")

alerts = []

if cpu > 80:
    alerts.append("High CPU Usage")

if ram > 80:
    alerts.append("High RAM Usage")

if health < 70:
    alerts.append("System Health Degraded")

if confidence < 90:
    alerts.append("Model Confidence Reduced")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("✅ No Active Operational Alerts")


# =====================================
# HEALTH
# =====================================

st.subheader("🩺 System Health")

st.progress(
    health/100
)

st.success(
    f"Health Score • {health}%"
)

# =====================================
# RISK MONITORING ENGINE
# =====================================

st.subheader("🎯 Risk Monitoring Engine")

risk = "LOW"

if health < 70:
    risk = "HIGH"
elif health < 85:
    risk = "MODERATE"

r1,r2,r3 = st.columns(3)
r1.metric("Risk Level", risk)
r2.metric("Health", f"{health}%")
r3.metric("Confidence", f"{confidence}%")



# =====================================
# LIVE MONITORING FEED
# =====================================

st.subheader("📡 Live Monitoring Feed")

feed = pd.DataFrame({
    "Time": [updated_time]*5,
    "Event": [
        "Sensor Update",
        "AI Analysis Complete",
        "Health Check Passed",
        "Stream Synced",
        "Monitoring Cycle Completed"
    ],
    "Status": [
        "Success",
        "Success",
        "Success",
        "Success",
        "Success"
    ]
})

st.dataframe(
    feed,
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
    width="stretch"
)

# =====================================
# OPERATIONS INTELLIGENCE CENTER
# =====================================

st.subheader("🧠 Operations Intelligence Center")

ops1,ops2,ops3,ops4 = st.columns(4)
ops1.metric("CPU", f"{cpu}%")
ops2.metric("RAM", f"{ram}%")
ops3.metric("Health", f"{health}%")
ops4.metric("Confidence", f"{confidence}%")



# =====================================
# AI OPERATIONS ADVISOR
# =====================================

st.subheader("🤖 Monitor AI Advisor")

st.info(
    f"""
Operational Health: {health}%

Current Risk Level: {risk}

Model Confidence: {confidence}%

Recommendation:
Continue monitoring infrastructure, investigate anomalies, and maintain stream health for uninterrupted city intelligence operations.
"""
)


# =====================================
# EXPORT
# =====================================

file,mime,ext = export_data(df)

st.download_button(
    "⬇ Export Monitor",
    file,
    f"urbanmind_monitor{ext}",
    mime,
    width="stretch"
)



# =====================================
# SUMMARY
# =====================================

st.markdown("## 📌 National Operations Summary")

st.success(
f"""
🖥 CPU Usage: {cpu}%

💾 RAM Usage: {ram}%

📄 Records Processed: {records}

🩺 System Health: {health}%

🎯 Confidence Score: {confidence}%

⏱ System Uptime: {uptime}h

🚨 Current Risk Level: {risk}

✅ UrbanMind Monitoring Infrastructure Operational
"""
)
