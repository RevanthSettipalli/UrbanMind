from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import pytz

from pathlib import Path
from datetime import datetime

from utils.auth_guard import require_login
from utils.sidebar import render_sidebar

from utils.settings import (
    apply_theme,
    load_settings,
    export_data
)

from backend.intelligence.assistant_engine import (
    ask_urbanmind
)


# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="Urban AI Assistant",
    page_icon="🤖",
    layout="wide"
)

require_login()

render_sidebar()

settings = load_settings()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

refresh_rate = max(
    1,
    int(
        settings.get(
            "refresh_rate",
            10
        )
    )
)

st_autorefresh(
    interval=refresh_rate * 1000,
    key=f"assistant_live_clock_{refresh_rate}"
)


# =====================================
# STYLE
# =====================================

st.markdown("""
<style>

.block-container{
padding-top:.4rem!important;
}

.hero{

padding:40px;

border-radius:30px;

background:
linear-gradient(
135deg,
#04152f,
#005792
);

color:white;

margin-bottom:24px;

}

.hero h1{

font-size:54px;

margin:0;

}

.quick button{

height:52px;

}

</style>
""",
unsafe_allow_html=True)


# =====================================
# TIME
# =====================================

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

current_time = IST.strftime(
    "%I:%M:%S %p"
).replace(" AM","AM").replace(" PM","PM")

updated_time = IST.strftime(
    "%d %b %Y · %I:%M:%S %p"
).replace(" AM","AM").replace(" PM","PM")

# =====================================
# HEADER
# =====================================

left, right = st.columns([8.8,1.0])

with left:

    st.markdown("""
<div class='hero'>

<h1>
🤖 Urban AI Assistant
</h1>

<h3>
Ask • Analyze • Predict
</h3>

</div>
""",
unsafe_allow_html=True)

with right:

    st.markdown(
f"""
<div style="
background:#dfe8f5;
height:260px;
border-radius:22px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
text-align:center;
padding:18px;
position:relative;
">

<div style="
font-size:44px;
margin-top:0px;
margin-bottom:8px;
line-height:1;
">
🕒
</div>

<div style="
font-size:28px;
font-weight:800;
color:#124f9d;
white-space:nowrap;
line-height:1;
">
{current_time}
</div>

<div style="
margin-top:10px;
font-size:15px;
color:#5a6572;
">
Live Time
</div>

</div>
""",
unsafe_allow_html=True
)


# =====================================
# DATA
# =====================================

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT/"data"/"processed_weather.csv"


@st.cache_data(ttl=0)
def load():

    try:

        return pd.read_csv(
            CSV
        )

    except:

        return pd.DataFrame()


df = load()

# =====================================
# AI COMMAND CENTER
# =====================================

st.subheader("🧠 Urban AI Command Center")

city_count = (
    df["city"].nunique()
    if not df.empty and "city" in df.columns
    else 0
)

record_count = len(df)

a1, a2, a3, a4 = st.columns(4)

a1.metric("🏙 Cities", city_count)
a2.metric("📄 Records", record_count)
a3.metric("🤖 AI Status", "Online")
a4.metric("⚡ Assistant", "Ready")


# =====================================
# SESSION
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages=[]


# =====================================
# CLEAR
# =====================================

_,clear = st.columns([6,1])

with clear:

    if st.button(
        "🗑 Clear"
    ):

        st.session_state.messages=[]

        st.rerun()


# =====================================
# HISTORY
# =====================================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )


# =====================================
# INPUT
# =====================================

prompt = st.chat_input(
    "Ask UrbanMind..."
)


def respond(text):

    if df.empty:

        return "Dataset unavailable"

    return ask_urbanmind(
        text,
        df
    )


# =====================================
# CHAT
# =====================================

if prompt:

    st.session_state.messages.append({

        "role":"user",

        "content":prompt

    })

    with st.chat_message(
        "user"
    ):

        st.write(
            prompt
        )

    answer = respond(
        prompt
    )

    with st.chat_message(
        "assistant"
    ):

        st.write(
            answer
        )

    st.session_state.messages.append({

        "role":"assistant",

        "content":answer

    })


# =====================================
# AI CAPABILITIES
# =====================================

st.subheader("🚀 AI Capabilities")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("📊 Urban Analytics")

with c2:
    st.info("🔮 Forecast Intelligence")

with c3:
    st.info("🌍 City Intelligence")

# =====================================
# SUGGESTED PROMPTS
# =====================================

st.subheader("💡 Suggested AI Prompts")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.info("Which city is healthiest?")

with p2:
    st.info("Show pollution hotspots")

with p3:
    st.info("Predict urban risk")

with p4:
    st.info("Give executive summary")


# =====================================
# QUICK
# =====================================

questions = [
    "temperature",
    "humidity",
    "city",
    "health",
    "forecast"
]

cols = st.columns(5)

for i,q in enumerate(
questions
):

    with cols[i]:

        if st.button(
            q.title()
        ):

            st.info(
                respond(q)
            )


# =====================================
# CITY AI ANALYSIS
# =====================================

if not df.empty and "city" in df.columns:

    st.subheader("🏙 City AI Analysis")

    selected_city = st.selectbox(
        "Select City",
        sorted(df["city"].unique()),
        key="assistant_city"
    )

    city_df = df[df["city"] == selected_city]

    if not city_df.empty:

        latest_city = city_df.tail(1).iloc[0]

        st.info(
            f"AI Analysis: {selected_city} currently reports Temperature {latest_city.get('temperature','N/A')}°C, Humidity {latest_city.get('humidity','N/A')}%, and AQI {latest_city.get('aqi','N/A')}."
        )


# =====================================
# EXECUTIVE AI REPORT
# =====================================

st.subheader("📈 Executive AI Report")

if not df.empty:

    report_text = f"""
UrbanMind Executive Report

Cities Monitored: {city_count}
Records Analysed: {record_count}

The platform is operational and continuously monitoring urban intelligence indicators.

AI Status: Online
Forecasting: Active
Analytics Engine: Active
"""

    st.success(report_text)


# =====================================
# EXPORT
# =====================================

if st.session_state.messages:

    chat = pd.DataFrame(
        st.session_state.messages
    )

    file,mime,ext = export_data(
        chat
    )

    st.download_button(

        "⬇ Export Chat",

        file,

        f"urbanmind_chat{ext}",

        mime,

        use_container_width=True

    )


# =====================================
# STATUS
# =====================================

st.markdown("## 📌 Assistant Executive Summary")

st.success(
    f"""
🤖 Urban AI Assistant Online

🏙 Cities Available: {city_count}

📄 Records Loaded: {record_count}

🎨 Theme: {settings.get('theme','default')}

📤 Export Format: {settings.get('export','csv')}

💬 Messages Processed: {len(st.session_state.messages)}
"""
)

# =====================================
# FORECAST Q&A MODE
# =====================================

st.subheader("🔮 Forecast Q&A")

forecast_question = st.selectbox(
    "Forecast Intelligence",
    [
        "What is the platform status?",
        "How many cities are monitored?",
        "Is AI active?",
        "Show monitoring summary"
    ],
    key="forecast_qa"
)

if forecast_question == "What is the platform status?":
    st.success("UrbanMind systems are operational.")
elif forecast_question == "How many cities are monitored?":
    st.info(f"Currently monitoring {city_count} cities.")
elif forecast_question == "Is AI active?":
    st.success("AI Analytics, Forecasting, and Intelligence modules are active.")
else:
    st.info(f"UrbanMind currently manages {record_count} records across {city_count} cities.")