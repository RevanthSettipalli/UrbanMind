import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="UrbanMind",
    layout="wide"
)

st.title("UrbanMind Dashboard")

df = pd.read_csv(
    "data/processed/weather_clean.csv"
)

st.subheader("Weather Dataset")

st.dataframe(df)


fig = px.line(
    df,
    y="temperature",
    title="Temperature Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


fig2 = px.bar(
    df,
    y="humidity",
    title="Humidity Analysis"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

avg = df["temperature"].mean()

st.metric(
    "Average Temperature",
    f"{avg:.1f} °C"
)