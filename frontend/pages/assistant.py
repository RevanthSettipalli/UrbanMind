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

st_autorefresh(
    interval=settings["refresh"] * 1000,
    key="assistant_refresh"
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
# HEADER
# =====================================

left,right = st.columns([5,1])

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

ROOT = Path(__file__).resolve().parents[2]

CSV = ROOT/"data"/"weather_history.csv"


@st.cache_data(ttl=5)
def load():

    try:

        return pd.read_csv(
            CSV
        )

    except:

        return pd.DataFrame()


df = load()


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
# QUICK
# =====================================

st.divider()

st.subheader(
"⚡ Quick Questions"
)

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

st.success(
f"""

Assistant Ready

Theme:
{settings["theme"]}

Export:
{settings["export"]}

Messages:
{len(st.session_state.messages)}

"""
)