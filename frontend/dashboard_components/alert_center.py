import streamlit as st


def render_alert_center(
    plot,
    alerts,
    latest,
    urban,
    selected_city,
    detect_anomalies,
    calculate_risk,
    generate_executive_report
):

    st.subheader("🚨 Real-Time Alert Command Center")

    st.markdown("### 📡 Live Anomaly Feed")

    anomaly_data = detect_anomalies(plot)

    risk_score = anomaly_data.get("risk_score", 0)
    anomaly_alerts = anomaly_data.get("alerts", [])

    st.metric("Risk Score", risk_score)

    if anomaly_alerts:

        for alert in anomaly_alerts:

            if isinstance(alert, dict):

                st.error(
                    alert.get(
                        "message",
                        str(alert)
                    )
                )

            else:

                st.error(str(alert))

    else:

        st.success(
            "No anomalies detected"
        )

    alert_col, risk_col = st.columns(2)

    with alert_col:

        st.markdown("### 🚨 Active Alerts")

        if alerts:

            for alert in alerts:

                if isinstance(alert, dict):

                    st.warning(
                        alert.get(
                            "message",
                            str(alert)
                        )
                    )

                else:

                    st.warning(
                        str(alert)
                    )

        else:

            st.success(
                "✅ No active alerts"
            )

    with risk_col:

        st.markdown(
            "### 🔮 Current Risk Status"
        )

        current_risk = calculate_risk(
            float(latest.get("temperature", 0)),
            float(latest.get("humidity", 0)),
            float(latest.get("aqi", 0)),
            float(latest.get("pm25", 0)),
            float(latest.get("pm10", 0)),
            float(latest.get("co", 0)),
            float(latest.get("no2", 0)),
            urban["score"]
        )

        st.metric(
            "Heat Risk",
            current_risk["heat_risk"]
        )

        st.metric(
            "Pollution Risk",
            current_risk["pollution_risk"]
        )

        st.metric(
            "Urban Risk",
            current_risk["urban_risk"]
        )

        executive_report = (
            generate_executive_report(
                city=(
                    selected_city
                    if selected_city != "All Cities"
                    else "India"
                ),
                score=urban["score"],
                heat_risk=current_risk["heat_risk"],
                pollution_risk=current_risk["pollution_risk"],
                urban_risk=current_risk["urban_risk"]
            )
        )

        st.subheader(
            "🧠 Executive AI Advisor"
        )

        st.info(
            executive_report["summary"]
        )

        st.success(
            executive_report["action"]
        )