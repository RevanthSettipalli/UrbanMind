

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_climate_panel(temperature: float,
                         humidity: float,
                         aqi: float,
                         rain_probability: float,
                         heatwave_probability: float):
    """Render the Climate Intelligence section for Forecast."""

    climate_risk = min(
        100,
        round(
            (temperature * 1.4)
            + (aqi * 0.20)
            + (heatwave_probability * 0.25),
            1,
        ),
    )

    st.subheader("🌍 Climate Intelligence Center")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡 Temperature", f"{temperature:.1f}°C")
    c2.metric("💧 Humidity", f"{humidity:.1f}%")
    c3.metric("🌫 AQI", f"{aqi:.0f}")
    c4.metric("⚠ Climate Risk", f"{climate_risk}/100")

    radar_df = pd.DataFrame({
        "Category": [
            "Temperature",
            "Humidity",
            "AQI",
            "Rain",
            "Heatwave",
        ],
        "Value": [
            temperature,
            humidity,
            aqi,
            rain_probability,
            heatwave_probability,
        ],
    })

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=radar_df["Value"],
            theta=radar_df["Category"],
            fill="toself",
            name="Climate Profile",
        )
    )

    fig.update_layout(
        polar={"radialaxis": {"visible": True}},
        height=500,
        title="Climate Intelligence Radar",
    )

    st.plotly_chart(fig, width="stretch")

    if climate_risk >= 80:
        st.error("Extreme climate risk detected. Emergency preparedness is recommended.")
    elif climate_risk >= 60:
        st.warning("Moderate climate risk. Increase monitoring and readiness.")
    else:
        st.success("Climate conditions are stable. No immediate action required.")

    st.info(
        f"UrbanMind AI estimates a climate risk score of {climate_risk}/100 based on current weather, air quality, rainfall probability, and heatwave indicators."
    )