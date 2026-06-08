import streamlit as st


def render_hero(current_time=None):
    left, right = st.columns([6, 1])

    with left:
        st.markdown(
            """
            <div style="
            background: linear-gradient(90deg,#001f3f,#0d5c9e);
            padding:40px;
            border-radius:30px;
            color:white;
            min-height:180px;
            display:flex;
            flex-direction:column;
            justify-content:center;">
                <h1 style="font-size:64px;margin:0;">📊 Urban Analytics</h1>
                <p style="font-size:28px;margin-top:10px;">
                Advanced Intelligence • Ranking • Geo Analysis
                </p>
                </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.components.v1.html(
            """
            <div style="
            background:#dfe8f5;
            height:260px;
            border-radius:22px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            text-align:center;
            padding:18px;">
                <div style="font-size:44px;">🕒</div>
                <div id="urbanmind-clock" style="font-size:28px;font-weight:800;color:#124f9d;"></div>
                <div style="font-size:15px;color:#5a6572;">Live Time</div>
                </div>
            <script>
            function updateClock(){
                const now = new Date();
                const time = now.toLocaleTimeString('en-IN', {
                    hour:'2-digit',
                    minute:'2-digit',
                    second:'2-digit',
                    hour12:true
                });
                document.getElementById('urbanmind-clock').innerHTML = time;
            }
            updateClock();
            setInterval(updateClock,1000);
            </script>
            """,
            height=260,
        )