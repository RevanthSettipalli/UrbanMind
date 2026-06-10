import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def render_executive_center(
    df,
    ranking_df,
    alerts
):

    st.subheader("🏛 National Executive Situation Room")

    status1, status2, status3, status4 = st.columns(4)

    status1.success("⚡ Power Grid Stable")
    status2.success("🚦 Mobility Active")
    status3.success("🏥 Healthcare Online")
    status4.success("🌐 Connectivity Healthy")

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

    st.subheader("🧠 National Executive Intelligence Center")

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

    leader_city = best_city['City']
    priority_city = worst_city['City']

    st.info(
        f"🇮🇳 National Executive Assessment | Score: {avg_score} | Leader: {leader_city} | Priority Intervention: {priority_city} | Readiness: {readiness_index}% | Intelligence Index: {national_intelligence}/100"
    )

    executive_summary = f"""
### 🇮🇳 Executive Situation Assessment

National Urban Score: {avg_score}

Best Performing City: {best_city['City']}

Priority Intervention City: {worst_city['City']}

National Readiness: {readiness_index}%

Executive Risk Level: {executive_risk}%
"""

    st.info(executive_summary)

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

    st.subheader("🤖 AI Governance Recommendations")

    action_df = pd.DataFrame({
        "Priority": ["HIGH", "HIGH", "MEDIUM", "LOW"],
        "Action": [
            f"Immediate intervention planning for {worst_city['City']}",
            f"Replicate best practices from {best_city['City']}",
            "Expand predictive monitoring coverage",
            "Optimize sustainability resource allocation"
        ]
    })

    st.dataframe(
        action_df,
        use_container_width=True,
        hide_index=True
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🏆 Top Performing Cities")
        st.bar_chart(
            ranking_df.head(5).set_index("City")[["Score"]]
        )

    with col_b:
        st.subheader("⚠ Cities Requiring Attention")
        st.bar_chart(
            ranking_df.tail(5).set_index("City")[["Score"]]
        )

    st.subheader("🚨 National Alert Summary")

    a1, a2, a3, a4 = st.columns(4)

    a1.metric("🚨 Total Alerts", len(alerts))
    a2.metric("⚠ Critical Cities", critical_cities)
    a3.metric("🌍 National UHI", national_uhi)
    a4.metric("🎯 Readiness Index", f"{readiness_index}%")

    # =================================
    # EXECUTIVE VISUAL INTELLIGENCE
    # =================================

    st.subheader("📊 Executive Risk Intelligence")

    healthy_cities = len(
        ranking_df[
            ranking_df["Score"] >= 80
        ]
    )

    alert_cities = len(
        ranking_df[
            (ranking_df["Score"] >= 60)
            &
            (ranking_df["Score"] < 80)
        ]
    )

    high_risk_cities = len(
        ranking_df[
            (ranking_df["Score"] >= 40)
            &
            (ranking_df["Score"] < 60)
        ]
    )

    risk_chart = pd.DataFrame(
        {
            "Category": [
                "Excellent",
                "Good",
                "High Risk",
                "Critical"
            ],
            "Count": [
                healthy_cities,
                alert_cities,
                high_risk_cities,
                critical_cities
            ]
        }
    )

    risk_fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "domain"}, {"type": "xy"}]],
        subplot_titles=("National Risk Classification", "Risk Distribution by Cities")
    )

    risk_fig.add_trace(
        go.Pie(
            labels=risk_chart["Category"],
            values=risk_chart["Count"],
            hole=0.45
        ),
        row=1,
        col=1
    )

    risk_fig.add_trace(
        go.Bar(
            x=risk_chart["Category"],
            y=risk_chart["Count"]
        ),
        row=1,
        col=2
    )

    risk_fig.update_layout(
        height=450,
        showlegend=True
    )

    st.plotly_chart(risk_fig, use_container_width=True)

    st.success(
        f"🏆 National Leader: {best_city['City']} | ⚠ Priority Intervention: {worst_city['City']} | 🎯 National Readiness: {readiness_index}/100"
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
            title={"text": "National Readiness Index"},
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
        gauge,
        use_container_width=True
    )

    st.subheader("📈 National Performance Intelligence")

    performance_fig = go.Figure()
    performance_fig.add_bar(
        x=ranking_df["City"],
        y=ranking_df["Score"]
    )
    performance_fig.update_layout(
        title="National Urban Performance Ranking",
        height=420
    )

    st.plotly_chart(
        performance_fig,
        use_container_width=True
    )

    st.subheader("📄 Board Executive Briefing")

    st.markdown(
        f'''
### 🇮🇳 National Executive Briefing

**National Status:** {'Excellent' if avg_score >= 85 else 'Good' if avg_score >= 70 else 'Moderate' if avg_score >= 50 else 'Critical'}

**National Urban Score:** {avg_score}

**Best Performing City:** {best_city['City']}

**Priority Intervention City:** {worst_city['City']}

**National Intelligence Index:** {national_intelligence}/100

**Strategic Recommendation:** Continue predictive governance, targeted intervention, resilience planning, and sustainability optimization across monitored cities.
'''
    )