import streamlit as st
import pandas as pd

from backend.intelligence.urban_score import calculate_score
from backend.intelligence.risk_engine import calculate_risk
from backend.intelligence.forecast_ai import forecast_city
from backend.intelligence.predictive_analytics import predictive_report


def render_copilot(df, prediction):

    st.subheader("🤖 Urban AI Copilot")

    copilot_city = st.selectbox(
        "Select City for AI Analysis",
        sorted(df["city"].unique()),
        key="urban_ai_copilot"
    )

    copilot_row = (
        df[df["city"] == copilot_city]
        .tail(1)
        .iloc[0]
    )

    copilot_score = calculate_score(
        float(copilot_row["temperature"]),
        float(copilot_row["humidity"]),
        prediction,
        float(copilot_row.get("aqi", 0)),
        float(copilot_row.get("pm25", 0)),
        float(copilot_row.get("pm10", 0)),
        float(copilot_row.get("co", 0)),
        float(copilot_row.get("no2", 0))
    )["score"]

    copilot_risk = calculate_risk(
        float(copilot_row["temperature"]),
        float(copilot_row["humidity"]),
        float(copilot_row.get("aqi", 0)),
        float(copilot_row.get("pm25", 0)),
        float(copilot_row.get("pm10", 0)),
        float(copilot_row.get("co", 0)),
        float(copilot_row.get("no2", 0)),
        copilot_score
    )

    copilot_forecast = forecast_city(
        float(copilot_row["temperature"]),
        float(copilot_row["humidity"]),
        float(copilot_row.get("aqi", 0))
    )

    copilot_prediction = predictive_report(
        copilot_score,
        float(copilot_row.get("aqi", 0))
    )

    cp1, cp2, cp3, cp4 = st.columns(4)

    cp1.metric("🏙 Urban Score", copilot_score)
    cp2.metric("🌫 AQI", round(float(copilot_row.get("aqi", 0)), 2))
    cp3.metric("🔥 Risk", copilot_risk["urban_risk"])
    cp4.metric(
        "🔮 Forecast Score",
        copilot_prediction["urban_score_forecast"]
    )

    st.markdown("### 🧠 AI Executive Summary")

    copilot_summary = f"""
City: {copilot_city}

Urban Score: {copilot_score}

Risk Level: {copilot_risk['urban_risk']}

Next Day Temperature Forecast: {copilot_forecast['next_day_temp']}°C

Forecast AQI: {copilot_prediction['aqi_forecast']}

Recommendation: Focus on environmental monitoring, sustainability programs, and risk mitigation strategies.
"""

    st.info(copilot_summary)

    copilot_df = pd.DataFrame([
        {"Metric": "Urban Score", "Value": copilot_score},
        {"Metric": "Urban Risk", "Value": copilot_risk["urban_risk"]},
        {"Metric": "Forecast Score", "Value": copilot_prediction["urban_score_forecast"]},
        {"Metric": "Forecast AQI", "Value": copilot_prediction["aqi_forecast"]}
    ])

    st.dataframe(
        copilot_df,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        f"Urban AI Copilot recommends prioritizing strategic improvements in {copilot_city} based on current intelligence, predictive analytics, and forecast models."
    )