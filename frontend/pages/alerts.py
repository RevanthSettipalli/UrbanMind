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

CSV = ROOT/"data"/"weather_history.csv"

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


def save_alerts(data):

    try:

        with open(
            ALERT_FILE,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    except:
        pass


def load_alerts():

    try:

        with open(
            ALERT_FILE
        ) as f:

            return json.load(f)

    except:

        return []


df = load_weather()

stored = load_alerts()


# =====================================
# HEADER
# =====================================

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

left,right = st.columns([4,1])

with left:

    st.title(
        "🚨 Alert Intelligence Center"
    )

with right:

    st.info(
        IST.strftime(
            "%I:%M:%S %p"
        )
    )


# =====================================
# BUILD ALERTS
# =====================================

alerts = []

if not df.empty:

    latest = df.tail(1).iloc[0]

    temp = float(
        latest.get(
            "temperature",
            0
        )
    )

    hum = float(
        latest.get(
            "humidity",
            0
        )
    )

    city = str(
        latest.get(
            "city",
            "Unknown"
        )
    )

    if temp >= 40:

        alerts.append({

            "level":"HIGH",

            "message":
            f"🔥 Extreme Heat in {city}"

        })

    elif temp >= 35:

        alerts.append({

            "level":"MEDIUM",

            "message":
            f"🌡 Temperature Rising in {city}"

        })

    if hum >= 85:

        alerts.append({

            "level":"HIGH",

            "message":
            f"🌧 Humidity Critical"

        })

    if len(alerts) == 0:

        alerts.append({

            "level":"LOW",

            "message":
            "🟢 Urban Conditions Stable"

        })

save_alerts(
    alerts
)


# =====================================
# KPI
# =====================================

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
        if x["level"]=="HIGH"
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

    if alert["level"]=="HIGH":

        st.error(
            alert["message"]
        )

    elif alert["level"]=="MEDIUM":

        st.warning(
            alert["message"]
        )

    else:

        st.success(
            alert["message"]
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