import streamlit as st

from frontend.utils.auth_guard import require_login
from frontend.utils.sidebar import render_sidebar
from frontend.utils.settings import (
    load_settings,
    save_settings,
    apply_theme
)


# ====================================
# PAGE
# ====================================

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

require_login()

render_sidebar()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)


# ====================================
# LOAD
# ====================================

config = load_settings()


# ====================================
# STYLE
# ====================================

st.markdown("""
<style>

.hero{
padding:32px;

border-radius:26px;

background:
linear-gradient(
135deg,
#031120,
#0b5ea8
);

color:white;

margin-bottom:28px;
}

.hero h1{
margin:0;

font-size:52px;

font-weight:700;
}

.card{

padding:26px;

background:white;

border-radius:22px;

box-shadow:
0 10px 30px
rgba(0,0,0,.06);

margin-bottom:22px;
}

[data-testid="metric-container"]{

background:white;

padding:20px;

border-radius:18px;

box-shadow:
0 8px 20px
rgba(0,0,0,.04);

}

.stButton>button{

height:55px;

border-radius:14px;

font-size:18px;

}

</style>
""",
unsafe_allow_html=True)


# ====================================
# HERO
# ====================================

st.markdown(
"""
<div class='hero'>
<h1>⚙️ Settings</h1>
</div>
""",
unsafe_allow_html=True
)

# ====================================
# CONTROL CENTER
# ====================================

st.subheader("🏛 UrbanMind Control Center")

cc1,cc2,cc3,cc4 = st.columns(4)

cc1.metric("🤖 AI Engine","Active")
cc2.metric("📡 Data Streams","Running")
cc3.metric("🔒 Security","Protected")
cc4.metric("⚡ Platform","Online")


# ====================================
# SETTINGS PANEL
# ====================================

st.markdown(
"<div class='card'>",
unsafe_allow_html=True
)

st.subheader(
"🎨 Appearance"
)

theme = st.selectbox(

"Theme",

["Dark","Light"],

index=0
if config.get(
"theme"
)=="Dark"
else 1

)

environment = st.selectbox(
    "Environment",
    ["Development","Testing","Production"],
    index=0
)

platform_mode = st.selectbox(
    "Platform Mode",
    ["Development","Production"],
    index=0
)

if platform_mode == "Production":
    refresh_default = 300
else:
    refresh_default = config.get("refresh_rate",60)

refresh = st.slider(
    "Refresh Rate",
    5,
    300,
    refresh_default
)

notify = st.toggle(

"Enable Notifications",

value=config.get(
"notify",
True
)

)


export = st.selectbox(

"Export Format",

[

"CSV",

"JSON",

"Excel"

],

index=[

"CSV",

"JSON",

"Excel"

].index(

config.get(
"export",
"CSV"
)

)

)

st.subheader("🧠 AI Configuration")

ai_insights = st.toggle("AI Insights", value=True)
forecast_engine = st.toggle("Forecast Engine", value=True)
governance_engine = st.toggle("Governance Engine", value=True)
copilot_engine = st.toggle("AI Copilot", value=True)

if st.button(

"💾 Save Settings",

use_container_width=True

):

    settings = {

        "theme": theme,

        "refresh_rate": refresh,

        "notify": notify,

        "export": export,

        "environment": environment,
        "platform_mode": platform_mode,
        "ai_insights": ai_insights,
        "forecast_engine": forecast_engine,
        "governance_engine": governance_engine,
        "copilot_engine": copilot_engine,

    }

    save_settings(
        settings
    )

    st.session_state["settings"] = settings

    st.cache_data.clear()

    st.success(
        f"Settings Saved • Refresh set to {refresh}s"
    )

    st.rerun()

st.markdown(
"</div>",
unsafe_allow_html=True
)

# ====================================
# DEPLOYMENT CENTER
# ====================================

st.subheader("🚀 Deployment Configuration")

st.success("Target Deployment: Google Cloud Run")

# ====================================
# DATA PIPELINE STATUS
# ====================================

st.subheader("📡 Data Pipeline Status")

p1,p2,p3,p4 = st.columns(4)

p1.metric("Kafka","Running")
p2.metric("Producer","Running")
p3.metric("Consumer","Running")
p4.metric("Database","Connected")

# ====================================
# SECURITY CENTER
# ====================================

st.subheader("🔒 Security Center")

st.success("Login Protection Enabled")
st.success("Session Security Active")
st.success("Access Control Protected")

# ====================================
# BACKUP CENTER
# ====================================

st.subheader("💾 Backup & Recovery")

b1,b2,b3 = st.columns(3)

b1.button("Export Config")
b2.button("Backup Settings")
b3.button("Restore Settings")

# ====================================
# PLATFORM HEALTH
# ====================================

st.subheader("🩺 Platform Health")

h1,h2,h3,h4 = st.columns(4)

h1.metric("CPU","24%")
h2.metric("RAM","38%")
h3.metric("Storage","72%")
h4.metric("Health","98%")


# ====================================
# CURRENT SETTINGS
# ====================================

st.subheader(
"🧠 Current Settings"
)

a,b,c,d,e,f = st.columns(6)

with a:

    st.metric(

        "Theme",

        config["theme"]

    )

with b:

    st.metric(

        "Refresh",

        f'{config.get("refresh_rate",10)}s'

    )

with c:

    st.metric(

        "Alerts",

        "ON"

        if config["notify"]

        else "OFF"

    )

with d:

    st.metric(

        "Export",

        config["export"]

    )

with e:
    st.metric(
        "Mode",
        config.get("platform_mode","Development")
    )

with f:
    st.metric(
        "Environment",
        config.get("environment","Development")
    )


# ====================================
# INFO
# ====================================

st.markdown("## 📌 UrbanMind Configuration Summary")

st.success(
    f"""
Theme: {config.get('theme','Dark')}

Refresh Rate: {config.get('refresh_rate',60)}s

Environment: {config.get('environment','Development')}

Mode: {config.get('platform_mode','Development')}

Deployment: Google Cloud Run

AI Status: Active

Security Status: Protected

UrbanMind Administration Center Operational
"""
)