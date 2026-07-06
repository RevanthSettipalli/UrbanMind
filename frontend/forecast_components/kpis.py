import streamlit as st
from typing import Optional


def render_forecast_kpis(
    temperature: float,
    humidity: float,
    aqi: float,
    confidence: float,
    rain_probability: float,
    heatwave_probability: float,
    climate_risk: float,
    feels_like: Optional[float] = None,
):
    """Render executive KPI cards for the Forecast page."""

    if feels_like is None:
        feels_like = round(temperature + max(0, (humidity - 60) * 0.05), 1)

    k1, k2, k3, k4 = st.columns(4)
    k5, k6, k7, k8 = st.columns(4)

    k1.metric("🌡 Current", f"{temperature:.1f}°C")
    k2.metric("🥵 Feels Like", f"{feels_like:.1f}°C")
    k3.metric("💧 Humidity", f"{humidity:.1f}%")
    k4.metric("🌫 AQI", f"{aqi:.0f}")

    k5.metric("🌧 Rain", f"{rain_probability:.1f}%")
    k6.metric("🔥 Heatwave", f"{heatwave_probability:.1f}%")
    k7.metric("🎯 Confidence", f"{confidence:.1f}%")
    k8.metric("⚠ Climate Risk", f"{climate_risk:.1f}/100")

    if climate_risk >= 80:
        st.error("Executive Status: Extreme climate risk detected.")
    elif climate_risk >= 60:
        st.warning("Executive Status: Moderate climate risk. Increase monitoring.")
    else:
        st.success("Executive Status: Urban conditions remain stable.")