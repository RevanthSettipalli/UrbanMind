import streamlit as st
import time
import sys

from pathlib import Path


# =====================================
# ROOT
# =====================================

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# =====================================
# IMPORT
# =====================================

from backend.auth.auth import login


# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="UrbanMind Login",
    page_icon="🌍",
    layout="wide"
)


# =====================================
# HIDE SIDEBAR
# =====================================

st.markdown("""
<style>

[data-testid="stSidebar"]{
display:none;
}

[data-testid="collapsedControl"]{
display:none;
}

[data-testid="stSidebarNav"]{
display:none;
}

.block-container{

max-width:760px;

padding-top:2rem;

}

/* Login Card */

.login-card{

padding:55px;

border-radius:30px;

background:

linear-gradient(
180deg,
rgba(255,255,255,.95),
rgba(248,250,252,.95)
);

box-shadow:

0 20px 60px rgba(0,0,0,.12);

}

/* Header */

.title{

font-size:68px;

font-weight:800;

}

.subtitle{

font-size:22px;

opacity:.75;

}

/* Footer */

.footer{

text-align:center;

opacity:.6;

padding:30px;

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

if "user" not in st.session_state:
    st.session_state.user = None


# =====================================
# REDIRECT
# =====================================

if st.session_state.logged_in:

    st.switch_page(
        "pages/dashboard.py"
    )


# =====================================
# UI
# =====================================

st.markdown("""
<div class='login-card'>
<div class='title'>
🌍 UrbanMind
</div>

<br>

<h1>
Smart City Intelligence Platform
</h1>

<div class='subtitle'>

Secure access to Analytics • Forecast • Geo • Monitor

</div>

</div>
""",
unsafe_allow_html=True
)


st.write("")


# =====================================
# FORM
# =====================================

email = st.text_input(
    "Email",
    placeholder="Enter email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter password"
)


# =====================================
# LOGIN
# =====================================

if st.button(
    "🔐 Login",
    use_container_width=True
):

    email = email.strip()
    password = password.strip()

    if not email or not password:

        st.warning(
            "Please fill all fields"
        )

    else:

        try:

            user = login(
                email,
                password
            )

        except:

            user = None


        if user:

            st.session_state.logged_in = True
            st.session_state.user = user

            username = (

                user.get(
                    "username",
                    "User"
                )

                if isinstance(
                    user,
                    dict
                )

                else "User"

            )

            st.success(
                f"Welcome {username}"
            )

            time.sleep(1)

            st.switch_page(
                "pages/dashboard.py"
            )

        else:

            st.error(
                "Invalid Email or Password"
            )


# =====================================
# ACTIONS
# =====================================

st.write("")
st.divider()

left,right=st.columns(2)

with left:

    if st.button(
        "📝 Register",
        use_container_width=True
    ):

        st.switch_page(
            "pages/register.py"
        )


with right:

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):

        st.switch_page(
            "home.py"
        )


# =====================================
# FOOTER
# =====================================

st.markdown("""
<div class='footer'>

UrbanMind • AI • Big Data • Digital Twin • Smart Cities

<br><br>

Built for Research • Industry

</div>
""",
unsafe_allow_html=True
)