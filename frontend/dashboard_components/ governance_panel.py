

import streamlit as st
import pandas as pd
import plotly.express as px

from backend.intelligence.governance_simulator import simulate_policy


def render_governance_panel(urban):
    st.subheader("🏛 Governance Decision Simulator")

    policy_gain = st.slider(
        "Governance Improvement (%)",
        0,
        30,
        10
    )

    simulated_score = round(
        min(100, urban + policy_gain * 0.6),
        1
    )

    sim1, sim2 = st.columns(2)

    sim1.metric(
        "Current Urban Score",
        urban
    )

    sim2.metric(
        "Simulated Score",
        simulated_score,
        delta=round(simulated_score - urban, 1)
    )

    st.info(
        f"Policy intervention could improve Urban Intelligence from {urban} to {simulated_score}."
    )

    policy_budget = st.slider(
        "Policy Investment (Million ₹)",
        0,
        500,
        100,
        key="policy_budget"
    )

    st.subheader("🌍 Digital Twin Scenario Simulator")

    pollution_cut = st.slider(
        "Pollution Reduction (%)",
        0,
        50,
        10,
        key="pollution_cut"
    )

    traffic_cut = st.slider(
        "Traffic Reduction (%)",
        0,
        50,
        10,
        key="traffic_cut"
    )

    green_increase = st.slider(
        "Green Space Increase (%)",
        0,
        50,
        10,
        key="green_increase"
    )

    simulation = simulate_policy(
        pollution_cut,
        traffic_cut,
        green_increase,
        policy_budget
    )

    st.metric(
        "Future Smart City Score",
        simulation["future_score"],
        delta=simulation["policy_gain"]
    )

    st.metric(
        "Governance Policy ROI",
        f"{simulation['roi']}%"
    )

    st.info(simulation["recommendation"])

    scenario_df = pd.DataFrame({
        "Scenario": [
            "Current",
            "Pollution Policy",
            "Traffic Policy",
            "Green Policy",
            "Combined"
        ],
        "Score": [
            urban,
            urban + pollution_cut * 0.2,
            urban + traffic_cut * 0.15,
            urban + green_increase * 0.25,
            simulation["future_score"]
        ]
    })

    scenario_fig = px.bar(
        scenario_df,
        x="Scenario",
        y="Score",
        color="Score",
        title="Digital Twin Scenario Comparison"
    )

    st.plotly_chart(
        scenario_fig,
        use_container_width=True
    )

    return simulation