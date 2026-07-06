

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_digital_twin(temperature: float,
                        humidity: float,
                        aqi: float):
    """Render the Digital Twin simulation panel."""

    st.subheader("🛰 Digital Twin Simulation Center")

    scenario = st.selectbox(
        "Simulation Scenario",
        ["Normal", "Heatwave", "Heavy Rain", "Cold Front", "High Pollution"],
        key="dt_scenario",
    )

    sim_temp = temperature
    sim_humidity = humidity
    sim_aqi = aqi

    if scenario == "Heatwave":
        sim_temp += 5
    elif scenario == "Heavy Rain":
        sim_temp -= 3
        sim_humidity += 20
    elif scenario == "Cold Front":
        sim_temp -= 7
    elif scenario == "High Pollution":
        sim_aqi += 80

    impact_score = max(0, round(100 - (abs(sim_temp - 30) * 1.5 + sim_aqi * 0.15), 1))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡 Sim Temp", f"{sim_temp:.1f}°C")
    c2.metric("💧 Sim Humidity", f"{sim_humidity:.1f}%")
    c3.metric("🌫 Sim AQI", f"{sim_aqi:.0f}")
    c4.metric("🏙 Urban Impact", f"{impact_score}/100")

    sim_df = pd.DataFrame({
        "Metric": ["Temperature", "Humidity", "AQI"],
        "Current": [temperature, humidity, aqi],
        "Simulated": [sim_temp, sim_humidity, sim_aqi],
    })

    fig = go.Figure()
    fig.add_bar(name="Current", x=sim_df["Metric"], y=sim_df["Current"])
    fig.add_bar(name="Simulated", x=sim_df["Metric"], y=sim_df["Simulated"])
    fig.update_layout(
        barmode="group",
        height=420,
        title="Digital Twin Scenario Comparison",
    )

    st.plotly_chart(fig, width="stretch")

    if impact_score >= 80:
        st.success("Digital Twin indicates stable urban conditions.")
    elif impact_score >= 60:
        st.warning("Moderate operational impact predicted. Increase monitoring.")
    else:
        st.error("High impact scenario detected. Prepare emergency response.")

    st.info(
        f"Scenario '{scenario}' projects an Urban Impact Score of {impact_score}/100 based on simulated environmental conditions."
    )