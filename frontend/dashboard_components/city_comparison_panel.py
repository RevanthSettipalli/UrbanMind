

import streamlit as st
import pandas as pd
import plotly.express as px


def render_city_comparison_panel(rank_df):

    st.subheader("⚖ City Comparison Engine")

    if rank_df is None or rank_df.empty:
        st.warning("No city comparison data available")
        return

    compare_cities = sorted(rank_df["city"].astype(str).unique())

    if len(compare_cities) < 2:
        st.info("At least two cities are required for comparison")
        return

    cmp1, cmp2 = st.columns(2)

    city_a = cmp1.selectbox(
        "City A",
        compare_cities,
        key="city_compare_a_component"
    )

    city_b = cmp2.selectbox(
        "City B",
        compare_cities,
        index=min(1, len(compare_cities) - 1),
        key="city_compare_b_component"
    )

    compare_df = rank_df[
        rank_df["city"].isin([city_a, city_b])
    ][[
        "city",
        "temperature",
        "humidity",
        "score"
    ]]

    st.dataframe(
        compare_df,
        width="stretch"
    )

    radar_df = pd.DataFrame({
        "Metric": ["Temperature", "Humidity", "Score"],
        city_a: [
            compare_df.iloc[0]["temperature"],
            compare_df.iloc[0]["humidity"],
            compare_df.iloc[0]["score"]
        ],
        city_b: [
            compare_df.iloc[1]["temperature"],
            compare_df.iloc[1]["humidity"],
            compare_df.iloc[1]["score"]
        ]
    }).melt(
        id_vars="Metric",
        var_name="City",
        value_name="Value"
    )

    compare_chart = px.line_polar(
        radar_df,
        r="Value",
        theta="Metric",
        color="City",
        line_close=True
    )

    st.plotly_chart(
        compare_chart,
        width="stretch"
    )

    winner = (
        city_a
        if float(compare_df.iloc[0]["score"])
        >= float(compare_df.iloc[1]["score"])
        else city_b
    )

    st.success(f"🏆 Comparison Winner: {winner}")