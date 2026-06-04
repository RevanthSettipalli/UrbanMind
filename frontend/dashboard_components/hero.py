import streamlit as st


def render_hero(current_time):

    left, right = st.columns([8, 1.5])

    with left:

        st.markdown(
            """
<div style="
padding:55px;
height:260px;
border-radius:30px;
background:linear-gradient(135deg,#021224,#0d5a8a);
color:white;
display:flex;
flex-direction:column;
justify-content:center;
">

<div style="
font-size:72px;
font-weight:900;
">
🌍 Urban Dashboard
</div>

<div style="
font-size:24px;
margin-top:15px;
">
Advanced Intelligence • Ranking • Geo Analysis
</div>

</div>
""",
            unsafe_allow_html=True
        )

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
">

<div style="
font-size:44px;
">
🕒
</div>

<div style="
font-size:28px;
font-weight:800;
color:#124f9d;
">
{current_time}
</div>

<div style="
font-size:15px;
color:#5a6572;
">
Live Time
</div>

</div>
""",
            unsafe_allow_html=True
        )