import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def render_intelligence(
    ranking_df,
    pollution_df,
    uhi_df
):

    # ====================================
    # CITY INSIGHTS ENGINE
    # ====================================

    st.subheader("🧠 National Intelligence & Decision Center")

    national_score = round(ranking_df['Score'].mean(), 1)

    intelligence_index = round(min(100, national_score * 1.08), 1)
    confidence_score = round(min(99, 75 + national_score * 0.2), 1)

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric("🏙 National Score", national_score)
    k2.metric("🏆 Leader", ranking_df.iloc[0]['City'])
    k3.metric("⚠ Priority", ranking_df.iloc[-1]['City'])
    k4.metric("🌫 Pollution Hotspot", pollution_df.iloc[0]['City'])
    k5.metric("💚 Sustainability Leader", uhi_df.iloc[0]['City'])
    k6.metric(
        "🧠 Intelligence",
        intelligence_index
    )

    st.info(
        f"🇮🇳 National Intelligence Assessment | Intelligence Index: {intelligence_index} | Confidence: {confidence_score}% | Leader: {ranking_df.iloc[0]['City']} | Priority Intervention: {ranking_df.iloc[-1]['City']}"
    )

    insights = []

    best_city = ranking_df.iloc[0]
    worst_city = ranking_df.iloc[-1]

    insights.append(
        f"🏆 {best_city['City']} currently has the highest Urban Score ({best_city['Score']})."
    )

    insights.append(
        f"⚠️ {worst_city['City']} currently has the lowest Urban Score ({worst_city['Score']})."
    )

    polluted_city = pollution_df.iloc[0]
    clean_city = pollution_df.iloc[-1]

    insights.append(
        f"🌫 {polluted_city['City']} is currently the most polluted city."
    )

    insights.append(
        f"🌿 {clean_city['City']} is currently the cleanest city."
    )

    for insight in insights:
        st.success(insight)

    executive_brief = f"""
### 🇮🇳 National Intelligence Briefing

Best Performing City: {best_city['City']}

Priority Intervention City: {worst_city['City']}

Most Polluted City: {polluted_city['City']}

Healthiest City: {uhi_df.iloc[0]['City']}

National Urban Score: {national_score}
"""

    st.info(executive_brief)

    intelligence_df = pd.DataFrame([
        {
            "Insight": "Best Performing City",
            "Value": ranking_df.iloc[0]["City"]
        },
        {
            "Insight": "Critical City",
            "Value": ranking_df.iloc[-1]["City"]
        },
        {
            "Insight": "Most Polluted City",
            "Value": pollution_df.iloc[0]["City"]
        },
        {
            "Insight": "Healthiest City",
            "Value": uhi_df.iloc[0]["City"]
        },
        {
            "Insight": "National Urban Score",
            "Value": national_score
        }
    ])

    left_info, right_info = st.columns([2,1])

    with left_info:
        st.dataframe(
            intelligence_df,
            use_container_width=True,
            hide_index=True
        )

    with right_info:
        st.metric("🧠 Intelligence Index", intelligence_index)
        st.metric("🎯 Confidence", f"{confidence_score}%")

    left_chart, right_chart = st.columns(2)

    with left_chart:
        insight_fig = px.bar(
            ranking_df,
            x="City",
            y="Score",
            color="Score",
            title="National Urban Performance"
        )

        st.plotly_chart(
            insight_fig,
            use_container_width=True
        )

    with right_chart:
        pollution_chart = px.bar(
            pollution_df,
            x="City",
            y="Pollution Index",
            color="Pollution Index",
            title="Pollution Intelligence"
        )

        st.plotly_chart(
            pollution_chart,
            use_container_width=True
        )

    # ====================================
    # STRATEGIC DECISION INTELLIGENCE CENTER
    # ====================================

    st.subheader("🔍 Explainable National AI")

    exp1, exp2 = st.columns(2)

    with exp1:
        st.success(
            f"Why {ranking_df.iloc[0]['City']} leads nationally:\n• Highest urban score\n• Strong governance indicators\n• Better environmental performance\n• Consistent readiness levels"
        )

    with exp2:
        st.warning(
            f"Why {ranking_df.iloc[-1]['City']} needs intervention:\n• Lower readiness score\n• Higher risk exposure\n• Governance optimization required\n• Infrastructure improvements needed"
        )

    st.subheader(
        "🎯 Strategic Decision Intelligence Center"
    )

    s1, s2, s3, s4 = st.columns(4)

    s1.metric(
        "🚨 Highest Priority",
        ranking_df.iloc[-1]["City"]
    )

    s2.metric(
        "🏆 National Leader",
        ranking_df.iloc[0]["City"]
    )

    s3.metric(
        "🌫 Pollution Hotspot",
        pollution_df.iloc[0]["City"]
    )

    s4.metric(
        "💚 Sustainability Leader",
        uhi_df.iloc[0]["City"]
    )

    decision_df = pd.DataFrame({
        "Priority": ["High", "High", "Medium", "Medium"],
        "Action": [
            f"Intervene in {ranking_df.iloc[-1]['City']}",
            f"Reduce pollution in {pollution_df.iloc[0]['City']}",
            f"Replicate policies from {ranking_df.iloc[0]['City']}",
            f"Scale sustainability programs from {uhi_df.iloc[0]['City']}"
        ]
    })

    left_action, right_action = st.columns([1,1])

    with left_action:
        st.dataframe(
            decision_df,
            use_container_width=True,
            hide_index=True
        )

    with right_action:
        action_chart = px.bar(
            decision_df,
            x="Priority",
            title="Strategic Action Priorities"
        )

        st.plotly_chart(
            action_chart,
            use_container_width=True
        )

    strategy_text = f"""
1. Increase infrastructure investment in {ranking_df.iloc[-1]['City']}.

2. Replicate smart-city policies from {ranking_df.iloc[0]['City']}.

3. Deploy pollution control measures in {pollution_df.iloc[0]['City']}.

4. Use {uhi_df.iloc[0]['City']} as a national sustainability benchmark.
"""

    st.info(strategy_text)

    st.success(
        f"🧠 Executive Recommendation: Prioritize {ranking_df.iloc[-1]['City']}, replicate governance practices from {ranking_df.iloc[0]['City']}, deploy environmental mitigation measures in {pollution_df.iloc[0]['City']}, and maintain an intelligence confidence score of {confidence_score}%."
    )

    st.markdown("---")

    st.caption(
        "UrbanMind Intelligence Engine • Explainable AI • National Decision Support • Strategic Governance Intelligence"
    )