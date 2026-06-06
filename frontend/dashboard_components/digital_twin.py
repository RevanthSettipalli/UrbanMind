import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_digital_twin(
    national_score,
    national_aqi,
    national_risk,
    avg_score,
    pollution_df,
    uhi_df
):

    # ====================================
    # NATIONAL DIGITAL TWIN & SIMULATION PLATFORM
    # ====================================

    st.subheader("🌍 National Digital Twin & Simulation Platform")

    simulation_mode = st.selectbox(
        "Select Simulation Scenario",
        [
            "Heatwave Event",
            "Pollution Surge",
            "Smart City Upgrade",
            "Emergency Response"
        ],
        key="digital_twin_simulation"
    )

    sim_score = national_score
    sim_aqi = national_aqi

    if simulation_mode == "Heatwave Event":
        sim_score = max(0, national_score - 12)
        sim_aqi = round(national_aqi + 1.0, 2)

    elif simulation_mode == "Pollution Surge":
        sim_score = max(0, national_score - 18)
        sim_aqi = round(national_aqi + 2.0, 2)

    elif simulation_mode == "Smart City Upgrade":
        sim_score = min(100, national_score + 10)
        sim_aqi = max(0, round(national_aqi - 0.8, 2))

    elif simulation_mode == "Emergency Response":
        sim_score = min(100, national_score + 5)
        sim_aqi = max(0, round(national_aqi - 0.4, 2))

    sd1, sd2, sd3 = st.columns(3)

    sd1.metric("Current Score", national_score)

    sd2.metric(
        "Simulated Score",
        sim_score,
        round(sim_score - national_score, 1)
    )

    sd3.metric(
        "Simulated AQI",
        sim_aqi,
        round(sim_aqi - national_aqi, 2)
    )

    # ====================================
    # POLICY IMPACT PREDICTION ENGINE
    # ====================================

    st.subheader("🏛 Policy Impact Prediction Engine")

    policy_option = st.selectbox(
        "Select Policy Scenario",
        [
            "Green Infrastructure Investment",
            "Public Transport Expansion",
            "Pollution Control Program",
            "Smart City Modernization"
        ],
        key="policy_prediction_engine"
    )

    policy_score = national_score
    policy_aqi = national_aqi

    if policy_option == "Green Infrastructure Investment":
        policy_score += 6
        policy_aqi = max(0, round(policy_aqi - 0.5, 2))

    elif policy_option == "Public Transport Expansion":
        policy_score += 4
        policy_aqi = max(0, round(policy_aqi - 0.3, 2))

    elif policy_option == "Pollution Control Program":
        policy_score += 8
        policy_aqi = max(0, round(policy_aqi - 0.8, 2))

    elif policy_option == "Smart City Modernization":
        policy_score += 10
        policy_aqi = max(0, round(policy_aqi - 0.4, 2))

    st.success(
        f"AI Prediction: '{policy_option}' could improve the National Urban Score to {round(policy_score,1)} while reducing AQI to {policy_aqi}."
    )

    # ====================================
    # DISASTER & EMERGENCY RESPONSE SIMULATOR
    # ====================================

    st.subheader("🚨 Disaster & Emergency Response Simulator")

    emergency_scenario = st.selectbox(
        "Select Emergency Scenario",
        [
            "Extreme Heatwave",
            "Severe Air Pollution",
            "Urban Flooding",
            "Industrial Accident"
        ],
        key="emergency_response_simulator"
    )

    response_level = "LOW"
    resource_units = 25

    if emergency_scenario == "Extreme Heatwave":
        response_level = "HIGH"
        resource_units = 80

    elif emergency_scenario == "Severe Air Pollution":
        response_level = "CRITICAL"
        resource_units = 100

    elif emergency_scenario == "Urban Flooding":
        response_level = "HIGH"
        resource_units = 90

    elif emergency_scenario == "Industrial Accident":
        response_level = "MEDIUM"
        resource_units = 70

    st.error(
        f"Emergency Intelligence: Scenario '{emergency_scenario}' would require {resource_units} response units with a projected emergency level of {response_level}."
    )

    # ====================================
    # NATIONAL RESILIENCE & SUSTAINABILITY
    # ====================================

    st.subheader(
        "🌱 National Resilience & Sustainability Intelligence Center"
    )

    resilience_score = round(
        (national_score * 0.6)
        + (100 - (national_aqi * 10)) * 0.4,
        1
    )

    if resilience_score >= 85:
        resilience_status = "Excellent"
    elif resilience_score >= 70:
        resilience_status = "Good"
    elif resilience_score >= 50:
        resilience_status = "Moderate"
    else:
        resilience_status = "Critical"

    r1, r2, r3, r4 = st.columns(4)

    r1.metric(
        "🌍 Resilience Score",
        resilience_score
    )

    r2.metric(
        "♻ Sustainability Status",
        resilience_status
    )

    r3.metric(
        "💚 Green Leader",
        uhi_df.iloc[0]["City"]
    )

    r4.metric(
        "⚠ Climate Risk",
        national_risk
    )

    st.success(
        f"UrbanMind Sustainability Intelligence predicts a resilience score of {resilience_score} with {uhi_df.iloc[0]['City']} serving as the national sustainability benchmark."
    )