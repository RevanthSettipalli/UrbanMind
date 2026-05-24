import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
    
import streamlit as st


# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="UrbanMind",
    page_icon="🌍",
    layout="wide"
)


# =====================================
# HIDE SIDEBAR
# =====================================

st.markdown("""
<style>

/* Hide Streamlit Sidebar */

[data-testid="stSidebar"]{
display:none;
}

[data-testid="collapsedControl"]{
display:none;
}

[data-testid="stSidebarNav"]{
display:none;
}

/* Main Layout */

.block-container{
max-width:1200px;
padding-top:2rem;
padding-bottom:3rem;
}

/* Hero */

.hero{

padding:60px;

border-radius:28px;

background:
linear-gradient(
135deg,
#020617,
#0c4a6e
);

color:white;

text-align:center;

box-shadow:
0 20px 50px rgba(0,0,0,.18);

}

/* Cards */

.card{

padding:28px;

border-radius:18px;

background:#f8fafc;

border:1px solid #e5e7eb;

}

/* Footer */

.footer{

text-align:center;

padding:50px;

opacity:.7;

}

</style>
""",
unsafe_allow_html=True
)


# =====================================
# SESSION
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =====================================
# REDIRECT
# =====================================

if st.session_state.logged_in:

    st.switch_page(
        "pages/dashboard.py"
    )


# =====================================
# HERO
# =====================================

st.markdown("""
<div class='hero'>

<h1 style="font-size:70px;">
🌍 UrbanMind
</h1>

<h2>
Smart City Intelligence Platform
</h2>

<p style="font-size:22px;">

AI • Big Data • Digital Twin • Geo Intelligence

</p>

<p>

Transform Urban Data Into Intelligent Decisions

</p>

</div>
""",
unsafe_allow_html=True
)


st.write("")
st.write("")


# =====================================
# STATS
# =====================================

a,b,c,d=st.columns(4)

a.metric("Modules","5")
b.metric("AI Models","Active")
c.metric("Analytics","Live")
d.metric("Cities","6+")


# =====================================
# OVERVIEW
# =====================================

st.divider()

st.subheader(
"🚀 Platform Overview"
)

st.markdown("""

UrbanMind is an enterprise-scale urban intelligence platform combining:

✔ Artificial Intelligence  
✔ Big Data Analytics  
✔ Forecast Intelligence  
✔ Digital Twin Monitoring  
✔ Geo Intelligence  
✔ Decision Support Systems  

""")



# =====================================
# MODULES
# =====================================

st.divider()

st.subheader(
"✨ Platform Modules"
)

c1,c2,c3=st.columns(3)

with c1:

    st.info(
        "📊 Analytics"
    )

    st.info(
        "🔮 Forecast"
    )

with c2:

    st.info(
        "🌍 Geo Intelligence"
    )

    st.info(
        "🖥 Monitor"
    )

with c3:

    st.info(
        "🤖 AI Engine"
    )

    st.info(
        "📈 Dashboard"
    )


# =====================================
# FLOW
# =====================================

st.divider()

st.subheader(
"🏗 Architecture"
)

st.code("""
Data Producer
↓

Weather Dataset

↓

Analytics

↓

Forecast Engine

↓

Dashboard

↓

Geo Intelligence

↓

Monitor Center
""")


# =====================================
# START
# =====================================

st.divider()

st.subheader(
"🧭 Get Started"
)

left,right=st.columns(2)

with left:

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

        st.switch_page(
            "pages/login.py"
        )

with right:

    if st.button(
        "📝 Register",
        use_container_width=True
    ):

        st.switch_page(
            "pages/register.py"
        )


# =====================================
# STATUS
# =====================================

st.divider()

x,y,z=st.columns(3)

x.metric(
"Authentication",
"Ready"
)

y.metric(
"Dashboard",
"Live"
)

z.metric(
"AI Engine",
"Active"
)


# =====================================
# FOOTER
# =====================================

st.markdown("""
<div class='footer'>

UrbanMind • AI • Big Data • Smart Cities

<br><br>

Built for Research • Industry • Urban Intelligence

</div>
""",
unsafe_allow_html=True
)
