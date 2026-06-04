import streamlit as st
import pandas as pd
import pytz
import json

from pathlib import Path
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar


# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="UrbanMind Alerts",
    page_icon="🚨",
    layout="wide"
)

require_login()

render_sidebar()

st_autorefresh(
    interval=5000,
    key="alerts_refresh"
)


# =====================================
# PATH
# =====================================

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT/"data"/"processed_weather.csv"

ALERT_FILE = ROOT/"data"/"alerts.json"


# =====================================
# LOAD
# =====================================

@st.cache_data(ttl=5)
def load_weather():

    try:
        return pd.read_csv(
            CSV,
            on_bad_lines="skip"
        )

    except:
        return pd.DataFrame()


def load_alerts():

    try:

        with open(
            ALERT_FILE
        ) as f:

            return json.load(f)

    except:

        return []


df = load_weather()

alerts = load_alerts()


# =====================================
# KPI
# =====================================

if not alerts:

    alerts = [{
        "level": "LOW",
        "message": "🟢 No Active Alerts"
    }]

a,b,c = st.columns(3)

a.metric(
    "Active",
    len(alerts)
)

b.metric(
    "Critical",
    len([
        x
        for x in alerts
        if x.get("level") == "HIGH"
    ])
)

b.metric

c.metric(
    "Status",
    "Live"
)


# =====================================
# DISPLAY
# =====================================

st.subheader(
    "📡 Live Alerts"
)

for alert in alerts:

    if alert.get("level") == "HIGH":

        st.error(
            alert.get("message", "Alert")
        )

    elif alert.get("level") == "MEDIUM":

        st.warning(
            alert.get("message", "Alert")
        )

    else:

        st.success(
            alert.get("message", "Alert")
        )


# =====================================
# HISTORY
# =====================================

st.subheader(
    "📄 Alert History"
)

history = pd.DataFrame(
    alerts
)

st.dataframe(
    history,
    use_container_width=True
)


# =====================================
# DOWNLOAD
# =====================================

st.download_button(

    "⬇ Export Alerts",

    history.to_csv(
        index=False
    ).encode(),

    "urbanmind_alerts.csv",

    use_container_width=True
)


# =====================================
# SUMMARY
# =====================================

st.success(
f"""
Alerts:
{len(alerts)}

Generated:
{IST.strftime('%I:%M %p')}
"""
)