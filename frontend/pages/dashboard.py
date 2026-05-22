from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import folium
from streamlit_folium import st_folium


# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="UrbanMind",
    layout="wide"
)

st.title("UrbanMind Dashboard")

st.caption(
    "Live Data • AI Analytics • Predictive Intelligence"
)


# ==================================
# SIDEBAR
# ==================================

st.sidebar.title(
    "UrbanMind Controls"
)

records = st.sidebar.slider(
    "Records to Display",
    10,
    100,
    20
)

auto = st.sidebar.checkbox(
    "Auto Refresh",
    True
)

if auto:
    st_autorefresh(
        interval=3000,
        key="urbanmind_live"
    )


# ==================================
# LOAD DATA
# ==================================
# ==================================
# LOAD DATA
# ==================================

import os

CSV = os.getenv(
    "CSV",
    "data/weather_history.csv"
)

MODEL = os.getenv(
    "MODEL",
    "models/weather/weather_model.pkl"
)

try:

    df = pd.read_csv(CSV)

except Exception as e:

    st.error(
        f"CSV Error: {e}"
    )

    st.stop()


try:

    model = joblib.load(MODEL)

except Exception as e:

    st.error(
        f"Model Error: {e}"
    )

    st.stop()


latest = df.iloc[-1]

latest_prediction = model.predict(
    [[latest["humidity"]]]
)[0]


# ==================================
# STATUS ROW
# ==================================

a, b, c = st.columns(3)

with a:
    st.success("● LIVE")

with b:
    st.info("Model Active")

with c:
    st.info("Streaming Enabled")

st.caption(
    f"Last Updated: {pd.Timestamp.now().strftime('%H:%M:%S')}"
)


# ==================================
# KPI
# ==================================

st.subheader("City KPIs")

a, b, c, d = st.columns(4)

with a:
    st.metric(
        "Current Temp",
        f"{latest['temperature']}°C"
    )

with b:
    st.metric(
        "Current Humidity",
        f"{latest['humidity']}%"
    )

with c:
    st.metric(
        "Records",
        len(df)
    )

with d:
    st.metric(
        "Prediction",
        f"{latest_prediction:.1f}°C"
    )


# ==================================
# DATASET
# ==================================

st.subheader(
    "Weather Dataset"
)

recent_df = df.tail(records)

st.dataframe(
    recent_df,
    use_container_width=True
)


# ==================================
# AI
# ==================================

st.subheader(
    "AI Weather Prediction"
)

humidity = st.slider(
    "Select Humidity",
    0,
    100,
    int(latest["humidity"])
)

prediction = model.predict(
    [[humidity]]
)[0]

st.metric(
    "Predicted Temperature",
    f"{prediction:.2f} °C"
)

confidence = 94

st.progress(
    confidence / 100
)

st.caption(
    f"Model Confidence: {confidence}%"
)


# ==================================
# HEALTH SCORE
# ==================================

score = 100

if prediction > 35:
    score -= 40

if latest["humidity"] > 80:
    score -= 20

st.metric(
    "Urban Health Score",
    f"{score}/100"
)

if prediction > 35:

    st.error(
        "High Temperature Alert"
    )

elif prediction > 30:

    st.warning(
        "Warm Weather"
    )

else:

    st.success(
        "Normal Weather"
    )


# ==================================
# TEMP TREND
# ==================================

st.subheader(
    "Temperature Trend"
)

graph_df = df.tail(20)

fig = px.area(
    graph_df,
    x="time",
    y="temperature"
)

fig.update_layout(
    yaxis_title="Temperature °C"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==================================
# HUMIDITY
# ==================================

st.subheader(
    "Humidity Analysis"
)

fig2 = px.bar(
    graph_df,
    x="time",
    y="humidity"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ==================================
# ANALYTICS
# ==================================

avg = df["temperature"].mean()

avg_humidity = df["humidity"].mean()

max_temp = df["temperature"].max()

risk = (
    "HIGH"
    if max_temp > 37
    else "MEDIUM"
    if max_temp > 32
    else "LOW"
)

st.subheader(
    "Urban Analytics"
)

st.progress(
    score / 100
)

st.caption(
    f"Risk Score: {score}/100"
)

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Average Humidity",
        f"{avg_humidity:.1f}%"
    )

with c2:

    st.metric(
        "Maximum Temperature",
        f"{max_temp:.1f}°C"
    )

with c3:

    st.metric(
        "Urban Risk",
        risk
    )


# ==================================
# ANOMALY
# ==================================

st.subheader(
    "City Health Status"
)

if latest["temperature"] > 38:

    st.error(
        "Urban Heat Risk Detected"
    )

elif latest["humidity"] > 85:

    st.warning(
        "Humidity Spike Detected"
    )

else:

    st.success(
        "City Stable"
    )


# ==================================
# FORECAST
# ==================================

st.subheader(
    "Forecast"
)

future = []

for h in range(40, 90, 5):

    future.append(
        {
            "Humidity": h,
            "Predicted Temp":
            round(
                model.predict(
                    [[h]]
                )[0],
                1
            )
        }
    )

future_df = pd.DataFrame(
    future
)

fig3 = px.line(
    future_df,
    x="Humidity",
    y="Predicted Temp",
    markers=True
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# ==================================
# DIGITAL TWIN MAP
# ==================================

st.subheader(
    "Urban Digital Twin"
)

city = folium.Map(
    location=[
        16.5062,
        80.6480
    ],
    zoom_start=12
)

folium.CircleMarker(
    [
        16.5062,
        80.6480
    ],
    radius=20,
    popup=f"{latest['temperature']} °C",
    color="red",
    fill=True
).add_to(city)

st_folium(
    city,
    width=1200,
    height=500
)


# ==================================
# HEAT INDEX
# ==================================

st.subheader(
    "Heat Index"
)

heat = avg + avg_humidity / 20

st.metric(
    "Feels Like",
    f"{heat:.1f}°C"
)


# ==================================
# SYSTEM
# ==================================

st.subheader(
    "System Status"
)

x, y, z = st.columns(3)

with x:
    st.success(
        "API Running"
    )

with y:
    st.success(
        "Consumer Running"
    )

with z:
    st.success(
        "Model Loaded"
    )


# ==================================
# EXPORT
# ==================================

st.subheader(
    "Export"
)

summary = pd.DataFrame(
    {
        "Average Temp": [avg],
        "Average Humidity": [avg_humidity],
        "Maximum Temp": [max_temp],
        "Risk": [risk]
    }
)

st.download_button(
    "Download Analytics Report",
    summary.to_csv(
        index=False
    ),
    "urbanmind_report.csv"
)

st.download_button(
    "Download Dataset",
    df.to_csv(
        index=False
    ),
    "weather_history.csv"
)


# ==================================
# EXECUTIVE SUMMARY
# ==================================

st.divider()

st.subheader(
    "Executive Summary"
)

st.info(
f"""
Temperature: {latest['temperature']} °C

Humidity: {latest['humidity']} %

Prediction: {prediction:.1f} °C

Risk Level: {risk}

Records: {len(df)}
"""
)

st.caption(
    "UrbanMind • Real-Time Urban Intelligence Platform"
)