import streamlit as st


def render_executive_center(
    df,
    ranking_df,
    alerts
):

    st.subheader("🎯 Executive Command Center")

    avg_score = round(
        ranking_df["Score"].mean(),
        1
    )

    critical_cities = len(
        ranking_df[
            ranking_df["Score"] < 50
        ]
    )

    national_uhi = avg_score

    e1, e2, e3, e4, e5, e6 = st.columns(6)

    e1.metric(
        "🏙 Cities",
        len(df["city"].unique())
    )

    e2.metric(
        "📄 Records",
        len(df)
    )

    e3.metric(
        "🚨 Alerts",
        len(alerts)
    )

    e4.metric(
        "🔥 Critical",
        critical_cities
    )

    e5.metric(
        "💚 Avg Score",
        avg_score
    )

    e6.metric(
        "🌍 National UHI",
        national_uhi
    )

    if avg_score >= 85:

        st.success(
            "🇮🇳 National Urban Status: Excellent"
        )

    elif avg_score >= 70:

        st.info(
            "🇮🇳 National Urban Status: Good"
        )

    elif avg_score >= 50:

        st.warning(
            "🇮🇳 National Urban Status: Moderate"
        )

    else:

        st.error(
            "🇮🇳 National Urban Status: Critical"
        )