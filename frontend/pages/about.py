import streamlit as st

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar


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


# ==================================
# HERO
# ==================================

st.markdown("""
<style>

.hero{

padding:40px;

border-radius:30px;

background:
linear-gradient(
135deg,
#04111f,
#0d4d88
);

color:white;

}

</style>
""",
unsafe_allow_html=True
)


st.markdown("""
<div class='hero'>

# 🌍 UrbanMind

Smart City Intelligence Platform

AI • Big Data • Digital Twin

</div>
""",
unsafe_allow_html=True
)


# ==================================
# CONTENT
# ==================================

st.divider()

st.subheader(
"🚀 Overview"
)

st.write("""

UrbanMind is an advanced urban
intelligence platform built using:

• Streamlit

• Machine Learning

• Big Data

• Geo Intelligence

• Forecast Systems

• Digital Twin

""")


st.subheader(
"🏗 Architecture"
)

st.code("""

Producer
↓

Dataset

↓

Analytics

↓

Forecast

↓

Geo

↓

Monitor

↓

Assistant

""")


st.subheader(
"🧠 Modules"
)

modules=[

"Dashboard",

"Analytics",

"Forecast",

"Geo",

"Monitor",

"Assistant",

"Settings"

]

for m in modules:

    st.success(m)


st.divider()

st.caption(
"UrbanMind v2.0"
)