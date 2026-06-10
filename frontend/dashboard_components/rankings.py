import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from backend.intelligence.urban_score import calculate_score


def render_rankings(
    df,
    ranking_df,
    prediction
):

    # ====================================
    # CITY RANKINGS
    # ====================================

    st.subheader("🏆 National City Performance Rankings")

    ranking_display = ranking_df.copy()

    # Round Score column to 1 decimal if present
    if "Score" in ranking_display.columns:
        ranking_display["Score"] = ranking_display["Score"].round(1)

    if len(ranking_display) >= 1:
        ranking_display.loc[ranking_display.index[0], "City"] = f"🥇 {ranking_display.iloc[0]['City']}"

    if len(ranking_display) >= 2:
        ranking_display.loc[ranking_display.index[1], "City"] = f"🥈 {ranking_display.iloc[1]['City']}"

    if len(ranking_display) >= 3:
        ranking_display.loc[ranking_display.index[2], "City"] = f"🥉 {ranking_display.iloc[2]['City']}"

    left_rank, right_rank = st.columns([2, 1])

    with left_rank:
        fig_rank = px.bar(
            ranking_df.head(10),
            x="City",
            y="Score",
            title="Top Urban Performance Rankings"
        )

        st.plotly_chart(
            fig_rank,
            use_container_width=True
        )

    with right_rank:
        st.dataframe(
            ranking_display,
            width='stretch',
            hide_index=True
        )

    # Dashboard is currently calling:
    # render_rankings(ranking_df, pollution_df)
    # so swap variables if the first dataframe is not the raw city dataframe.
    if "city" not in df.columns:
        st.info("Using precomputed ranking and pollution tables")
        return ranking_df, df

    best = ranking_df.iloc[0]
    worst = ranking_df.iloc[-1]
    score_col = "Score" if "Score" in ranking_df.columns else ranking_df.columns[-1]

    c1, c2 = st.columns(2)

    with c1:
        st.success(
            f"🥇 Best City: {best['City']} | Score: {best[score_col]}"
        )

    with c2:
        st.error(
            f"📉 Worst City: {worst['City']} | Score: {worst[score_col]}"
        )

    st.info(
        f"🏆 National Leader: {best['City']} | ⚠ Priority Intervention: {worst['City']}"
    )

    # ====================================
    # POLLUTION LEADERBOARD
    # ====================================

    st.subheader("🏭 Environmental Risk Intelligence")

    pollution_rows = []

    for city_name in df["city"].unique():

        city_df = df[df["city"] == city_name]

        row = city_df.tail(1).iloc[0]

        pollution_score = (
            float(row.get("aqi", 0)) * 15
            + float(row.get("pm25", 0)) * 0.20
            + float(row.get("pm10", 0)) * 0.08
            + float(row.get("co", 0)) * 0.01
            + float(row.get("no2", 0)) * 0.25
        )

        pollution_score = min(
            100,
            round(pollution_score, 2)
        )

        pollution_rows.append({
            "City": city_name,
            "Pollution Index": pollution_score
        })

    pollution_df = pd.DataFrame(
        pollution_rows
    )

    pollution_df = pollution_df.sort_values(
        "Pollution Index",
        ascending=False
    )

    pollution_display = pollution_df.copy()

    if len(pollution_display) >= 1:
        pollution_display.iloc[0, pollution_display.columns.get_loc("City")] = f"🥇 {pollution_display.iloc[0]['City']}"

    if len(pollution_display) >= 2:
        pollution_display.iloc[1, pollution_display.columns.get_loc("City")] = f"🥈 {pollution_display.iloc[1]['City']}"

    if len(pollution_display) >= 3:
        pollution_display.iloc[2, pollution_display.columns.get_loc("City")] = f"🥉 {pollution_display.iloc[2]['City']}"

    p_left, p_right = st.columns([2,1])

    with p_left:
        pollution_chart = px.bar(
            pollution_df,
            x="City",
            y="Pollution Index",
            title="Pollution Risk Ranking"
        )

        st.plotly_chart(
            pollution_chart,
            use_container_width=True
        )

    with p_right:
        st.dataframe(
            pollution_display,
            width='stretch',
            hide_index=True
        )

    most_polluted = pollution_df.iloc[0]
    least_polluted = pollution_df.iloc[-1]

    p1, p2 = st.columns(2)

    with p1:

        st.error(
            f"🚨 Most Polluted: {most_polluted['City']} ({most_polluted['Pollution Index']})"
        )

    with p2:

        st.success(
            f"🌿 Cleanest City: {least_polluted['City']} ({least_polluted['Pollution Index']})"
        )

    # ====================================
    # URBAN HEALTH INDEX
    # ====================================

    st.subheader(
        "💚 Urban Health Intelligence"
    )

    uhi_rows = []

    for city_name in df["city"].unique():

        city_df = (
            df[
                df["city"] == city_name
            ]
        )

        row = (
            city_df
            .tail(1)
            .iloc[0]
        )

        urban_score = calculate_score(
            float(row["temperature"]),
            float(row["humidity"]),
            prediction,
            float(row.get("aqi", 0)),
            float(row.get("pm25", 0)),
            float(row.get("pm10", 0)),
            float(row.get("co", 0)),
            float(row.get("no2", 0))
        )["score"]

        if urban_score >= 80:
            health_status = "Excellent"
        elif urban_score >= 60:
            health_status = "Good"
        elif urban_score >= 40:
            health_status = "Moderate"
        else:
            health_status = "Critical"

        uhi_rows.append({
            "City": city_name,
            "Urban Health Index": urban_score,
            "Status": health_status
        })

    uhi_df = pd.DataFrame(
        uhi_rows
    )

    uhi_df = uhi_df.sort_values(
        "Urban Health Index",
        ascending=False
    )

    uhi_display = uhi_df.copy()

    if len(uhi_display) >= 1:
        uhi_display.iloc[0, uhi_display.columns.get_loc("City")] = f"🥇 {uhi_display.iloc[0]['City']}"

    if len(uhi_display) >= 2:
        uhi_display.iloc[1, uhi_display.columns.get_loc("City")] = f"🥈 {uhi_display.iloc[1]['City']}"

    if len(uhi_display) >= 3:
        uhi_display.iloc[2, uhi_display.columns.get_loc("City")] = f"🥉 {uhi_display.iloc[2]['City']}"

    h_left, h_right = st.columns([2,1])

    with h_left:
        health_chart = px.bar(
            uhi_df,
            x="City",
            y="Urban Health Index",
            color="Urban Health Index",
            title="Urban Health Intelligence Ranking"
        )

        st.plotly_chart(
            health_chart,
            use_container_width=True
        )

    with h_right:
        st.dataframe(
            uhi_display,
            width='stretch',
            hide_index=True
        )

    best_health = uhi_df.iloc[0]
    worst_health = uhi_df.iloc[-1]

    h1, h2 = st.columns(2)

    with h1:

        st.success(
            f"💚 Healthiest City: {best_health['City']} ({best_health['Urban Health Index']})"
        )

    with h2:

        st.error(
            f"❤️‍🩹 Least Healthy City: {worst_health['City']} ({worst_health['Urban Health Index']})"
        )

    # Urban Health bar chart section removed

    st.markdown("### 📊 National Ranking Intelligence")

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric(
        "🏆 Best Urban Score",
        round(float(best_health['Urban Health Index']), 1)
    )

    summary2.metric(
        "🌿 Cleanest City",
        least_polluted['City']
    )

    summary3.metric(
        "⚠ Highest Risk City",
        most_polluted['City']
    )

    return pollution_df, uhi_df