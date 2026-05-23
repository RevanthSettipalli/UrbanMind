import streamlit as st


def render_sidebar():

    st.markdown("""
<style>

/* MAIN PAGE */
.block-container{
padding-top:0.4rem !important;
}


/* REMOVE DEFAULT NAV */
[data-testid="stSidebarNav"]{
display:none;
}


/* SIDEBAR */

section[data-testid="stSidebar"]{

background:
linear-gradient(
180deg,
#021122,
#082d61
);

padding-top:0rem !important;

width:300px !important;

}


/* SIDEBAR CONTENT */

[data-testid="stSidebarContent"]{

padding-top:0rem !important;

padding-left:18px;

padding-right:18px;

}


/* MOVE HEADER UP */

.sidebar-content{

margin-top:-45px;

}


/* BRAND */

.logo{

font-size:34px;

font-weight:800;

color:white;

margin-bottom:2px;

line-height:1;

}


.sub{

color:#9cb5d6;

font-size:15px;

margin-bottom:28px;

}


/* USER */

.user{

background:
rgba(
255,
255,
255,
0.08
);

padding:22px;

border-radius:20px;

margin-bottom:30px;

color:white;

line-height:2;

}


/* NAV */

.nav{

color:#8ea6c8;

font-size:12px;

font-weight:700;

letter-spacing:3px;

margin-bottom:10px;

}


/* BUTTONS */

.stButton button{

width:100%;

height:58px;

border-radius:18px;

background:white;

color:#172033;

font-size:18px;

font-weight:700;

border:none;

margin-bottom:12px;

transition:0.2s;

}


.stButton button:hover{

background:#eef5ff;

transform:translateY(-2px);

}


/* LOGOUT */

.logout button{

background:#ef4444 !important;

color:white !important;

}


/* FOOTER */

.footer{

color:#7e9bc2;

text-align:center;

padding-top:18px;

font-size:12px;

opacity:0.7;

}

</style>
""",
unsafe_allow_html=True
)

    with st.sidebar:

        user = st.session_state.get(
            "user",
            {}
        )

        username = (
            user.get(
                "username",
                "admin"
            )
            if isinstance(
                user,
                dict
            )
            else "admin"
        )

        st.markdown(
"""
<div class="sidebar-content">

<div class="logo">
🌍 UrbanMind
</div>

<div class="sub">
Smart City Intelligence
</div>

</div>
""",
unsafe_allow_html=True
)

        st.markdown(
f"""
<div class="user">

👤 <b>{username}</b>

<br>

🟢 Online

</div>
""",
unsafe_allow_html=True
)

        st.markdown(
"""
<div class="nav">

NAVIGATION

</div>
""",
unsafe_allow_html=True
)

        pages = [

("📊 Dashboard","pages/dashboard.py"),

("📈 Analytics","pages/analytics.py"),

("🔮 Forecast","pages/forecast.py"),

("🌍 Geo","pages/geo.py"),

("🖥 Monitor","pages/monitor.py")

]

        for title,page in pages:

            if st.button(
                title,
                use_container_width=True
            ):

                st.switch_page(
                    page
                )

        st.markdown(
"<div class='logout'>",
unsafe_allow_html=True
)

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.clear()

            st.switch_page(
                "pages/login.py"
            )

        st.markdown(
"</div>",
unsafe_allow_html=True
)

        st.markdown(
"""
<div class="footer">

UrbanMind v1.0

</div>
""",
unsafe_allow_html=True
)