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
# ARCHITECTURE
# ==================================

st.subheader(
"🏗 Architecture"
)

st.code("""

Producer

↓

Weather Dataset

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

Export Layer

""")


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
# STATUS
# ==================================

st.success(
f"""

UrbanMind v3.0

Theme:
{settings["theme"]}

Production Candidate

"""
)