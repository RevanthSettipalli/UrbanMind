import streamlit as st
from pathlib import Path
import sys

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar
from utils.settings import (
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
# HERO
# ====================================

st.markdown("""
<div style='
padding:40px;
border-radius:28px;

background:
linear-gradient(
135deg,
#031120,
#0b5ea8
);

color:white;

margin-bottom:30px;
'>

<h1>⚙️ Settings</h1>

<p>Customize UrbanMind</p>

<p>
Theme • Notifications • Export
</p>

</div>
""",
unsafe_allow_html=True
)


# ====================================
# APPEARANCE
# ====================================

st.subheader(
    "🎨 Appearance"
)

theme = st.selectbox(

    "Theme",

    [
        "Dark",
        "Light"
    ],

    index=0
    if config.get(
        "theme"
    ) == "Dark"

    else 1

)


refresh = st.slider(

    "Refresh Rate",

    5,

    60,

    config.get(
        "refresh",
        10
    )

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


# ====================================
# SAVE
# ====================================

if st.button(

    "💾 Save Settings",

    use_container_width=True

):

    new_settings = {

        "theme":theme,

        "refresh":refresh,

        "notify":notify,

        "export":export

    }

    save_settings(
        new_settings
    )

    st.session_state.update(
        new_settings
    )

    st.success(
        "Settings Applied Successfully"
    )

    st.rerun()


# ====================================
# CURRENT
# ====================================

st.divider()

st.subheader(
    "🧠 Current Settings"
)

config = load_settings()

a,b,c,d = st.columns(4)

a.metric(

    "Theme",

    config["theme"]

)

b.metric(

    "Refresh",

    f'{config["refresh"]}s'

)

c.metric(

    "Alerts",

    "ON"

    if config["notify"]

    else "OFF"

)

d.metric(

    "Export",

    config["export"]

)


# ====================================
# INFO
# ====================================

st.info(
"""
Theme changes apply after saving.

Export format affects downloads.

Refresh controls live updates.
"""
)