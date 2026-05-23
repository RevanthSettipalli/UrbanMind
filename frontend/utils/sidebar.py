import streamlit as st


def render_sidebar():

    current = st.session_state.get(
        "current_page",
        ""
    )

    st.markdown("""
<style>

/* MAIN */
.block-container{
padding-top:.15rem!important;
padding-left:2rem!important;
padding-right:2rem!important;
}


/* REMOVE STREAMLIT NAV */
[data-testid="stSidebarNav"]{
display:none!important;
}


/* SIDEBAR */

section[data-testid="stSidebar"]{

background:
linear-gradient(
180deg,
#031120,
#0a3168
);

width:300px!important;

}


/* CONTENT */

[data-testid="stSidebarContent"]{

padding-top:0rem!important;

padding-left:20px;

padding-right:20px;

}


/* MOVE TOP */

.sidebar-content{

margin-top:-78px;

}


/* LOGO */

.logo{

font-size:40px;

font-weight:900;

color:white;

line-height:1;

margin-bottom:4px;

}


/* SUB */

.sub{

color:#b8c7dc;

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

border-radius:24px;

color:white;

margin-bottom:28px;

line-height:2;

}


/* NAV */

.nav{

font-size:12px;

letter-spacing:4px;

color:#86a5cc;

font-weight:800;

margin-bottom:12px;

}


/* BUTTON */

.stButton>button{

width:100%;

height:54px;

border:none;

border-radius:18px;

background:white;

color:#172033;

font-size:17px;

font-weight:700;

margin-bottom:10px;

transition:.25s;

box-shadow:
0 10px 20px
rgba(
0,
0,
0,
0.08
);

}


/* HOVER */

.stButton>button:hover{

background:#edf4ff;

transform:
translateY(-2px);

}


/* LOGOUT */

.logout .stButton>button{

background:
linear-gradient(
90deg,
#ef4444,
#dc2626
)!important;

color:white!important;

}


/* FOOTER */

.footer{

padding-top:18px;

text-align:center;

font-size:12px;

color:#7f9bc0;

opacity:.8;

}

.footer2{

font-size:11px;

opacity:.55;

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
                "Admin"
            )

            if isinstance(
                user,
                dict
            )

            else "Admin"

        )

        st.markdown(
f"""
<div class='sidebar-content'>

<div class='logo'>

🌍 UrbanMind

</div>

<div class='sub'>

Smart City Intelligence

</div>

<div class='user'>

👤 <b>{username}</b>

<br>

🟢 Online

</div>

<div class='nav'>

NAVIGATION

</div>

</div>
""",
unsafe_allow_html=True
)

        pages = [

("📊 Dashboard","pages/dashboard.py"),

("📈 Analytics","pages/analytics.py"),

("🔮 Forecast","pages/forecast.py"),

("🌍 Geo","pages/geo.py"),

("🖥 Monitor","pages/monitor.py"),

("🤖 Assistant","pages/assistant.py"),

("⚙️ Settings","pages/settings.py"),

("ℹ️ About","pages/about.py")

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
'<div class="logout">',
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

        st.markdown("""
<div class='footer'>

UrbanMind v2.0

<div class='footer2'>

AI • Big Data • Smart Cities

</div>

</div>
""",
unsafe_allow_html=True
)