

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_forecast_charts(forecast_df: pd.DataFrame):
    """Render executive forecast visualizations."""

    st.subheader("📈 Forecast Analytics Center")

    required = {"hour", "temperature", "humidity"}
    if forecast_df.empty or not required.issubset(forecast_df.columns):
        st.warning("Forecast data unavailable for visualization.")
        return

    c1, c2 = st.columns(2)

    with c1:
        temp_fig = go.Figure()
        temp_fig.add_trace(
            go.Scatter(
                x=forecast_df["hour"],
                y=forecast_df["temperature"],
                mode="lines+markers",
                name="Temperature",
            )
        )
        temp_fig.update_layout(
            title="24-Hour Temperature Forecast",
            xaxis_title="Hour",
            yaxis_title="Temperature (°C)",
            height=420,
        )
        st.plotly_chart(temp_fig, width="stretch")

    with c2:
        hum_fig = go.Figure()
        hum_fig.add_trace(
            go.Scatter(
                x=forecast_df["hour"],
                y=forecast_df["humidity"],
                mode="lines+markers",
                name="Humidity",
            )
        )
        hum_fig.update_layout(
            title="24-Hour Humidity Forecast",
            xaxis_title="Hour",
            yaxis_title="Humidity (%)",
            height=420,
        )
        st.plotly_chart(hum_fig, width="stretch")

    st.subheader("📋 Forecast Data")
    st.dataframe(forecast_df, width="stretch")

    avg_temp = forecast_df["temperature"].mean()
    max_temp = forecast_df["temperature"].max()
    avg_humidity = forecast_df["humidity"].mean()

    k1, k2, k3 = st.columns(3)
    k1.metric("Average Temperature", f"{avg_temp:.1f}°C")
    k2.metric("Peak Temperature", f"{max_temp:.1f}°C")
    k3.metric("Average Humidity", f"{avg_humidity:.1f}%")

    st.info(
        f"Executive Insight: Average temperature is {avg_temp:.1f}°C with a peak of {max_temp:.1f}°C over the forecast horizon."
    )