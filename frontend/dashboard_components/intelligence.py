import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_intelligence(
    ranking_df,
    pollution_df,
    uhi_df
):

    # ====================================
    # CITY INSIGHTS ENGINE
    # ====================================

    st.subheader("🧠 City Insights Engine")

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
        st.info(insight)

    # ====================================
    # URBAN INTELLIGENCE INSIGHTS ENGINE
    # ====================================

    st.subheader("🧠 Urban Intelligence Insights Engine")

    i1, i2, i3, i4 = st.columns(4)

    i1.metric(
        "🏆 Best City",
        ranking_df.iloc[0]["City"]
    )

    i2.metric(
        "⚠ Critical City",
        ranking_df.iloc[-1]["City"]
    )

    i3.metric(
        "🌫 Most Polluted",
        pollution_df.iloc[0]["City"]
    )

    i4.metric(
        "💚 Healthiest",
        uhi_df.iloc[0]["City"]
    )

    insight_text = f"""
🏆 {ranking_df.iloc[0]['City']} currently leads India in Urban Performance.

⚠ {ranking_df.iloc[-1]['City']} requires immediate urban intervention.

🌫 Pollution levels are highest in {pollution_df.iloc[0]['City']}.

💚 {uhi_df.iloc[0]['City']} currently maintains the healthiest urban ecosystem.

📈 National Urban Score is {round(ranking_df['Score'].mean(),1)}.
"""

    st.info(insight_text)

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
            "Value": round(
                ranking_df["Score"].mean(),
                1
            )
        }
    ])

    st.dataframe(
        intelligence_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "### 📈 Intelligence Ranking Overview"
    )

    insight_fig = go.Figure()

    insight_fig.add_bar(
        x=ranking_df["City"],
        y=ranking_df["Score"]
    )

    st.plotly_chart(
        insight_fig,
        use_container_width=True
    )

    # ====================================
    # STRATEGIC DECISION INTELLIGENCE CENTER
    # ====================================

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

    strategy_text = f"""
1. Increase infrastructure investment in {ranking_df.iloc[-1]['City']}.

2. Replicate smart-city policies from {ranking_df.iloc[0]['City']}.

3. Deploy pollution control measures in {pollution_df.iloc[0]['City']}.

4. Use {uhi_df.iloc[0]['City']} as a national sustainability benchmark.
"""

    st.info(strategy_text)