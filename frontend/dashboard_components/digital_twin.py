import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


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

    st.subheader("🌍 National Digital Twin Intelligence Platform")

    st.markdown(
        """
        ### National Urban Digital Twin
        Real-time scenario simulation, policy forecasting, emergency preparedness modeling, and sustainability intelligence for smart-city governance.
        """
    )

    intelligence_score = round(min(100, national_score * 1.08), 1)
    confidence_score = round(min(99, 78 + national_score * 0.2), 1)

    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric("🏙 National Score", national_score)
    k2.metric("🌫 National AQI", national_aqi)
    k3.metric("⚠ Risk Level", national_risk)
    k4.metric("🛰 Twin Status", "ACTIVE")
    k5.metric("🧠 Intelligence", intelligence_score)
    k6.metric("🎯 Confidence", f"{confidence_score}%")

    st.info(
        f"Digital Twin Assessment | Intelligence Index: {intelligence_score} | Confidence: {confidence_score}% | National Risk: {national_risk}"
    )

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

    comparison_df = pd.DataFrame({
        "Scenario": ["Current", "Simulation"],
        "Urban Score": [national_score, sim_score],
        "AQI": [national_aqi, sim_aqi]
    })

    comparison_fig = px.bar(
        comparison_df,
        x="Scenario",
        y="Urban Score",
        color="Urban Score",
        text="Urban Score",
        title="Digital Twin Scenario Comparison"
    )
    comparison_fig.update_layout(height=420)

    c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            comparison_fig,
            use_container_width=True
        )

    with c2:
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sim_score,
            title={'text': "Projected Readiness"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': 'darkblue'},
                'steps': [
                    {'range': [0, 50], 'color': 'lightcoral'},
                    {'range': [50, 75], 'color': 'gold'},
                    {'range': [75, 100], 'color': 'lightgreen'}
                ]
            }
        ))
        gauge_fig.update_layout(height=420)
        st.plotly_chart(gauge_fig, use_container_width=True)

    st.subheader("🔍 Explainable Simulation Intelligence")

    exp1, exp2 = st.columns(2)

    with exp1:
        st.success(
            f"Selected Scenario: {simulation_mode}\n• Simulated Score: {sim_score}\n• AQI Projection: {sim_aqi}\n• Predicted National Impact Generated"
        )

    with exp2:
        st.warning(
            f"Expected Score Change: {round(sim_score - national_score,1)}\nExpected AQI Change: {round(sim_aqi - national_aqi,2)}\nConfidence: {confidence_score}%"
        )

    # ====================================
    # POLICY IMPACT PREDICTION ENGINE
    # ====================================

    st.markdown("---")
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

    policy_df = pd.DataFrame({
        "Metric": ["Current Score", "Policy Score"],
        "Value": [national_score, policy_score]
    })

    policy_fig = px.bar(
        policy_df,
        x="Metric",
        y="Value",
        color="Value",
        text="Value",
        title="Policy Impact Projection"
    )
    policy_fig.update_layout(height=400)

    st.plotly_chart(
        policy_fig,
        use_container_width=True
    )

    st.metric(
        "🏛 Policy Confidence",
        f"{confidence_score}%"
    )

    # ====================================
    # DISASTER & EMERGENCY RESPONSE SIMULATOR
    # ====================================

    st.markdown("---")
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

    response_df = pd.DataFrame({
        "Category": ["Response Units", "Preparedness Index"],
        "Value": [resource_units, max(0, 100 - resource_units/2)]
    })

    response_fig = px.bar(
        response_df,
        x="Category",
        y="Value",
        color="Value",
        title="Emergency Response Intelligence"
    )

    st.plotly_chart(
        response_fig,
        use_container_width=True
    )

    # ====================================
    # NATIONAL RESILIENCE & SUSTAINABILITY
    # ====================================

    st.markdown("---")
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


    r1, r2, r3, r4, r5 = st.columns(5)

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

    r5.metric(
        "🎯 Confidence",
        f"{confidence_score}%"
    )

    st.success(
        f"UrbanMind Sustainability Intelligence predicts a resilience score of {resilience_score} with {uhi_df.iloc[0]['City']} serving as the national sustainability benchmark."
    )

    st.subheader("📊 Strategic Digital Twin Intelligence")

    strategy_df = pd.DataFrame({
        "Area": [
            "Urban Readiness",
            "Policy Impact",
            "Emergency Preparedness",
            "Sustainability"
        ],
        "Score": [
            national_score,
            round(policy_score,1),
            max(0, 100 - resource_units/2),
            resilience_score
        ]
    })

    strategy_fig = px.bar(
        strategy_df,
        x="Area",
        y="Score",
        color="Score",
        text="Score",
        title="Strategic Digital Twin Intelligence"
    )
    strategy_fig.update_layout(height=450)

    st.plotly_chart(strategy_fig, use_container_width=True)

    st.subheader("🧠 Executive Digital Twin Assessment")

    st.info(
        f"UrbanMind Digital Twin forecasts national readiness at {national_score}/100. Under the selected scenario, urban performance shifts to {round(sim_score,1)} while sustainability resilience remains {resilience_status}. Policy simulations indicate that '{policy_option}' delivers the strongest projected impact for urban improvement."
    )

    st.success(
        f"🌍 Digital Twin ACTIVE | ♻ Resilience: {resilience_status} | 🏆 Sustainability Leader: {uhi_df.iloc[0]['City']} | 🎯 Confidence: {confidence_score}%"
    )
    
    st.info(
        "Executive Insight: Digital Twin simulations provide explainable policy evaluation, resilience forecasting, and risk-aware governance recommendations suitable for national smart-city planning."
    )
    
    st.markdown("---")
    st.caption(
        "UrbanMind v2.0 | Research-Grade Digital Twin Platform | Explainable AI | Scenario Intelligence | Policy Forecasting | Sustainability Analytics"
    )