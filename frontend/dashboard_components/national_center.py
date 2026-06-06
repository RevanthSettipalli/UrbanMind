import streamlit as st
import plotly.graph_objects as go


def render_national_center(
    df,
    ranking_df
):

    st.subheader("🇮🇳 National Intelligence Center")

    national_score = round(
        ranking_df["Score"].mean(),
        1
    )

    smartest_city = ranking_df.iloc[0]
    critical_city = ranking_df.iloc[-1]

    national_aqi = round(
        df["aqi"].mean(),
        2
    )

    if national_score >= 80:
        national_risk = "LOW"
    elif national_score >= 60:
        national_risk = "MODERATE"
    elif national_score >= 40:
        national_risk = "HIGH"
    else:
        national_risk = "CRITICAL"

    n1, n2, n3, n4, n5 = st.columns(5)

    n1.metric(
        "🇮🇳 National Score",
        national_score
    )

    n2.metric(
        "🏆 Smartest City",
        smartest_city["City"]
    )

    n3.metric(
        "⚠ Critical City",
        critical_city["City"]
    )

    n4.metric(
        "🌫 National AQI",
        national_aqi
    )

    n5.metric(
        "🔥 National Risk",
        national_risk
    )

    st.markdown(
        "### 🧠 India Intelligence Summary"
    )

    summary = f"""
India currently maintains an Urban Score of {national_score}.

Top Performing City: {smartest_city['City']}

Most Critical City: {critical_city['City']}

Average AQI: {national_aqi}

Total Cities Monitored: {len(ranking_df)}

National Readiness Index: {national_score}/100
"""

    st.info(summary)

    if national_score >= 80:

        st.success(
            "🇮🇳 National Urban Ecosystem Status: Excellent"
        )

    elif national_score >= 60:

        st.info(
            "🇮🇳 National Urban Ecosystem Status: Good"
        )

    elif national_score >= 40:

        st.warning(
            "🇮🇳 National Urban Ecosystem Status: Moderate"
        )

    else:

        st.error(
            "🇮🇳 National Urban Ecosystem Status: Critical"
        )

    # ===============================
    # NATIONAL ANALYTICS
    # ===============================

    st.markdown(
        "### 🗺 National City Performance"
    )

    heatmap_fig = go.Figure()

    heatmap_fig.add_bar(
        x=ranking_df["City"],
        y=ranking_df["Score"]
    )

    heatmap_fig.update_layout(
        title="National Urban Score Distribution"
    )

    st.plotly_chart(
        heatmap_fig,
        use_container_width=True
    )

    st.markdown(
        "### 🚨 National Risk Distribution"
    )

    excellent = len(
        ranking_df[
            ranking_df["Score"] >= 80
        ]
    )

    good = len(
        ranking_df[
            (ranking_df["Score"] >= 60)
            &
            (ranking_df["Score"] < 80)
        ]
    )

    moderate = len(
        ranking_df[
            (ranking_df["Score"] >= 40)
            &
            (ranking_df["Score"] < 60)
        ]
    )

    critical = len(
        ranking_df[
            ranking_df["Score"] < 40
        ]
    )

    pie = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Excellent",
                    "Good",
                    "Moderate",
                    "Critical"
                ],
                values=[
                    excellent,
                    good,
                    moderate,
                    critical
                ]
            )
        ]
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    st.markdown(
        "### 🏆 Top Performing Cities"
    )

    display_df = ranking_df.head(5).copy()

    if len(display_df) >= 1:
        display_df.iloc[0, display_df.columns.get_loc("City")] = f"🥇 {display_df.iloc[0]['City']}"

    if len(display_df) >= 2:
        display_df.iloc[1, display_df.columns.get_loc("City")] = f"🥈 {display_df.iloc[1]['City']}"

    if len(display_df) >= 3:
        display_df.iloc[2, display_df.columns.get_loc("City")] = f"🥉 {display_df.iloc[2]['City']}"

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )