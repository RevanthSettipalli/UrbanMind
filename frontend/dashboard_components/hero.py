import streamlit as st
from datetime import datetime


def render_hero(current_time=None):
    if current_time is None:
        current_time = datetime.now().strftime('%I:%M:%S %p')

    left, right = st.columns([5, 1])

    with left:
        st.markdown("""
        <div style='
        background:linear-gradient(135deg,#001428,#003d73,#0d5c9e);
        padding:28px;
        border-radius:24px;
        color:white;
        box-shadow:0px 10px 25px rgba(0,0,0,0.18);'>

        <div style='font-size:12px;font-weight:700;letter-spacing:2px;opacity:0.85;'>
        AI-POWERED SMART CITY INTELLIGENCE PLATFORM
        </div>

        <div style='font-size:48px;font-weight:900;margin-top:10px;'>
        🌍 UrbanMind
        </div>

        <div style='font-size:24px;font-weight:600;margin-top:4px;'>
        National Urban Command Center
        </div>

        <div style='font-size:14px;opacity:0.9;margin-top:10px;'>
        Research-Grade Smart City Intelligence, Governance AI & Predictive Analytics Platform
        </div>

        <div style='margin-top:16px;font-size:15px;'>
        Real-Time Monitoring • Predictive Analytics • Governance AI • Digital Twin Intelligence
        </div>

        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📡 Live Data", "ACTIVE")
        c2.metric("🤖 AI Engine", "ONLINE")
        c3.metric("🏙 Cities", "10+")
        c4.metric("🔮 Forecast", "READY")

    with right:
        st.components.v1.html(f"""
        <div style='background:white;height:220px;border-radius:20px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;box-shadow:0px 6px 18px rgba(0,0,0,0.12);'>
            <div style='font-size:42px;'>🕒</div>
            <div style='font-size:28px;font-weight:900;color:#0d5c9e;'>{current_time}</div>
            <div style='font-size:13px;color:#666;margin-top:6px;'>India Standard Time</div>
            <div style='font-size:12px;color:#28a745;font-weight:700;margin-top:10px;'>● SYSTEM ONLINE</div>
            <div style='font-size:11px;color:#666;margin-top:4px;'>National Operations Center</div>
        </div>
        """, height=220)

    st.info(
        "UrbanMind Research Contributions: Urban Readiness Scoring • Governance AI • Predictive Risk Analytics • Digital Twin Intelligence • National Decision Support"
    )