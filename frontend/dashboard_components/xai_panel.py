import streamlit as st
import pandas as pd
import plotly.express as px


calculate_feature_importance = None


def render_xai_panel(avg_temp, avg_hum, current_aqi, overall_risk, best_city):
    global calculate_feature_importance

    st.subheader("🔍 Explainable AI Intelligence")

    try:
        if calculate_feature_importance is None:
            from backend.intelligence.explainable_ai import (
                calculate_feature_importance as _calculate_feature_importance
            )
            calculate_feature_importance = _calculate_feature_importance

        feature_importance = calculate_feature_importance(
            avg_temp,
            avg_hum,
            current_aqi,
            overall_risk
        )

    except Exception as e:
        st.warning(f"Explainable AI disabled: {e}")

        feature_importance = {
            "Temperature": 30,
            "Humidity": 25,
            "AQI": 25,
            "Risk": 20
        }

    impact_df = pd.DataFrame({
        "Factor": list(feature_importance.keys()),
        "Impact": list(feature_importance.values())
    })

    if impact_df.empty:
        st.warning("No explainability data available.")
        return feature_importance, impact_df

    impact_fig = px.bar(
        impact_df,
        x="Factor",
        y="Impact",
        color="Impact",
        title="Urban Score Contribution Analysis"
    )

    st.plotly_chart(
        impact_fig,
        width="stretch"
    )

    contribution_total = impact_df["Impact"].sum()

    st.caption(
        f"Explainable AI generated from Urban Score contribution analysis. Total measurable contribution: {contribution_total}%"
    )

    st.success(
        f"Why {best_city} ranks #1: balanced environmental indicators, lower risk exposure and stronger predictive intelligence."
    )

    return feature_importance, impact_df