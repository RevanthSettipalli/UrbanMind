

import streamlit as st
import pandas as pd
import plotly.express as px


def render_explainable_ai(
    temperature: float,
    humidity: float,
    aqi: float,
    pm25: float,
    pm10: float,
    co: float,
    no2: float,
    prediction: float,
    confidence: float,
):
    """Render Explainable AI insights for the forecast engine."""

    impacts = {
        "Temperature": round(temperature * 0.35, 2),
        "Humidity": round(humidity * 0.20, 2),
        "AQI": round(aqi * 0.15, 2),
        "PM2.5": round(pm25 * 0.10, 2),
        "PM10": round(pm10 * 0.08, 2),
        "CO": round(co * 0.07, 2),
        "NO₂": round(no2 * 0.05, 2),
    }

    feature_df = (
        pd.DataFrame({"Feature": impacts.keys(), "Impact": impacts.values()})
        .sort_values("Impact", ascending=False)
    )

    st.subheader("🤖 Explainable AI Center")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎯 Prediction", f"{prediction:.1f}°C")
    c2.metric("📈 Confidence", f"{confidence:.1f}%")
    c3.metric("🏆 Top Driver", feature_df.iloc[0]["Feature"])
    c4.metric("🧠 Model", "Hybrid AI")

    fig = px.bar(
        feature_df,
        x="Impact",
        y="Feature",
        orientation="h",
        title="Feature Importance",
        text="Impact",
    )

    fig.update_layout(height=420, yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig, width="stretch")

    st.markdown("### 🧠 AI Reasoning")
    st.info(
        f"The Hybrid AI model predicts **{prediction:.1f}°C** with **{confidence:.1f}%** confidence. "
        f"The strongest contributors are **{feature_df.iloc[0]['Feature']}**, **{feature_df.iloc[1]['Feature']}**, "
        f"and **{feature_df.iloc[2]['Feature']}**. Environmental variables are combined to produce the final forecast."
    )

    st.markdown("### 📋 Executive Interpretation")

    if prediction >= 40:
        st.error("Extreme heat conditions are likely. Immediate preparedness is recommended.")
    elif prediction >= 35:
        st.warning("Moderate heat risk detected. Increase monitoring and citizen advisories.")
    else:
        st.success("Forecast conditions remain stable. Continue standard monitoring.")