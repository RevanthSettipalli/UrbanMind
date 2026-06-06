import streamlit as st

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar
from utils.settings import (
    apply_theme,
    load_settings
)


# ==================================
# PAGE
# ==================================

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

require_login()

render_sidebar()

settings = load_settings()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)


# ==================================
# STYLE
# ==================================

st.markdown("""
<style>

.block-container{
padding-top:.4rem!important;
}

.hero{

padding:45px;

border-radius:30px;

background:
linear-gradient(
135deg,
#04111f,
#0d4d88
);

color:white;

margin-bottom:26px;

}

.hero h1{

font-size:58px;

margin:0;

}

.card{

padding:25px;

border-radius:22px;

background:white;

box-shadow:
0 10px 30px
rgba(0,0,0,.05);

margin-bottom:20px;

}

</style>
""",
unsafe_allow_html=True)


# ==================================
# HERO
# ==================================

st.markdown("""
<div class='hero'>

<h1>
🌍 UrbanMind
</h1>

<h3>

Real-Time Urban Intelligence Platform

</h3>

</div>
""",
unsafe_allow_html=True)


# ==================================
# OVERVIEW
# ==================================

st.subheader(
"🚀 Project Overview"
)

st.markdown("""
UrbanMind is a real-time urban intelligence platform designed to collect, analyze, monitor, visualize and forecast urban conditions using Artificial Intelligence and Big Data technologies.

Core capabilities:

• Real-Time Dashboard

• Forecast Intelligence

• Geo Intelligence

• Monitoring Center

• Urban AI Assistant

• Export & Reporting

• Digital Twin Visualization
""")


# ==================================
# METRICS
# ==================================

a,b,c,d = st.columns(4)

a.metric(
"Pages",
8
)

b.metric(
"AI Modules",
5
)

c.metric(
"Data Source",
"Live"
)

d.metric(
"Status",
"Ready"
)

# ==================================
# EXECUTIVE OVERVIEW
# ==================================

st.subheader("🏛 UrbanMind Executive Overview")

ex1,ex2,ex3,ex4 = st.columns(4)

ex1.metric("🏙 Cities Monitored", "Multiple")
ex2.metric("🧠 Intelligence Modules", "8+")
ex3.metric("🤖 AI Engines", "Active")
ex4.metric("🟢 Platform Status", "Operational")


# ==================================
# ARCHITECTURE
# ==================================

st.subheader(
"🏗 Architecture"
)

st.code("""
Data Sources
     ↓
Kafka Streaming
     ↓
Analytics Engine
     ↓
Forecast Intelligence
     ↓
Geo Intelligence
     ↓
Monitor Center
     ↓
AI Assistant
     ↓
Executive Reports
""")


# ==================================
# CAPABILITIES CENTER
# ==================================

st.subheader("🧠 UrbanMind Capabilities Center")

cap1,cap2,cap3 = st.columns(3)

with cap1:
    st.success("📊 Real-Time Analytics")
    st.success("🖥 Live Monitoring")

with cap2:
    st.success("🔮 Forecast Intelligence")
    st.success("🌍 Digital Twin")

with cap3:
    st.success("🤖 AI Assistant")
    st.success("📄 Executive Reporting")


# ==================================
# MODULES
# ==================================

st.subheader(
"🧠 Core Modules"
)

modules = [

"📊 Dashboard",

"📈 Analytics",

"🔮 Forecast",

"🌍 Geo",

"🖥 Monitor",

"🤖 Assistant",

"⚙ Settings",

"ℹ About"

]

c1,c2 = st.columns(2)

for i,m in enumerate(modules):

    if i%2==0:

        c1.success(m)

    else:

        c2.success(m)


# ==================================
# PLATFORM HIGHLIGHTS
# ==================================

st.subheader("🌍 Platform Highlights")

st.info("Real-Time Analytics • Big Data Architecture • AI Decision Support • Urban Digital Twin • Forecast Intelligence")


# ==================================
# STACK
# ==================================

st.subheader(
"⚙ Technology Stack"
)

st.code("""

Frontend
• Streamlit

Backend
• Python

Analytics
• Pandas
• Plotly

AI
• Machine Learning

Visualization
• Folium

Deployment
• Cloud Ready

""")


# ==================================
# RESEARCH VALUE
# ==================================

st.subheader("🎓 Research & Academic Value")

st.markdown("""
• Big Data Analytics and Streaming Concepts
• Urban Intelligence and Smart City Research
• AI-Powered Decision Support Systems
• Forecasting and Predictive Analytics
• Real-Time Monitoring Architectures
• Master's-Level Big Data Portfolio Project
""")

# ==================================
# DEPLOYMENT ARCHITECTURE
# ==================================

st.subheader("🚀 Deployment Architecture")

st.code("""
Local Development
↓
Docker Containers
↓
Kafka Streaming
↓
UrbanMind Platform
↓
Google Cloud Run
""")


# ==================================
# PROJECT ACHIEVEMENTS
# ==================================

st.subheader("🏆 Project Achievements")

st.success("Multi-Page Urban Intelligence Platform")
st.success("Real-Time Monitoring & Analytics")
st.success("AI-Powered Forecasting Engine")
st.success("Executive Reporting Portal")
st.success("Urban Digital Twin & Geo Intelligence")


# ==================================
# GOAL
# ==================================

st.subheader(
"🎯 Vision"
)

st.success("""
Build a scalable AI-powered
decision support platform
for future smart cities.
""")


# ==================================
# ROADMAP
# ==================================

st.subheader("📌 UrbanMind Roadmap")

v1,v2 = st.columns(2)

with v1:
    st.markdown("""
### Version 1.0
- Dashboard
- Analytics
- Forecast
- Geo
- Monitor
- Assistant
- Reports
""")

with v2:
    st.markdown("""
### Version 2.0
- LSTM Forecasting
- Real PDF Reports
- Policy Simulation
- AI Recommendations
- Advanced Risk Modeling
""")


# ==================================
# AUTHOR
# ==================================

st.subheader("👨‍💻 Project Information")

st.info("Developed as an Urban Intelligence, Big Data, and AI Platform for academic, research, and smart-city decision support use cases.")

# ==================================
# PLATFORM STATISTICS
# ==================================

st.subheader("📊 Platform Statistics")

s1,s2,s3,s4,s5,s6 = st.columns(6)

s1.metric("Pages", "8+")
s2.metric("Modules", "10+")
s3.metric("AI", "Enabled")
s4.metric("Reports", "Ready")
s5.metric("Version", "3.0")
s6.metric("Cloud", "Ready")


st.markdown("## 📌 UrbanMind Executive Summary")

st.success(
f"""
UrbanMind v3.0

Theme: {settings['theme']}

Status: Production Candidate

Domain: Urban Intelligence & Big Data

Deployment Target: Google Cloud Run

Research Focus: Smart Cities, AI, Forecasting, Analytics

UrbanMind Platform Operational
"""
)