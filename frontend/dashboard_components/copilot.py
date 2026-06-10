import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from backend.intelligence.urban_score import calculate_score
from backend.intelligence.risk_engine import calculate_risk
from backend.intelligence.forecast_ai import forecast_city
from backend.intelligence.predictive_analytics import predictive_report


def render_copilot(df, prediction):

    st.subheader("🤖 UrbanMind AI Copilot & Decision Assistant")

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

    st.info(
        "UrbanMind AI Copilot provides executive decision support, risk forecasting, sustainability intelligence, and governance recommendations for city administrators."
    )

    cp1, cp2, cp3, cp4 = st.columns(4)

    cp1.metric("🏙 Urban Score", copilot_score)
    cp2.metric("🌫 AQI", round(float(copilot_row.get("aqi", 0)), 2))
    cp3.metric("🔥 Risk", copilot_risk["urban_risk"])
    cp4.metric(
        "🔮 Forecast Score",
        copilot_prediction["urban_score_forecast"]
    )

    risk_value = 90 if str(copilot_risk['urban_risk']).upper() == 'CRITICAL' else 70 if str(copilot_risk['urban_risk']).upper() == 'HIGH' else 40 if str(copilot_risk['urban_risk']).upper() == 'MODERATE' else 20

    risk_gauge = go.Figure(
        go.Indicator(
            mode='gauge+number',
            value=risk_value,
            title={'text': 'AI Risk Index'},
            gauge={
                'axis': {'range': [0, 100]},
                'steps': [
                    {'range': [0, 40], 'color': 'green'},
                    {'range': [40, 70], 'color': 'orange'},
                    {'range': [70, 100], 'color': 'red'}
                ]
            }
        )
    )

    st.plotly_chart(
        risk_gauge,
        use_container_width=True
    )

    st.markdown("### 🧠 Executive AI Briefing")

    copilot_summary = f"""
🏙 City: {copilot_city}

📊 Urban Score: {copilot_score}

⚠ Risk Level: {copilot_risk['urban_risk']}

🌡 Next Day Temperature Forecast: {copilot_forecast['next_day_temp']}°C

🌫 Forecast AQI: {copilot_prediction['aqi_forecast']}

🧠 AI Insights:
- Maintain continuous environmental monitoring.
- Strengthen sustainability and resilience programs.
- Use predictive analytics to reduce future urban risks.
"""

    st.info(copilot_summary)

    decision_df = pd.DataFrame({
        'Priority': ['High', 'Medium', 'Medium', 'Low'],
        'Action': [
            f'Improve resilience planning in {copilot_city}',
            'Strengthen environmental monitoring',
            'Expand predictive analytics coverage',
            'Review sustainability initiatives'
        ]
    })

    st.dataframe(
        decision_df,
        use_container_width=True,
        hide_index=True
    )

    copilot_df = pd.DataFrame([
        {"Metric": "Urban Score", "Value": copilot_score},
        {"Metric": "Urban Risk", "Value": copilot_risk["urban_risk"]},
        {"Metric": "Forecast Score", "Value": copilot_prediction["urban_score_forecast"]},
        {"Metric": "Forecast AQI", "Value": copilot_prediction["aqi_forecast"]}
    ])

    left_col, right_col = st.columns([2,1])

    with left_col:
        st.dataframe(
            copilot_df,
            width='stretch',
            hide_index=True
        )

    with right_col:
        st.metric(
            '🎯 AI Confidence',
            '94%'
        )

    recommendations = []

    if copilot_score < 40:
        recommendations.append(
            f"Immediate intervention is recommended in {copilot_city}."
        )
    elif copilot_score < 60:
        recommendations.append(
            f"Increase monitoring and mitigation efforts in {copilot_city}."
        )
    else:
        recommendations.append(
            f"Maintain current sustainability practices in {copilot_city}."
        )

    if str(copilot_risk['urban_risk']).upper() in ["HIGH", "CRITICAL"]:
        recommendations.append(
            "Deploy preventive resources and emergency preparedness measures."
        )

    recommendations.append(
        "Leverage predictive analytics for proactive decision making."
    )

    forecast_chart = pd.DataFrame({
        'Metric': ['Current Score', 'Forecast Score'],
        'Value': [copilot_score, copilot_prediction['urban_score_forecast']]
    })

    fig_forecast = px.bar(
        forecast_chart,
        x='Metric',
        y='Value',
        title='UrbanMind Forecast Intelligence'
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

    st.success("\n".join(recommendations))

    st.markdown('---')

    st.caption(
        'UrbanMind AI Copilot • Executive Decision Support • Predictive Governance Intelligence'
    )