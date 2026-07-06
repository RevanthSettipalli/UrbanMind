import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
def render_governance_ai(
    df,
    ranking_df
):
    city_col = "city" if "city" in ranking_df.columns else "City"
    score_col = "score" if "score" in ranking_df.columns else "Score"

    avg_score = round(
        float(ranking_df[score_col].mean()),
        1
    )

    st.subheader("🏛 National Governance Intelligence Center")

    national_intelligence = round(avg_score * 1.05, 1)

    best_city_name = ranking_df.iloc[0][city_col]
    worst_city_name = ranking_df.iloc[-1][city_col]

    governance_status = "ACTIVE"

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("🏛 Governance", governance_status)
    k2.metric("🏆 Leader", best_city_name)
    k3.metric("⚠ Priority", worst_city_name)
    k4.metric("📊 National Score", avg_score)
    k5.metric("🧠 Intelligence", national_intelligence)

    avg_temp = round(
        float(df["temperature"].mean()),
        1
    )

    avg_humidity = round(
        float(df["humidity"].mean()),
        1
    )

    if avg_score >= 80:

        governance_status = "Excellent"

        governance_action = (
            "Maintain current smart-city policies, continue sustainability programs and expand best practices nationwide."
        )

    elif avg_score >= 60:

        governance_status = "Good"

        governance_action = (
            "Strengthen environmental monitoring and optimize urban infrastructure investments."
        )

    elif avg_score >= 40:

        governance_status = "Moderate"

        governance_action = (
            "Increase intervention in underperforming cities and improve pollution mitigation strategies."
        )

    else:

        governance_status = "Critical"

        governance_action = (
            "Immediate national intervention required across environmental, transportation and public-health sectors."
        )

    g1, g2, g3, g4 = st.columns(4)

    g1.metric(
        "🏛 Governance Status",
        governance_status
    )

    g2.metric(
        "🏆 Model City",
        best_city_name
    )

    g3.metric(
        "⚠ Priority City",
        worst_city_name
    )

    g4.metric(
        "🌡 National Temp",
        f"{avg_temp}°C"
    )

    left_panel, right_panel = st.columns([2, 1])

    with left_panel:
        st.info(
            f"""
### 🇮🇳 National Governance Assessment

Governance Status: {governance_status}

National Urban Score: {avg_score}

Model City: {best_city_name}

Priority Intervention City: {worst_city_name}

Average Temperature: {avg_temp}°C

Average Humidity: {avg_humidity}%
"""
        )

    with right_panel:
        governance_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=avg_score,
                title={"text": "Governance Readiness"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "steps": [
                        {"range": [0, 40], "color": "red"},
                        {"range": [40, 70], "color": "orange"},
                        {"range": [70, 100], "color": "green"}
                    ]
                }
            )
        )

        st.plotly_chart(
            governance_gauge,
            use_container_width=True
        )

    score_chart = px.bar(
        ranking_df.head(10),
        x=city_col,
        y=score_col,
        title="National Governance Performance"
    )

    st.plotly_chart(
        score_chart,
        use_container_width=True
    )

    st.success(
        f"UrbanMind Governance AI identifies {best_city_name} as the national governance benchmark while {worst_city_name} requires focused intervention and accelerated resilience planning."
    )

    # ====================================
    # AUTONOMOUS DECISION INTELLIGENCE
    # ====================================

    st.subheader(
        "🤖 Autonomous Governance Decision Engine"
    )

    budget_priority = worst_city_name
    resource_priority = worst_city_name

    if avg_score < 40:
        emergency_level = "CRITICAL"
    elif avg_score < 60:
        emergency_level = "HIGH"
    elif avg_score < 80:
        emergency_level = "MODERATE"
    else:
        emergency_level = "LOW"

    ad1, ad2, ad3, ad4 = st.columns(4)

    ad1.metric(
        "💰 Budget Priority",
        budget_priority
    )

    ad2.metric(
        "🚑 Emergency Level",
        emergency_level
    )

    ad3.metric(
        "🏗 Resource Focus",
        resource_priority
    )

    ad4.metric(
        "📈 Expected Impact",
        "+15% Readiness"
    )

    decision_summary = pd.DataFrame({
        "Priority": ["Critical", "High", "Medium", "Medium"],
        "Action": [
            f"Intervention Program for {worst_city_name}",
            "Environmental Risk Reduction",
            f"Replication of {best_city_name} Policies",
            "Smart Infrastructure Expansion"
        ]
    })

    left_decision, right_decision = st.columns([1,1])

    with left_decision:
        st.dataframe(
            decision_summary,
            use_container_width=True,
            hide_index=True
        )

    with right_decision:
        priority_chart = px.bar(
            decision_summary,
            x="Priority",
            y=[100, 90, 75, 65],
            title="Governance Priority Matrix"
        )

        st.plotly_chart(
            priority_chart,
            use_container_width=True
        )

    st.info(
        f"AI Governance Engine recommends targeted funding, predictive monitoring, environmental resilience measures, and policy replication from {best_city_name}."
    )

    st.error(
        f"Executive Action Plan: Prioritize {worst_city_name}, deploy preventive resources, increase environmental monitoring, and expand successful governance models from {best_city_name}."
    )

    decision_df = pd.DataFrame([
        {
            'Decision': 'Budget Allocation',
            'Recommendation': budget_priority
        },
        {
            'Decision': 'Emergency Response',
            'Recommendation': emergency_level
        },
        {
            'Decision': 'Resource Deployment',
            'Recommendation': resource_priority
        },
        {
            'Decision': 'Policy Replication',
            'Recommendation': best_city_name
        }
    ])

    col_left, col_right = st.columns(2)

    with col_left:
        st.dataframe(
            decision_df,
            use_container_width=True,
            hide_index=True
        )

    with col_right:
        fig_actions = px.bar(
            x=["Budget", "Emergency", "Resources", "Policy"],
            y=[95, 90, 85, 80],
            title="Governance Action Priority"
        )

        st.plotly_chart(
            fig_actions,
            use_container_width=True
        )

    st.subheader("🎯 Strategic Governance Outlook")

    outlook_df = pd.DataFrame({
        "Initiative": [
            "Environmental Monitoring",
            "Policy Replication",
            "Infrastructure Modernization",
            "Predictive Governance"
        ],
        "Impact": [92, 88, 84, 90]
    })

    outlook_fig = px.bar(
        outlook_df,
        x="Initiative",
        y="Impact",
        title="Projected Governance Impact"
    )

    st.plotly_chart(
        outlook_fig,
        use_container_width=True
    )

    st.success(
        f"🏛 Governance Status: {governance_status} | 🏆 Benchmark City: {best_city_name} | ⚠ Priority City: {worst_city_name}"
    )

    st.caption(
        "UrbanMind Governance AI • Autonomous Decision Intelligence • National Policy Optimization"
    )