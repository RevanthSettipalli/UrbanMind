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

st_autorefresh(
    interval=settings["refresh"]*1000,
    key="assistant_refresh"
)


# =====================================
# UI
# =====================================

st.markdown("""
<style>

.block-container{
padding-top:.4rem;
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
font-size:48px;
}

.chat-box{

padding:18px;

border-radius:18px;

}

</style>
""",
unsafe_allow_html=True)


# =====================================
# HEADER
# =====================================

left,right=st.columns([5,1])

with left:

    st.markdown("""
<div class='hero'>

<h1>
🤖 Urban AI Assistant
</h1>

<p>
Ask Questions • Analyze Cities • Get Insights
</p>

</div>
""",
unsafe_allow_html=True
)

with right:

    st.info(

datetime.now(

pytz.timezone(
"Asia/Kolkata"

)

).strftime(
"%I:%M:%S %p"
)

)


# =====================================
# DATA
# =====================================

ROOT=Path(__file__).resolve().parents[2]

CSV=ROOT/"data"/"weather_history.csv"


@st.cache_data
def load():

    try:

        return pd.read_csv(
            CSV
        )

    except:

        return pd.DataFrame()


df=load()


# =====================================
# SESSION
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages=[]


# =====================================
# ACTIONS
# =====================================

left,right=st.columns([4,1])

with right:

    if st.button(
        "🗑 Clear Chat"
    ):

        st.session_state.messages=[]

        st.rerun()


# =====================================
# CHAT
# =====================================

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )


prompt=st.chat_input(
"Ask UrbanMind..."
)


# =====================================
# AI ENGINE
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

    q=prompt.lower()

    answer=""

    if df.empty:

        answer="No dataset available."

    elif "temperature" in q:

        answer=f"""
🌡 Average Temperature

{df["temperature"].mean():.1f}°C
"""

    elif "humidity" in q:

        answer=f"""
💧 Average Humidity

{df["humidity"].mean():.1f}%
"""

    elif "city" in q:

        answer="\n".join(
            sorted(
                df[
                    "city"
                ]
                .astype(str)
                .unique()
            )
        )

    elif "health" in q:

        avg=df[
            "temperature"
        ].mean()

        score=max(
            60,
            100-(avg-30)
        )

        answer=f"""
❤️ Urban Health

{score:.0f}%

Status Stable
"""

    elif "risk" in q:

        temp=df[
            "temperature"
        ].mean()

        answer=(
            "⚠ Moderate Risk"

            if temp>35

            else

            "✅ Low Risk"
        )

    elif "summary" in q:

        answer=f"""
📊 Urban Summary

Records:
{len(df)}

Temperature:
{df["temperature"].mean():.1f}°C

Humidity:
{df["humidity"].mean():.1f}%
"""

    else:

        answer="""
I can help with:

• Temperature

• Humidity

• Risk

• Health

• Cities

• Summary
"""

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
# QUICK
# =====================================

st.divider()

st.subheader(
"⚡ Quick Questions"
)

a,b,c,d,e=st.columns(5)

a.info(
"Temperature"
)

b.info(
"Humidity"
)

c.info(
"Risk"
)

d.info(
"Health"
)

e.info(
"Summary"
)


# =====================================
# EXPORT
# =====================================

if st.session_state.messages:

    chat=pd.DataFrame(
        st.session_state.messages
    )

    file,mime,ext=export_data(
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
# SUMMARY
# =====================================

st.success(f"""
Assistant Active

Theme:
{settings["theme"]}

Export:
{settings["export"]}

Messages:
{len(st.session_state.messages)}
""")