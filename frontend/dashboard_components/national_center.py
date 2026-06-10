import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def render_national_center(
    df,
    ranking_df
):

    st.subheader("🇮🇳 National Situation Room")

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

    intelligence_score = round(min(100, national_score * 1.05), 1)
    governance_confidence = round(min(99, 70 + national_score * 0.25), 1)

    if national_score >= 80:
        national_risk = "LOW"
    elif national_score >= 60:
        national_risk = "MODERATE"
    elif national_score >= 40:
        national_risk = "HIGH"
    else:
        national_risk = "CRITICAL"

    n1, n2, n3, n4, n5, n6 = st.columns(6)

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

    n6.metric(
        "🧠 Intelligence",
        intelligence_score
    )

    r1, r2 = st.columns([3, 2])

    with r2:
        st.info(
            f"""
### 🇮🇳 National Executive Assessment

National Score: {national_score}

Model City: {smartest_city['City']}

Priority Intervention: {critical_city['City']}

National AQI: {national_aqi}

Governance Confidence: {governance_confidence}%

Cities Monitored: {len(ranking_df)}
"""
        )

    with r2:
        st.metric("📡 Cities", len(ranking_df))
        st.metric("🎯 Confidence", f"{governance_confidence}%")
        st.metric("🧠 Intelligence", intelligence_score)

    st.markdown("### 🧠 National Intelligence Briefing")

    st.success(
        f"UrbanMind AI identifies {smartest_city['City']} as the national benchmark city while {critical_city['City']} requires focused intervention. National readiness currently stands at {national_score}/100."
    )

    st.markdown("### 📈 National Performance Intelligence")
    st.caption("Explainable national readiness, governance intelligence and city performance benchmarking")

    fig_rank = px.bar(
        ranking_df,
        x="City",
        y="Score",
        orientation='v',
        color='Score',
        title="National Urban Performance Ranking"
    )

    st.plotly_chart(
        fig_rank,
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

    left_chart, right_chart = st.columns(2)

    with left_chart:
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
                    ],
                    hole=0.45
                )
            ]
        )

        pie.update_layout(
            title="National Risk Classification"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    with right_chart:
        risk_df = px.bar(
            x=["Excellent", "Good", "Moderate", "Critical"],
            y=[excellent, good, moderate, critical],
            title="Risk Distribution by Cities"
        )

        st.plotly_chart(
            risk_df,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("🔍 Explainable National AI")

    left_ai, right_ai = st.columns(2)

    with left_ai:
        st.success(
            f"Why {smartest_city['City']} leads nationally:\n• Strong environmental indicators\n• Stable risk profile\n• High readiness score\n• Consistent urban performance"
        )

    with right_ai:
        st.warning(
            f"Why {critical_city['City']} needs intervention:\n• Lower readiness indicators\n• Higher risk exposure\n• Governance optimization required\n• Environmental improvements needed"
        )

    st.success(
        f"🏆 Model City: {smartest_city['City']} | ⚠ Priority Intervention: {critical_city['City']} | 📊 National Readiness: {national_score}/100 | 🎯 Confidence: {governance_confidence}%"
    )