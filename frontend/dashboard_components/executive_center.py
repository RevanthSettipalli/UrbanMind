import streamlit as st
import plotly.graph_objects as go
import pandas as pd


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

    # =================================
    # EXECUTIVE INTELLIGENCE
    # =================================

    best_city = ranking_df.iloc[0]
    worst_city = ranking_df.iloc[-1]

    readiness_index = round(
        min(100, avg_score + 5),
        1
    )

    executive_risk = round(
        max(0, 100 - avg_score),
        1
    )

    national_intelligence = round(
        (
            national_uhi
            + avg_score
            + readiness_index
        ) / 3,
        1
    )

    st.subheader("🏛 Executive Intelligence Center")

    x1, x2, x3, x4 = st.columns(4)

    x1.metric(
        "🎯 Readiness Index",
        f"{readiness_index}%"
    )

    x2.metric(
        "⚠ Executive Risk",
        f"{executive_risk}%"
    )

    x3.metric(
        "🌍 Intelligence Index",
        f"{national_intelligence}/100"
    )

    x4.metric(
        "🏆 Best Score",
        round(float(best_city['Score']), 1)
    )

    st.subheader("🧠 Executive Briefing")

    c1, c2, c3 = st.columns(3)

    c1.success(
        f"🏆 Best City: {best_city['City']}"
    )

    c2.error(
        f"⚠ Highest Risk City: {worst_city['City']}"
    )

    c3.info(
        f"🎯 National Readiness: {readiness_index}%"
    )

    st.subheader("🤖 AI Decision Support")

    recommendations = []

    if critical_cities > 0:
        recommendations.append(
            "Increase monitoring in high-risk cities."
        )

    recommendations.append(
        "Expand sustainability initiatives."
    )

    recommendations.append(
        "Optimize urban resources using predictive intelligence."
    )

    recommendations.append(
        "Deploy preventive resources to vulnerable regions."
    )

    for recommendation in recommendations:
        st.info(recommendation)

    st.subheader("🏆 Top Performing Cities")
    st.dataframe(
        ranking_df.head(5),
        use_container_width=True
    )

    st.subheader("⚠ Cities Requiring Attention")
    st.dataframe(
        ranking_df.tail(5),
        use_container_width=True
    )

    st.subheader("🚨 National Alert Summary")

    alert_summary = {
        'Total Alerts': len(alerts),
        'Critical Cities': critical_cities,
        'National UHI': national_uhi,
        'Readiness Index': readiness_index,
    }

    st.json(alert_summary)

    # =================================
    # EXECUTIVE VISUAL INTELLIGENCE
    # =================================

    st.subheader("📊 Executive Risk Distribution")

    healthy_cities = len(
        ranking_df[
            ranking_df["Score"] >= 85
        ]
    )

    alert_cities = len(
        ranking_df[
            (ranking_df["Score"] >= 50)
            &
            (ranking_df["Score"] < 85)
        ]
    )

    risk_chart = pd.DataFrame(
        {
            "Category": [
                "Healthy",
                "Alert",
                "Critical"
            ],
            "Count": [
                healthy_cities,
                alert_cities,
                critical_cities
            ]
        }
    )

    st.bar_chart(
        risk_chart.set_index("Category")
    )

    st.subheader("🏆 National Top 3 Cities")

    top3 = ranking_df.head(3)

    t1, t2, t3 = st.columns(3)

    medals = ["🥇", "🥈", "🥉"]

    for col, (_, row), medal in zip(
        [t1, t2, t3],
        top3.iterrows(),
        medals
    ):
        col.success(
            f"{medal} {row['City']}\n\nScore: {round(float(row['Score']),1)}"
        )

    st.subheader("🎯 Executive Readiness Gauge")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=readiness_index,
            title={"text": "National Readiness"},
            gauge={
                "axis": {"range": [0, 100]}
            }
        )
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    st.subheader("📄 Board Executive Summary")

    st.markdown(
        f"""
### National Urban Intelligence Brief

**National Status:** {'Excellent' if avg_score >= 85 else 'Good' if avg_score >= 70 else 'Moderate' if avg_score >= 50 else 'Critical'}

**Best City:** {best_city['City']}

**Highest Risk City:** {worst_city['City']}

**National Intelligence Index:** {national_intelligence}/100

**Recommendation:** Continue predictive monitoring, sustainability initiatives, and targeted intervention in vulnerable cities.
"""
    )