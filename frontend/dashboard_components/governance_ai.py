import streamlit as st
import pandas as pd


def render_governance_ai(
    df,
    ranking_df
):

    avg_score = round(
        float(ranking_df["Score"].mean()),
        1
    )

    st.subheader("🏛 Urban Governance AI")

    best_city_name = ranking_df.iloc[0]["City"]
    worst_city_name = ranking_df.iloc[-1]["City"]

    avg_temp = round(
        float(df["temperature"].mean()),
        1
    )

    avg_humidity = round(
        float(df["humidity"].mean()),
        1
    )

    if avg_score >= 85:

        governance_status = "Excellent"

        governance_action = (
            "Maintain current smart-city policies, continue sustainability programs and expand best practices nationwide."
        )

    elif avg_score >= 70:

        governance_status = "Good"

        governance_action = (
            "Strengthen environmental monitoring and optimize urban infrastructure investments."
        )

    elif avg_score >= 50:

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

    st.info(
        f"Urban Governance AI recommends focusing investments on {worst_city_name} while replicating successful policies from {best_city_name}. Average humidity across monitored cities is {avg_humidity}% and the national urban score is {avg_score}."
    )

    st.success(
        governance_action
    )

    # ====================================
    # AUTONOMOUS DECISION INTELLIGENCE
    # ====================================

    st.subheader(
        "🤖 Autonomous Decision Intelligence"
    )

    budget_priority = worst_city_name
    resource_priority = worst_city_name

    if avg_score < 50:
        emergency_level = "HIGH"
    elif avg_score < 70:
        emergency_level = "MEDIUM"
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
        "+15%"
    )

    st.info(
        f"AI recommends prioritizing funding and infrastructure improvements in {budget_priority}. Environmental resources should be focused on {resource_priority}."
    )

    st.warning(
        f"Autonomous Action Plan: Increase monitoring in {resource_priority}, deploy mitigation measures, strengthen public advisories, and replicate best practices from {best_city_name}."
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

    st.dataframe(
        decision_df,
        use_container_width=True,
        hide_index=True
    )