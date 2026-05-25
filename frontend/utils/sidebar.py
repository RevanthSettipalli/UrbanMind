import streamlit as st


def render_sidebar():

    st.markdown("""
<style>

.block-container{
padding-top:.15rem!important;
padding-left:2rem!important;
padding-right:2rem!important;
}

[data-testid="stSidebarNav"]{
display:none!important;
}

section[data-testid="stSidebar"]{
background:
linear-gradient(
180deg,
#031120,
#0a3168
);

width:300px!important;
}

[data-testid="stSidebarContent"]{
padding-top:0rem!important;
padding-left:20px;
padding-right:20px;
}

.sidebar-content{
margin-top:-78px;
}

.logo{
font-size:40px;
font-weight:900;
color:white;
margin-bottom:6px;
}

.sub{
color:#b8c7dc;
font-size:15px;
margin-bottom:26px;
}

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
}

.nav{

font-size:12px;

letter-spacing:4px;

color:#86a5cc;

font-weight:800;

margin-bottom:12px;
}

.stButton>button{

width:100%;

height:56px;

border:none;

border-radius:18px;

background:white;

color:#172033;

font-size:17px;

font-weight:700;

margin-bottom:10px;
}

.stButton>button:hover{

background:#edf4ff;

}

.logout .stButton>button{

background:
linear-gradient(
90deg,
#ef4444,
#dc2626
)!important;

color:white!important;

}

.footer{

padding-top:20px;

text-align:center;

font-size:12px;

color:#7f9bc0;

}

.footer2{

font-size:11px;

opacity:.55;

}

</style>
""",
unsafe_allow_html=True)

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
<br><br>
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
            ("📊 Dashboard", "dashboard"),
            ("📈 Analytics", "analytics"),
            ("🔮 Forecast", "forecast"),
            ("🌍 Geo", "geo"),
            ("🖥 Monitor", "monitor"),
            ("🤖 Assistant", "assistant"),
            ("📑 Reports", "reports"),
            ("⚙️ Settings", "settings"),
            ("ℹ️ About", "about")
        ]

        for title, page in pages:

            if st.button(
                title,
                use_container_width=True
            ):
                st.switch_page(f"frontend/pages/{page}.py")

        st.markdown(
'<div class="logout">',
unsafe_allow_html=True
)

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.session_state.pop("user", None)

            try:
                st.switch_page("frontend/pages/login.py")
            except Exception:
                st.rerun()

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
unsafe_allow_html=True)