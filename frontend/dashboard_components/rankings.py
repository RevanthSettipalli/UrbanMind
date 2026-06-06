import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from backend.intelligence.urban_score import calculate_score


def render_rankings(
    df,
    ranking_df,
    prediction
):


    # ====================================
    # CITY RANKINGS
    # ====================================

    st.subheader("🏆 City Rankings")

    st.dataframe(
        ranking_df,
        use_container_width=True,
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
            f"🏆 Best City: {best['City']} ({best[score_col]})"
        )

    with c2:
        st.error(
            f"⚠️ Worst City: {worst['City']} ({worst[score_col]})"
        )

    # ====================================
    # POLLUTION LEADERBOARD
    # ====================================

    st.subheader("🏭 Pollution Leaderboard")

    pollution_rows = []

    for city_name in df["city"].unique():

        city_df = df[df["city"] == city_name]

        row = city_df.tail(1).iloc[0]

        pollution_score = (
            float(row.get("aqi", 0))
            + float(row.get("pm25", 0))
            + float(row.get("pm10", 0))
            + float(row.get("co", 0))
            + float(row.get("no2", 0))
        )

        pollution_rows.append({
            "City": city_name,
            "Pollution": round(
                pollution_score,
                2
            )
        })

    pollution_df = pd.DataFrame(
        pollution_rows
    )

    pollution_df = pollution_df.sort_values(
        "Pollution",
        ascending=False
    )

    st.dataframe(
        pollution_df,
        use_container_width=True,
        hide_index=True
    )

    most_polluted = pollution_df.iloc[0]
    least_polluted = pollution_df.iloc[-1]

    p1, p2 = st.columns(2)

    with p1:

        st.error(
            f"🚨 Most Polluted: {most_polluted['City']} ({most_polluted['Pollution']})"
        )

    with p2:

        st.success(
            f"🌿 Cleanest City: {least_polluted['City']} ({least_polluted['Pollution']})"
        )

    # ====================================
    # URBAN HEALTH INDEX
    # ====================================

    st.subheader(
        "💚 Urban Health Index"
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

        if urban_score >= 85:

            health_status = "Excellent"

        elif urban_score >= 70:

            health_status = "Good"

        elif urban_score >= 50:

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

    st.dataframe(
        uhi_df,
        use_container_width=True,
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

    uhi_fig = go.Figure()

    uhi_fig.add_bar(
        x=uhi_df["City"],
        y=uhi_df["Urban Health Index"]
    )

    uhi_fig.update_layout(
        title="Urban Health Index Ranking"
    )

    st.plotly_chart(
        uhi_fig,
        use_container_width=True
    )

    return pollution_df, uhi_df