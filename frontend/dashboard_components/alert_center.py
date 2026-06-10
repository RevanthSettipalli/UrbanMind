import streamlit as st
from datetime import datetime


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

    st.subheader("🚨 National Risk & Alert Intelligence Center")

    anomaly_data = detect_anomalies(plot)
    anomaly_alerts = anomaly_data.get("alerts", []) if isinstance(anomaly_data, dict) else []

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("🚨 Active Alerts", len(alerts))
    k2.metric("🛰 Anomalies", len(anomaly_alerts))
    k3.metric("🏙 Urban Score", urban["score"])
    k4.metric("📍 Scope", selected_city)
    alert_confidence = round(min(99, 70 + len(alerts) * 4 + len(anomaly_alerts) * 2), 1)

    k5.metric(
        "🎯 Confidence",
        f"{alert_confidence}%"
    )

    st.markdown("### 📡 Live Anomaly Feed")

    def risk_badge(level):
        icons = {
            "LOW": "🟢",
            "MODERATE": "🟡",
            "HIGH": "🔴",
            "CRITICAL": "🚨"
        }
        return f"{icons.get(level, '⚪')} {level}"

    anomaly_alerts = anomaly_data.get("alerts", [])

    st.metric(
        "⚠ Anomaly Risk Score",
        anomaly_data.get("risk_score", 0)
    )
    st.info(
        f"Real-Time Risk Intelligence | Confidence: {alert_confidence}% | Anomalies Detected: {len(anomaly_alerts)}"
    )

    if anomaly_alerts:

        for alert in anomaly_alerts:

            if isinstance(alert, dict):
                severity = "🔴 HIGH"

                st.error(
                    f"{severity} | {alert.get('message', str(alert))}\n\n⏱ {datetime.now().strftime('%H:%M:%S')}"
                )

            else:

                st.error(
                    f"🔴 HIGH | {str(alert)}\n\n⏱ {datetime.now().strftime('%H:%M:%S')}"
                )

    else:

        st.success(
            "No anomalies detected"
        )

    st.info(
        "UrbanMind continuously evaluates environmental anomalies, pollution spikes, climate risks, and urban stability indicators in real time."
    )

    alert_col, risk_col = st.columns(2)

    with alert_col:

        st.markdown("### 🚨 Active Alerts")

        st.caption("Severity • Confidence • Timestamp Driven Alert Intelligence")

        if alerts:

            for alert in alerts:

                st.warning(
                    f"🟠 ACTIVE ALERT | {alert.get('message', str(alert)) if isinstance(alert, dict) else str(alert)} | Confidence: {alert_confidence}%"
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

        # Make displayed risk consistent with active alerts
        alert_count = len(alerts) if alerts else 0

        adjusted_risk_score = current_risk.get('risk_score', 0)

        if alert_count >= 3:
            adjusted_risk_score = max(adjusted_risk_score, 45)
        elif alert_count == 2:
            adjusted_risk_score = max(adjusted_risk_score, 35)
        elif alert_count == 1:
            adjusted_risk_score = max(adjusted_risk_score, 25)

        current_risk['risk_score'] = adjusted_risk_score

        if adjusted_risk_score >= 75:
            current_risk['urban_risk'] = 'CRITICAL'
        elif adjusted_risk_score >= 55:
            current_risk['urban_risk'] = 'HIGH'
        elif adjusted_risk_score >= 35:
            current_risk['urban_risk'] = 'MODERATE'

        st.metric(
            "Overall Risk Score",
            f"{current_risk.get('risk_score', 0)}/100"
        )
        st.metric(
            "🎯 Risk Confidence",
            f"{alert_confidence}%"
        )

        st.progress(
            min(current_risk.get('risk_score', 0), 100) / 100
        )

        import plotly.graph_objects as go

        risk_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=current_risk.get('risk_score', 0),
                title={"text": "National Risk Index"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "steps": [
                        {"range": [0, 40], "color": "green"},
                        {"range": [40, 70], "color": "orange"},
                        {"range": [70, 100], "color": "red"}
                    ]
                }
            )
        )

        st.plotly_chart(
            risk_gauge,
            use_container_width=True
        )

        st.metric(
            "Heat Risk",
            risk_badge(current_risk["heat_risk"])
        )

        st.metric(
            "Pollution Risk",
            risk_badge(current_risk["pollution_risk"])
        )

        st.metric(
            "Urban Risk",
            risk_badge(current_risk["urban_risk"])
        )

        st.success(
            f"Executive Assessment | Heat Risk: {current_risk['heat_risk']} | Pollution Risk: {current_risk['pollution_risk']} | Urban Risk: {current_risk['urban_risk']} | Confidence: {alert_confidence}%"
        )



    st.markdown("---")

    executive_report = generate_executive_report(
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

    st.subheader("📊 Risk Intelligence Summary")

    r1, r2, r3 = st.columns(3)

    r1.metric("🚨 Alerts", len(alerts))
    r2.metric("🛰 Anomalies", len(anomaly_alerts))
    r3.metric("🎯 Confidence", f"{alert_confidence}%")

    st.subheader("🧠 Executive Risk Advisor")

    st.info(
        executive_report.get(
            "summary",
            "Executive assessment unavailable"
        )
    )

    st.success(
        executive_report.get(
            "action",
            "Continue monitoring"
        )
    )

    st.subheader("📋 Recommended Executive Actions")

    st.dataframe(
        {
            "Priority": ["CRITICAL", "HIGH", "HIGH", "MEDIUM"],
            "Action": [
                "Increase monitoring coverage",
                "Deploy preventive resources",
                "Strengthen public advisories",
                "Review sustainability measures"
            ]
        },
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "UrbanMind recommends proactive governance measures, predictive monitoring, and rapid response planning for emerging urban risks."
    )

    st.markdown("---")
    st.caption(
        f"Last Evaluated: {datetime.now().strftime('%d %b %Y %H:%M:%S')}"
    )
    st.success(
        f"🚨 Alert Intelligence Active | Risk Status: {current_risk['urban_risk']} | Alerts: {len(alerts)} | Confidence: {alert_confidence}%"
    )