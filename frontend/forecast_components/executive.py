

import streamlit as st


def render_executive_panel(
    city: str,
    confidence: float,
    climate_risk: float,
    readiness_index: float,
    forecast_temp: float,
    heatwave_probability: float,
    rain_probability: float,
):
    """Render the executive decision-support section."""

    st.subheader("🏛 Executive Decision Center")

    e1, e2, e3, e4 = st.columns(4)
    e1.metric("🎯 AI Confidence", f"{confidence:.1f}%")
    e2.metric("🌍 Climate Risk", f"{climate_risk:.1f}/100")
    e3.metric("🛡 Readiness", f"{readiness_index:.1f}/100")
    e4.metric("🌡 Forecast", f"{forecast_temp:.1f}°C")

    if climate_risk >= 80:
        level = "Critical"
        recommendation = (
            "Activate emergency response, increase cooling infrastructure, "
            "and issue public safety advisories."
        )
        st.error(f"🚨 Executive Alert: {recommendation}")
    elif climate_risk >= 60:
        level = "Moderate"
        recommendation = (
            "Increase monitoring, prepare emergency teams, and monitor AQI."
        )
        st.warning(f"⚠ Executive Advisory: {recommendation}")
    else:
        level = "Low"
        recommendation = (
            "Urban conditions are stable. Continue routine monitoring."
        )
        st.success(f"✅ Executive Status: {recommendation}")

    st.markdown("### 📋 Executive Summary")
    st.info(
        f"""
**City:** {city}

**Forecast Temperature:** {forecast_temp:.1f}°C

**Heatwave Probability:** {heatwave_probability:.1f}%

**Rainfall Probability:** {rain_probability:.1f}%

**Overall Risk Level:** {level}

**Recommendation:** {recommendation}
"""
    )

    st.markdown("### 🎯 Strategic Priorities")
    p1, p2, p3 = st.columns(3)
    p1.success("✅ Maintain real-time monitoring")
    p2.info("📡 Review forecast updates every refresh cycle")
    p3.warning("🏙 Coordinate city response teams if risk increases")

    st.caption(
        "UrbanMind Executive Intelligence • AI Forecasting • Climate Analytics • Digital Twin"
    )