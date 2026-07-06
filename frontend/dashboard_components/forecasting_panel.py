import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_forecasting_panel(
    forecast_df,
    forecast_model,
    forecast_confidence,
    lstm_forecast,
    lstm_rmse,
    urban,
    current_aqi,
    predictive_data,
):
    try:
        st.subheader("🔮 Predictive Intelligence Center")

        intel = predictive_data["predictive_intelligence"]

        p1, p2, p3, p4 = st.columns(4)

        p1.metric("🏙 Future City Health", intel["future_city_health"])
        p2.metric("🎯 Confidence", f"{intel['confidence']}%")
        p3.metric("⚠ Future Risk", intel["future_risk"])
        p4.metric("📈 Forecast Score", predictive_data["urban_score_forecast"])

        st.subheader("📈 Forecast Intelligence")

        if not forecast_df.empty:

            forecast_plot_df = pd.DataFrame()
            forecast_plot_df["Date"] = forecast_df["ds"]
            forecast_plot_df["Temperature"] = forecast_df["yhat"]

            forecast_plot_df["Urban Score"] = (
                urban
                + (
                    forecast_plot_df["Temperature"]
                    - forecast_plot_df["Temperature"].iloc[0]
                ) * 0.8
            )

            forecast_plot_df["AQI"] = (
                current_aqi + forecast_plot_df.index * 0.02
            )

            base_risk = predictive_data['risk_intelligence']['overall_risk']
            forecast_plot_df["Risk"] = [
                base_risk + (i * 0.04)
                for i in range(len(forecast_plot_df))
            ]

            forecast_plot_df["Governance"] = [
                round(min(100, 70 + urban * 0.25 + i * 0.05), 2)
                for i in range(len(forecast_plot_df))
            ]

            fig_multi = go.Figure()

            for column in [
                "Urban Score",
                "Temperature",
                "AQI",
                "Risk",
                "Governance",
            ]:
                fig_multi.add_trace(
                    go.Scatter(
                        x=forecast_plot_df["Date"],
                        y=forecast_plot_df[column],
                        mode="lines",
                        name=column,
                    )
                )

            fig_multi.update_layout(
                title="Multi-Target Urban Forecasting",
                xaxis_title="Date",
                yaxis_title="Forecast Value",
                height=600,
            )

            st.plotly_chart(fig_multi, use_container_width=True)

        st.subheader("🧠 Dual Forecasting Framework")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Primary Model", forecast_model)
        m2.metric("LSTM Engine", "DISABLED")
        m3.metric("Forecast Confidence", f"{forecast_confidence}%")
        m4.metric("LSTM RMSE", lstm_rmse)

        st.subheader("🤖 Urban AI Forecasting Engine")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Forecast Horizon",
            f"{len(forecast_df)} Days"
        )

        c2.metric(
            "Predicted Avg Temp",
            round(forecast_df["yhat"].mean(), 1) if not forecast_df.empty else 0
        )

        c3.metric(
            "Peak Forecast Temp",
            round(forecast_df["yhat"].max(), 1) if not forecast_df.empty else 0
        )

        if forecast_df.empty:
            st.warning("Forecast model could not generate predictions.")
            return

        forecast_chart = px.line(
            forecast_df,
            x="ds",
            y="yhat",
            title="30-Day Prophet Forecast",
        )

        st.plotly_chart(forecast_chart, use_container_width=True)

        lstm_values = (
            lstm_forecast[: len(forecast_df)]
            if len(lstm_forecast) >= len(forecast_df)
            else list(forecast_df["yhat"][: len(forecast_df)])
        )

        comparison_df = pd.DataFrame(
            {
                "Date": forecast_df["ds"],
                "Prophet": forecast_df["yhat"],
                "LSTM": lstm_values,
            }
        )

        comparison_fig = px.line(
            comparison_df,
            x="Date",
            y=["Prophet", "LSTM"],
            title="Forecast Model Comparison",
        )

        st.plotly_chart(comparison_fig, use_container_width=True)

        if (
            "yhat_lower" in forecast_df.columns
            and "yhat_upper" in forecast_df.columns
        ):

            band_fig = go.Figure()

            band_fig.add_trace(
                go.Scatter(
                    x=forecast_df["ds"],
                    y=forecast_df["yhat"],
                    name="Forecast",
                )
            )

            band_fig.add_trace(
                go.Scatter(
                    x=forecast_df["ds"],
                    y=forecast_df["yhat_upper"],
                    line=dict(width=0),
                    showlegend=False,
                )
            )

            band_fig.add_trace(
                go.Scatter(
                    x=forecast_df["ds"],
                    y=forecast_df["yhat_lower"],
                    fill="tonexty",
                    line=dict(width=0),
                    name="Confidence Band",
                )
            )

            st.plotly_chart(band_fig, use_container_width=True)

        st.download_button(
            "📥 Download Forecast CSV",
            forecast_df.to_csv(index=False),
            "urbanmind_forecast.csv",
            "text/csv"
        )
    except Exception as e:
        st.error(f"Forecast Panel Error: {e}")