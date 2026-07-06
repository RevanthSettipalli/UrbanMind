

import streamlit as st
from datetime import datetime
import pytz


def render_forecast_hero(selected_city: str, last_updated: str, confidence: float = 95.0):
    """Render the executive Forecast hero section."""

    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    current_time = now.strftime("%I:%M:%S %p")

    st.markdown(
        """
        <style>
        .forecast-hero {
            background: linear-gradient(135deg,#0b1f4d,#1565c0,#42a5f5);
            border-radius:24px;
            padding:28px;
            color:white;
            margin-bottom:20px;
            box-shadow:0 12px 30px rgba(0,0,0,.18);
        }
        .forecast-title {
            font-size:40px;
            font-weight:800;
            margin-bottom:6px;
        }
        .forecast-subtitle {
            font-size:17px;
            opacity:.95;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([3, 1])

    with left:
        st.markdown(
            f"""
            <div class='forecast-hero'>
                <div class='forecast-title'>🔮 Forecast Intelligence Center</div>
                <div class='forecast-subtitle'>AI-Powered Urban Weather Prediction & Decision Support</div>
                <br>
                <b>Selected City:</b> {selected_city}<br>
                <b>Last Updated:</b> {last_updated}<br>
                <b>AI Confidence:</b> {confidence:.1f}%
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.metric("🕒 IST Time", current_time)
        st.metric("🤖 AI Status", "ONLINE")
        st.metric("📡 Engine", "ACTIVE")