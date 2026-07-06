

import streamlit as st
import pandas as pd
import plotly.express as px


def render_risk_panel(predictive_data):
    try:
        risk = predictive_data["risk_intelligence"]
        st.subheader("🏙 Urban Risk Intelligence")

        c1, c2, c3 = st.columns(3)

        c1.metric("Highest Risk", max(
            risk["infrastructure_risk"],
            risk["pollution_risk"],
            risk["traffic_risk"],
            risk["weather_risk"]
        ))

        c2.metric("Overall Risk", risk["overall_risk"])

        c3.metric(
            "Risk Status",
            "HIGH" if risk["overall_risk"] >= 70 else "MODERATE" if risk["overall_risk"] >= 40 else "LOW"
        )

        r1, r2, r3, r4, r5 = st.columns(5)

        r1.metric("Infrastructure", risk["infrastructure_risk"])
        r2.metric("Pollution", risk["pollution_risk"])
        r3.metric("Traffic", risk["traffic_risk"])
        r4.metric("Weather", risk["weather_risk"])
        r5.metric("Overall", risk["overall_risk"])

        st.subheader("📡 Urban Risk Distribution")

        st.success(
            "Urban Risk Monitoring Active • AI Risk Intelligence Operational"
        )

        risk_chart_df = pd.DataFrame({
            "Risk": [
                "Infrastructure",
                "Pollution",
                "Traffic",
                "Weather"
            ],
            "Value": [
                risk["infrastructure_risk"],
                risk["pollution_risk"],
                risk["traffic_risk"],
                risk["weather_risk"]
            ]
        })

        risk_fig = px.line_polar(
            risk_chart_df,
            r="Value",
            theta="Risk",
            line_close=True
        )

        st.plotly_chart(
            risk_fig,
            use_container_width=True
        )

        st.download_button(
            "📥 Export Risk Data",
            risk_chart_df.to_csv(index=False),
            "urban_risk_data.csv",
            "text/csv"
        )
    except Exception as e:
        st.error(f"Risk Panel Error: {e}")