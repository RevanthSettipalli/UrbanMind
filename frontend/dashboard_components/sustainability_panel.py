

import streamlit as st
import pandas as pd
import plotly.express as px


def render_sustainability_panel(rank_df=None):
    st.subheader("🌍 SDG Intelligence Layer")

    sdg_df = pd.DataFrame({
        "SDG": [
            "Clean Air",
            "Sustainable Cities",
            "Climate Action",
            "Innovation"
        ],
        "Score": [82, 79, 88, 84]
    })

    sdg_fig = px.bar(
        sdg_df,
        x="SDG",
        y="Score",
        color="Score",
        title="UN SDG Alignment"
    )

    st.plotly_chart(
        sdg_fig,
        width="stretch"
    )

    sdg_score = round(
        sdg_df["Score"].mean(),
        1
    )
    monitored_cities = len(rank_df) if rank_df is not None else 0

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🌱 SDG Alignment",
        f"{sdg_score}%"
    )

    c2.metric(
        "🏙 Cities Monitored",
        monitored_cities
    )

    c3.metric(
        "🌍 Climate Action",
        "88%"
    )

    st.success(
        "UrbanMind SDG Intelligence measures sustainability readiness, climate action performance and smart-city alignment."
    )

    return sdg_score