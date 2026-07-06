

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_ai_engine(rf_prediction: float,
                     lstm_prediction: float,
                     prophet_prediction: float,
                     confidence: float,
                     accuracy: float = 94.0,
                     mae: float = 1.2,
                     rmse: float = 1.8):
    """Render the AI Forecast Engine section."""

    hybrid_prediction = round(
        (rf_prediction + lstm_prediction + prophet_prediction) / 3,
        1,
    )

    st.subheader("🧠 AI Forecast Engine")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌲 Random Forest", f"{rf_prediction:.1f}°C")
    c2.metric("🧠 LSTM", f"{lstm_prediction:.1f}°C")
    c3.metric("📈 Prophet", f"{prophet_prediction:.1f}°C")
    c4.metric("🤝 Hybrid AI", f"{hybrid_prediction:.1f}°C")

    m1, m2, m3 = st.columns(3)
    m1.metric("🎯 Confidence", f"{confidence:.1f}%")
    m2.metric("✅ Accuracy", f"{accuracy:.1f}%")
    m3.metric("📉 RMSE", f"{rmse:.2f}")

    comparison = pd.DataFrame({
        "Model": ["Random Forest", "LSTM", "Prophet", "Hybrid"],
        "Prediction": [
            rf_prediction,
            lstm_prediction,
            prophet_prediction,
            hybrid_prediction,
        ],
    })

    fig = go.Figure()
    fig.add_bar(
        x=comparison["Model"],
        y=comparison["Prediction"],
        text=comparison["Prediction"],
        textposition="outside",
    )
    fig.update_layout(
        title="AI Model Comparison",
        height=420,
        xaxis_title="Forecast Model",
        yaxis_title="Predicted Temperature (°C)",
    )

    st.plotly_chart(fig, width="stretch")

    st.info(
        f"Hybrid AI consensus predicts **{hybrid_prediction:.1f}°C** with **{confidence:.1f}%** confidence. "
        f"Model quality: Accuracy {accuracy:.1f}%, MAE {mae:.2f}, RMSE {rmse:.2f}."
    )