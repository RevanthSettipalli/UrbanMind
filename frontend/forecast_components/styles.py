

import streamlit as st


def apply_forecast_styles():
    """Apply the shared UrbanMind Forecast theme."""

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0.8rem;
            padding-bottom: 2rem;
        }

        .forecast-hero {
            background: linear-gradient(135deg,#081c3d,#1565c0,#42a5f5);
            color: white;
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 14px 35px rgba(0,0,0,.18);
            margin-bottom: 22px;
        }

        .forecast-card {
            background: rgba(255,255,255,.97);
            border-radius: 20px;
            padding: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,.08);
            transition: all .25s ease;
        }

        .forecast-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0,0,0,.12);
        }

        .section-title {
            font-size: 28px;
            font-weight: 700;
            color: #124f9d;
            margin-bottom: 12px;
        }

        div[data-testid="stMetric"] {
            background: white;
            border-radius: 18px;
            padding: 12px;
            box-shadow: 0 6px 18px rgba(0,0,0,.06);
        }

        hr {
            margin-top: 24px;
            margin-bottom: 24px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )