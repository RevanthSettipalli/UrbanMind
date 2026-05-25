import streamlit as st
import sys
from pathlib import Path

st.set_page_config(
    page_title="UrbanMind Login",
    page_icon="🌍",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>
[data-testid="stSidebarNav"] {
    display:none;
}

section[data-testid="stSidebar"] {
    display:none;
}

button[kind="header"] {
    display:none;
}
</style>
""",
    unsafe_allow_html=True
)


# =====================
# ROOT PATH FIX
# =====================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# =====================
# IMPORT AUTH
# =====================

from backend.auth.auth import login


# =====================
# SESSION
# =====================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# =====================
# REDIRECT
# =====================

if st.session_state.logged_in:
    st.switch_page("dashboard.py")


# =====================
# UI
# =====================

st.title("🌍 UrbanMind Login")

email = st.text_input(
    "Email"
)

password = st.text_input(
    "Password",
    type="password"
)


# =====================
# LOGIN
# =====================

if st.button("🔐 Login"):

    user = login(
        email,
        password
    )

    if user:

        st.session_state.logged_in = True
        st.session_state.user = user

        st.success(
            f"Welcome {user['username']}"
        )

        st.switch_page(
            "dashboard.py"
        )

    else:

        st.error(
            "Invalid Email or Password"
        )


# =====================
# BUTTONS
# =====================

c1, c2 = st.columns(2)

with c1:

    if st.button(
        "📝 Register"
    ):

        st.switch_page(
            "register.py"
        )

with c2:

    if st.button(
        "🏠 Home"
    ):

        st.switch_page(
            "home.py"
        )