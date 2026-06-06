

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from backend.intelligence.urban_score import calculate_score


def render_analytics(
    df,
    plot,
    prediction,
    ranking_df
):

    st.subheader("📈 Historical Trends Engine")

    trend_df = plot.copy()

    if len(trend_df) >= 10:

        temp_change = (
            float(trend_df["temperature"].iloc[-1])
            - float(trend_df["temperature"].iloc[0])
        )

        hum_change = (
            float(trend_df["humidity"].iloc[-1])
            - float(trend_df["humidity"].iloc[0])
        )

        t1, t2 = st.columns(2)

        with t1:

            if temp_change > 2:
                st.warning(f"🌡 Temperature rising trend (+{round(temp_change,1)}°C)")
            elif temp_change < -2:
                st.success(f"❄ Temperature cooling trend ({round(temp_change,1)}°C)")
            else:
                st.info("🌡 Temperature stable")

        with t2:

            if hum_change > 5:
                st.warning(f"💧 Humidity increasing trend (+{round(hum_change,1)}%)")
            elif hum_change < -5:
                st.success(f"☀ Humidity decreasing trend ({round(hum_change,1)}%)")
            else:
                st.info("💧 Humidity stable")

        trend_fig = go.Figure()

        trend_fig.add_trace(
            go.Scatter(
                x=trend_df["time"],
                y=trend_df["temperature"],
                name="Temperature"
            )
        )

        trend_fig.add_trace(
            go.Scatter(
                x=trend_df["time"],
                y=trend_df["humidity"],
                name="Humidity"
            )
        )

        st.plotly_chart(
            trend_fig,
            use_container_width=True
        )

    st.subheader("🏙 Multi-City Comparison Dashboard")

    comparison_cities = st.multiselect(
        "Select Cities To Compare",
        sorted(df["city"].unique()),
        default=sorted(df["city"].unique())[:3]
    )

    if comparison_cities:

        comparison_rows = []

        for city_name in comparison_cities:

            city_df = df[df["city"] == city_name]

            if city_df.empty:
                continue

            row = city_df.tail(1).iloc[0]

            city_score = calculate_score(
                float(row["temperature"]),
                float(row["humidity"]),
                prediction,
                float(row.get("aqi", 0)),
                float(row.get("pm25", 0)),
                float(row.get("pm10", 0)),
                float(row.get("co", 0)),
                float(row.get("no2", 0))
            )["score"]

            comparison_rows.append({
                "City": city_name,
                "Urban Score": city_score,
                "AQI": float(row.get("aqi", 0)),
                "Temperature": float(row["temperature"]),
                "Humidity": float(row["humidity"])
            })

        comparison_df = pd.DataFrame(comparison_rows)

        if not comparison_df.empty:

            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    st.subheader("📊 Analytics Intelligence Center")

    analytics_summary = pd.DataFrame([
        {
            "Metric": "Average Temperature",
            "Value": round(float(df["temperature"].mean()), 2)
        },
        {
            "Metric": "Average Humidity",
            "Value": round(float(df["humidity"].mean()), 2)
        },
        {
            "Metric": "Average AQI",
            "Value": round(float(df["aqi"].mean()), 2)
        },
        {
            "Metric": "Average Urban Score",
            "Value": round(float(ranking_df["Score"].mean()), 2)
        }
    ])

    st.dataframe(analytics_summary, use_container_width=True, hide_index=True)

    st.subheader("🧪 Advanced Analytics & Correlation Engine")

    correlation_cols = [
        "temperature",
        "humidity",
        "aqi",
        "pm25",
        "pm10",
        "co",
        "no2"
    ]

    available_cols = [
        col for col in correlation_cols
        if col in df.columns
    ]

    if len(available_cols) >= 2:

        corr_df = df[available_cols].corr()

        corr_fig = go.Figure(
            data=go.Heatmap(
                z=corr_df.values,
                x=corr_df.columns,
                y=corr_df.columns
            )
        )

        st.plotly_chart(
            corr_fig,
            use_container_width=True
        )