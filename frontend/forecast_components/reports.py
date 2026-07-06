import io
import pandas as pd
import streamlit as st


def render_reports_panel(
    forecast_df: pd.DataFrame,
    city: str,
    confidence: float,
    climate_risk: float,
    readiness_index: float,
):
    """Render export and executive reporting tools."""

    st.subheader("📄 Executive Reports & Export")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("🏙 City", city)
    r2.metric("🎯 Confidence", f"{confidence:.1f}%")
    r3.metric("⚠ Climate Risk", f"{climate_risk:.1f}/100")
    r4.metric("🛡 Readiness", f"{readiness_index:.1f}/100")

    summary = f"""
UrbanMind Executive Forecast Report
===================================

City: {city}
Forecast Confidence: {confidence:.1f}%
Climate Risk: {climate_risk:.1f}/100
Forecast Readiness: {readiness_index:.1f}/100

Key Recommendations:
- Continue real-time monitoring.
- Review AI forecast updates regularly.
- Activate emergency response if climate risk exceeds 80.
"""

    st.markdown("### 📋 Executive Summary")
    st.code(summary)

    csv_buffer = io.StringIO()
    forecast_df.to_csv(csv_buffer, index=False)

    st.download_button(
        label="⬇ Download Forecast CSV",
        data=csv_buffer.getvalue(),
        file_name="urbanmind_forecast.csv",
        mime="text/csv",
        width="stretch",
    )

    st.download_button(
        label="📄 Download Executive Summary",
        data=summary,
        file_name="urbanmind_forecast_summary.txt",
        mime="text/plain",
        width="stretch",
    )

    st.success("Executive report and export package ready.")
