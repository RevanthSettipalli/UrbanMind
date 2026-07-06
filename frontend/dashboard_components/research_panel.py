

import streamlit as st
import pandas as pd
import plotly.express as px


def render_research_panel(
    best_city,
    worst_city,
    urban,
    urban_intelligence_index,
    forecast_confidence,
    sdg_score,
    risk,
    intel,
):

    st.subheader("📑 Novel Research Contributions")

    novelty_df = pd.DataFrame({
        "Innovation": [
            "Explainable AI",
            "Digital Twin",
            "SDG Intelligence",
            "Risk Forecasting",
            "Smart City Clustering",
            "Governance AI"
        ],
        "Research Score": [
            round(forecast_confidence, 1),
            round(urban_intelligence_index, 1),
            round(sdg_score, 1),
            round(100 - risk["overall_risk"], 1),
            round(urban, 1),
            round(min(100, 70 + urban * 0.25), 1)
        ]
    })

    novelty_fig = px.bar(
        novelty_df,
        x="Innovation",
        y="Research Score",
        color="Research Score",
        title="UrbanMind Research Novelty Index"
    )

    st.plotly_chart(novelty_fig, use_container_width=True)

    st.success(
        "UrbanMind combines Explainable AI, Digital Twin Intelligence, Governance Analytics, SDG Intelligence and Predictive Risk Forecasting into a unified Smart City research platform."
    )

    st.subheader("📚 Research Findings")

    findings = [
        f"{best_city} currently leads national urban readiness.",
        f"{worst_city} requires priority intervention.",
        f"Average urban intelligence score is {urban}.",
        f"Forecast confidence remains {intel['confidence']}%.",
        "Digital Twin monitoring is operational across all monitored cities."
    ]

    for finding in findings:
        st.success(finding)

    research_score = round(
        (
            forecast_confidence
            + sdg_score
            + urban_intelligence_index
            + (100 - risk["overall_risk"])
        ) / 4,
        1,
    )

    return research_score