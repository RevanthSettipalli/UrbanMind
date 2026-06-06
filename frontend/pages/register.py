import streamlit as st
import sys
import time

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

from backend.auth.auth import register


# =====================================
# PAGE
# =====================================

st.set_page_config(
    page_title="UrbanMind Register",
    page_icon="📝",
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

/* Card */

.register-card{

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

.footer{

text-align:center;

padding:30px;

opacity:.6;

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
# HEADER
# =====================================

st.markdown("""
<div class='register-card'>

<div class='title'>

📝 UrbanMind

</div>

<br>

<h1>

Create Account

</h1>

<div class='subtitle'>

Create your account to access Analytics • Forecast • Geo • Monitor

</div>

</div>
""",
unsafe_allow_html=True
)


st.write("")


# =====================================
# FORM
# =====================================

username = st.text_input(
    "Username",
    placeholder="Enter username"
)

email = st.text_input(
    "Email",
    placeholder="Enter email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Create password"
)


# =====================================
# REGISTER
# =====================================

if st.button(
    "🚀 Create Account",
    use_container_width=True
):

    username = username.strip()
    email = email.strip()
    password = password.strip()

    if not username or not email or not password:

        st.warning(
            "Please fill all fields"
        )

    else:

        try:

            created = register(
                username,
                email,
                password
            )

        except:

            created = False


        if created:

            st.success(
                "Account Created Successfully"
            )

            time.sleep(1)

            st.switch_page(
                "pages/login.py"
            )

        else:

            st.error(
                "Email already exists"
            )


# =====================================
# ACTIONS
# =====================================

st.write("")

st.divider()

left,right=st.columns(2)

with left:

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

        st.switch_page(
            "pages/login.py"
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