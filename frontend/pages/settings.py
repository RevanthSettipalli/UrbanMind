import streamlit as st

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


if st.button(

"💾 Save Settings",

use_container_width=True

):

    settings = {

        "theme":theme,

        "refresh":refresh,

        "notify":notify,

        "export":export

    }

    save_settings(
        settings
    )

    st.success(
        "Settings Saved Successfully"
    )

    st.rerun()

st.markdown(
"</div>",
unsafe_allow_html=True
)


# ====================================
# CURRENT SETTINGS
# ====================================

st.subheader(
"🧠 Current Settings"
)

config = load_settings()

a,b,c,d = st.columns(4)

with a:

    st.metric(

        "Theme",

        config["theme"]

    )

with b:

    st.metric(

        "Refresh",

        f'{config["refresh"]}s'

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


# ====================================
# INFO
# ====================================

st.info(
"""
• Save to apply changes

• Export format controls downloads

• Refresh controls live updates
"""
)