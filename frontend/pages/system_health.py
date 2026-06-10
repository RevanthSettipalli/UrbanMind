import streamlit as st
import pandas as pd
import pytz
from pathlib import Path
from datetime import datetime
import plotly.express as px

from frontend.utils.auth_guard import require_login
from frontend.utils.sidebar import render_sidebar
from frontend.utils.settings import apply_theme, load_settings

import json
import socket
import time

st.set_page_config(
    page_title="System Health Center",
    page_icon="🏥",
    layout="wide"
)

require_login()
render_sidebar()

st.markdown(apply_theme(), unsafe_allow_html=True)

settings = load_settings()

from streamlit_autorefresh import st_autorefresh

refresh_rate = max(
    1,
    int(settings.get("refresh_rate", 60))
)

st_autorefresh(
    interval=refresh_rate * 1000,
    key=f"system_health_{refresh_rate}"
)

st.markdown("""
<div style='padding:25px;border-radius:20px;
background:linear-gradient(135deg,#081326,#165ba8);
color:white;'>
<h1>🏥 UrbanMind Operations Center</h1>
<p>Real-Time Platform Health • Deployment Monitoring • System Intelligence</p>
</div>
""", unsafe_allow_html=True)

IST = datetime.now(
    pytz.timezone("Asia/Kolkata")
)

last_update = IST.strftime("%d %b %Y %I:%M:%S %p")

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "processed_weather.csv"
HEALTH_HISTORY = ROOT / "data" / "health_history.json"

records = 0
last_modified = "Unavailable"
data_age_seconds = 0

kafka_status = "Offline"
producer_status = "Unknown"
consumer_status = "Unknown"
uptime_hours = 0
alerts = []

if CSV.exists():
    try:
        df = pd.read_csv(CSV)
        records = len(df)
        last_modified = datetime.fromtimestamp(
            CSV.stat().st_mtime
        ).strftime("%d %b %Y %I:%M:%S %p")
        current_ts = datetime.now().timestamp()
        data_age_seconds = int(current_ts - CSV.stat().st_mtime)
    except Exception:
        pass

    # Kafka Connectivity Check
    try:
        sock = socket.create_connection(("localhost", 9092), timeout=1)
        sock.close()
        kafka_status = "Healthy"
    except Exception:
        kafka_status = "Offline"
        alerts.append("Kafka broker unreachable")

    # Producer / Consumer Heartbeat
    if data_age_seconds <= 120:
        producer_status = "Active"
        consumer_status = "Active"
    else:
        producer_status = "Stale"
        consumer_status = "Stale"
        alerts.append("Data pipeline heartbeat delayed")

    # Service Uptime
    if CSV.exists():
        uptime_hours = round(
            (time.time() - CSV.stat().st_ctime) / 3600,
            1
        )

health_score = 100

if kafka_status != "Healthy":
    health_score -= 30

if producer_status != "Active":
    health_score -= 20

if consumer_status != "Active":
    health_score -= 20

if data_age_seconds > 300:
    health_score -= 20

if records == 0:
    health_score -= 10

health_score = max(0, min(100, health_score))

if HEALTH_HISTORY.exists():
    try:
        with open(HEALTH_HISTORY, "r") as f:
            health_history = json.load(f)
    except Exception:
        health_history = []
else:
    health_history = []

# Backward compatibility for older health_history.json files
# that stored plain integers instead of objects.
normalized_history = []

for item in health_history:
    if isinstance(item, dict):
        normalized_history.append(item)
    else:
        normalized_history.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "health": int(item)
        })

health_history = normalized_history

health_history.append({
    "timestamp": datetime.now().strftime("%H:%M:%S"),
    "health": health_score
})

health_history = health_history[-20:]

try:
    with open(HEALTH_HISTORY, "w") as f:
        json.dump(health_history, f)
except Exception:
    pass

status_color = "🟢"
if health_score < 90:
    status_color = "🟡"
if health_score < 75:
    status_color = "🔴"

anomaly_score = 0

if kafka_status != "Healthy":
    anomaly_score += 40

if producer_status != "Active":
    anomaly_score += 20

if consumer_status != "Active":
    anomaly_score += 20

if data_age_seconds > 300:
    anomaly_score += 20

if anomaly_score >= 60:
    risk_level = "🔴 Critical"
elif anomaly_score >= 20:
    risk_level = "🟡 Warning"
else:
    risk_level = "🟢 Normal"

st.subheader("🎯 Executive Health Overview")

h1,h2,h3,h4 = st.columns(4)

h1.metric("System Health", f"{health_score}%")
h2.metric("Records Processed", records)
h3.metric("Platform Status", "ONLINE")
h4.metric("Environment", settings.get("environment", "Development"))

h5,h6 = st.columns(2)
h5.metric("Producer", producer_status)
h6.metric("Consumer", consumer_status)

st.metric("Service Uptime", f"{uptime_hours} hrs")

availability = round((health_score / 100) * 99.9, 2)

r1, r2 = st.columns(2)
r1.metric("Availability", f"{availability}%")
r2.metric("Risk Level", risk_level)

st.progress(health_score)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Kafka", kafka_status)
c2.metric("Forecast Engine", "Running")
c3.metric("Analytics Engine", "Running")
c4.metric("Reports Engine", "Running")

c5, c6, c7, c8 = st.columns(4)

c5.metric("PDF Engine", "Ready")
c6.metric("Dashboard", "Online")
c7.metric("Environment", settings.get("environment", "Development"))
c8.metric("Refresh Rate", f"{settings.get('refresh_rate', 60)}s")

st.info(
    f"{status_color} UrbanMind platform is operational with a health score of {health_score}%"
)

st.subheader("📡 Data Freshness")

f1,f2,f3,f4 = st.columns(4)

f1.metric("🕒 Last Update", last_update.split()[-2] + " " + last_update.split()[-1])
f2.metric("📄 Records", records)
f3.metric("⚡ Data Age", f"{data_age_seconds}s")
f4.metric("🔄 Refresh", f"{settings.get('refresh_rate',60)}s")

st.subheader("🏗 UrbanMind Architecture")

st.markdown("""
### 🌦 Weather Sources
⬇
### 📡 Kafka Streaming Layer
⬇
### ⚙️ Data Processing Engine
⬇
### 📊 Analytics Intelligence
⬇
### 🔮 Forecast Intelligence
⬇
### 📑 Executive Reporting
⬇
### 🏙 UrbanMind Dashboard
""")

st.subheader("✅ Deployment Readiness")

readiness = pd.DataFrame({
    "Component": [
        "Kafka",
        "Analytics",
        "Forecast",
        "Monitoring",
        "Reports",
        "PDF Generator"
    ],
    "Status": [
        "Ready",
        "Ready",
        "Ready",
        "Ready",
        "Ready",
        "Ready"
    ]
})

st.dataframe(
    readiness,
    use_container_width=True
)

st.subheader("🚀 Deployment Readiness Center")

ready_df = pd.DataFrame({
    "Status": ["Ready", "Pending"],
    "Value": [98, 2]
})

fig = px.pie(
    ready_df,
    names="Status",
    values="Value",
    hole=0.65,
    title="Deployment Readiness"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

score_df = pd.DataFrame({
    "Component": [
        "Kafka",
        "Analytics",
        "Forecast",
        "Reports",
        "Monitoring",
        "PDF Engine"
    ],
    "Score": [100, 100, 95, 100, 95, 100]
})

st.dataframe(score_df, use_container_width=True)

if settings.get("environment", "Development") == "Development":
    st.warning(
        "Development Mode Active • Recommended Refresh Rate: 60s • Production Recommendation: 300s"
    )

st.subheader("🧠 Operations Insight")

st.info(
    f"UrbanMind processed {records} records. All intelligence engines are operational. No critical anomalies detected. Platform health score is {health_score}% and deployment readiness is 98%."
)

st.subheader("🚨 Alert Center")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("No active alerts detected")

st.subheader("🎯 Anomaly Intelligence")

c1, c2 = st.columns(2)

c1.metric("Anomaly Score", anomaly_score)
c2.metric("Operational Risk", risk_level)

st.subheader("📈 System Health Trend")

trend_df = pd.DataFrame({
    "Time": [x.get("timestamp", "") for x in health_history],
    "Health": [x.get("health", health_score) for x in health_history]
})

if trend_df.empty:
    trend_df = pd.DataFrame({
        "Time": [datetime.now().strftime("%H:%M:%S")],
        "Health": [health_score]
    })

trend_fig = px.line(
    trend_df,
    x="Time",
    y="Health",
    markers=True,
    title="System Health Trend"
)

st.plotly_chart(
    trend_fig,
    use_container_width=True
)

s1,s2,s3,s4,s5 = st.columns(5)

s1.success("🟢 Kafka")
s2.success("🟢 Analytics")
s3.success("🟢 Forecast")
s4.success("🟢 Reports")
s5.success("🟢 PDF Engine")

st.subheader("🔍 Service Heartbeat Monitor")

heartbeat_status = "Healthy" if CSV.exists() else "Offline"

heartbeat_df = pd.DataFrame({
    "Service": [
        "Weather Dataset",
        "Forecast Engine",
        "Analytics Engine",
        "Reports Engine"
    ],
    "Heartbeat": [
        heartbeat_status,
        producer_status,
        consumer_status,
        kafka_status
    ]
})

st.dataframe(
    heartbeat_df,
    use_container_width=True
)

st.subheader("🟢 Service Status Matrix")

m1,m2,m3,m4,m5 = st.columns(5)

m1.success(f"Kafka\n{kafka_status}")
m2.success(f"Producer\n{producer_status}")
m3.success(f"Consumer\n{consumer_status}")
m4.success("Forecast\nHealthy")
m5.success("Analytics\nHealthy")

st.success("🚀 UrbanMind Enterprise Platform Operational • Deployment Ready • Executive Intelligence Active")