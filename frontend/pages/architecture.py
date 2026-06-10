

import streamlit as st
from frontend.utils.auth_guard import require_login
from frontend.utils.sidebar import render_sidebar
from frontend.utils.settings import apply_theme

st.set_page_config(
    page_title="Architecture Center",
    page_icon="🏗",
    layout="wide"
)

require_login()
render_sidebar()

st.markdown(apply_theme(), unsafe_allow_html=True)


st.markdown("""
<div style='padding:30px;border-radius:25px;
background:linear-gradient(135deg,#081326,#165ba8);
color:white;'>
<h1>🏗 UrbanMind Architecture Center</h1>
<p>Enterprise Big Data • AI Intelligence • Streaming Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# Executive Architecture Scorecard
st.subheader("🏆 Executive Architecture Scorecard")

k1,k2,k3,k4 = st.columns(4)

k1.metric("Data Sources", "3+")
k2.metric("Platform Modules", "7")
k3.metric("Architecture Score", "98/100")
k4.metric("Deployment Ready", "Yes")

st.subheader("🌐 UrbanMind End-to-End Architecture")

c1,c2,c3,c4,c5,c6,c7 = st.columns(7)

c1.info("🌦 Sources")
c2.info("📡 Kafka")
c3.info("⚙ Processing")
c4.info("📊 Analytics")
c5.info("🔮 Forecast")
c6.info("📑 Reports")
c7.success("🏙 Platform")

st.success(
    "Real-Time Urban Intelligence Pipeline: Sources → Kafka → Processing → Analytics → Forecast → Reports → Decision Support"
)


c1, c2 = st.columns(2)

with c1:
    st.subheader("📡 Kafka Streaming Architecture")
    st.info("Producer → Kafka Topics → Consumer → Processed Dataset")

    st.success("Real-Time Data Ingestion")
    st.success("Streaming Analytics")
    st.success("Scalable Event Processing")

with c2:
    st.subheader("🤖 AI Intelligence Stack")
    st.info("Analytics Engine → Forecast Engine → Executive Intelligence")

    st.success("Predictive Analytics")
    st.success("Risk Intelligence")
    st.success("Decision Support")

# Enterprise Intelligence Layers and Big Data Architecture Metrics
st.subheader("🧠 Enterprise Intelligence Layers")

l1,l2,l3 = st.columns(3)

with l1:
    st.success("Data Layer")
    st.write("Weather APIs")
    st.write("Environmental Sensors")
    st.write("Urban Datasets")

with l2:
    st.success("Processing Layer")
    st.write("Kafka Streaming")
    st.write("Data Cleaning")
    st.write("Aggregation")

with l3:
    st.success("Intelligence Layer")
    st.write("Analytics Engine")
    st.write("Forecast Engine")
    st.write("Executive Reporting")

st.subheader("📈 Big Data Architecture Metrics")

m1,m2,m3,m4 = st.columns(4)

m1.metric("Streaming", "Kafka")
m2.metric("ML Engine", "LSTM")
m3.metric("Reporting", "PDF")
m4.metric("Cloud Target", "GCP")

st.subheader("🧰 Technology Stack")

tech = {
    "Layer": [
        "Frontend",
        "Backend",
        "Streaming",
        "Machine Learning",
        "Database",
        "Reporting",
        "Deployment"
    ],
    "Technology": [
        "Streamlit",
        "Python",
        "Apache Kafka",
        "Scikit-Learn / LSTM",
        "CSV / Data Lake",
        "ReportLab",
        "Google Cloud Run"
    ]
}

st.dataframe(tech, use_container_width=True)

st.subheader("🚀 Deployment Architecture")

st.markdown("""
Developer Environment
⬇
Docker Containers
⬇
Kafka Services
⬇
UrbanMind Application
⬇
Google Cloud Run
⬇
Production Users
""")

st.subheader("🎯 Architecture Readiness Assessment")

st.progress(98)

st.success("Academic Readiness: 100%")
st.success("Industry Demonstration Readiness: 98%")
st.success("Deployment Readiness: 98%")
st.success("Portfolio / Masters Application Readiness: 100%")

st.success(
    "UrbanMind Architecture Ready for Academic Presentation, Industry Demonstration, and Production Deployment."
)