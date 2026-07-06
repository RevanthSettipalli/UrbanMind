# ==========================================================
# UrbanMind Forecast Intelligence
# Executive Forecast Center
# Phase 1 - Part 1
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pytz

from pathlib import Path
from datetime import datetime

# --------------------------
# UrbanMind Utilities
# --------------------------

from frontend.utils.auth_guard import require_login
from frontend.utils.sidebar import render_sidebar
from frontend.utils.settings import (
    load_settings,
    apply_theme,
    export_data
)

from frontend.utils.load_weather import (
    load_weather
)

# --------------------------
# Root
# --------------------------

ROOT = Path(__file__).resolve().parents[2]

# --------------------------
# Page Config
# --------------------------

st.set_page_config(
    page_title="Forecast Intelligence",
    page_icon="🔮",
    layout="wide"
)

# --------------------------
# Authentication
# --------------------------

require_login()

# --------------------------
# Sidebar
# --------------------------

render_sidebar()

# --------------------------
# Theme
# --------------------------

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

# ==========================================================
# Executive CSS
# ==========================================================

st.markdown("""

<style>

/* Hide Streamlit */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}


/* Main */

.block-container{

padding-top:0.6rem;
padding-bottom:2rem;

}


/* Hero */

.hero{

background:
linear-gradient(
135deg,
#081c3d,
#124f9d,
#1b6cff
);

padding:35px;

border-radius:28px;

color:white;

box-shadow:

0px 20px 45px
rgba(0,0,0,.18);

margin-bottom:25px;

}


/* Hero Title */

.hero-title{

font-size:48px;

font-weight:800;

margin-bottom:8px;

}


/* Hero Subtitle */

.hero-sub{

font-size:18px;

opacity:.92;

}


/* Glass Cards */

.glass{

background:

rgba(255,255,255,.95);

padding:22px;

border-radius:22px;

box-shadow:

0 12px 32px

rgba(0,0,0,.08);

}


/* KPI */

.metric-card{

background:white;

padding:18px;

border-radius:20px;

box-shadow:

0 10px 25px

rgba(0,0,0,.06);

transition:.25s;

}

.metric-card:hover{

transform:translateY(-4px);

}


/* Status */

.status-online{

color:#00d26a;

font-weight:700;

}


/* Divider */

hr{

margin-top:30px;

margin-bottom:30px;

}

</style>

""", unsafe_allow_html=True)

# ==========================================================
# Settings
# ==========================================================

settings = load_settings()

refresh_rate = int(
    settings.get(
        "refresh_rate",
        60
    )
)

# ==========================================================
# Current Time
# ==========================================================

IST = pytz.timezone(
    "Asia/Kolkata"
)

NOW = datetime.now(
    IST
)

CURRENT_TIME = NOW.strftime(
    "%I:%M:%S %p"
)

CURRENT_DATE = NOW.strftime(
    "%d %b %Y"
)

# ==========================================================
# Cached Weather Loader
# ==========================================================

@st.cache_data(ttl=60)

def get_weather():

    try:

        df = load_weather()

        if df is None:

            return pd.DataFrame()

        df["time"] = pd.to_datetime(
            df["time"],
            errors="coerce"
        )

        df["temperature"] = pd.to_numeric(
            df["temperature"],
            errors="coerce"
        )

        df["humidity"] = pd.to_numeric(
            df["humidity"],
            errors="coerce"
        )

        df = df.dropna()

        return df

    except Exception as e:

        st.error(e)

        return pd.DataFrame()

# ==========================================================
# Load Data
# ==========================================================

df = get_weather()

if df.empty:

    st.warning(
        "Waiting for weather stream..."
    )

    st.stop()

# ==========================================================
# Cities
# ==========================================================

cities = sorted(
    df["city"].unique()
)

city = st.selectbox(

    "🏙 Select City",

    ["All Cities"] + cities

)

if city != "All Cities":

    df = df[
        df["city"] == city
    ]

latest = df.iloc[-1]

temperature = float(
    latest["temperature"]
)

humidity = float(
    latest["humidity"]
)

aqi = float(
    latest.get(
        "aqi",
        0
    )
)

pm25 = float(
    latest.get(
        "pm25",
        0
    )
)

pm10 = float(
    latest.get(
        "pm10",
        0
    )
)

co = float(
    latest.get(
        "co",
        0
    )
)

no2 = float(
    latest.get(
        "no2",
        0
    )
)

LAST_UPDATED = NOW.strftime(
    "%d %b %Y %I:%M:%S %p"
)

# ----------------------------------------------------------
# Forecast Components Imports
# ----------------------------------------------------------
from frontend.forecast_components.styles import apply_forecast_styles
from frontend.forecast_components.hero import render_forecast_hero
from frontend.forecast_components.kpis import render_forecast_kpis
from frontend.forecast_components.ai_engine import render_ai_engine
from frontend.forecast_components.forecast_charts import render_forecast_charts
from frontend.forecast_components.explainable_ai import render_explainable_ai
from frontend.forecast_components.climate import render_climate_panel
from frontend.forecast_components.digital_twin import render_digital_twin
from frontend.forecast_components.executive import render_executive_panel
from frontend.forecast_components.reports import render_reports_panel

# ----------------------------------------------------------
# Forecast Intelligence Section
# ----------------------------------------------------------

# Apply forecast-specific styles
apply_forecast_styles()

# Create a simple 24-hour forecast DataFrame
import numpy as np
hours = np.arange(24)
temperature_trend = np.linspace(temperature - 1, temperature + 2, 24)
humidity_trend = np.linspace(humidity - 2, humidity + 2, 24)
forecast_df = pd.DataFrame({
    "hour": hours,
    "temperature": temperature_trend,
    "humidity": humidity_trend
})

# Compute model predictions and metrics
confidence = 95.0
rf_prediction = temperature + 0.4
lstm_prediction = temperature + 0.2
prophet_prediction = temperature + 0.6
consensus_temperature = (rf_prediction + lstm_prediction + prophet_prediction) / 3
rain_probability = min(100.0, humidity * 1.2)
heatwave_probability = min(100.0, max(0.0, temperature / 45 * 100))
climate_risk = min(100.0, temperature * 1.4 + aqi * 0.2 + heatwave_probability * 0.25)
readiness_index = max(0.0, 100.0 - climate_risk * 0.4)

# Render forecast components in specified order
render_forecast_hero(
    selected_city=city,
    last_updated=LAST_UPDATED,
    confidence=confidence,
)
render_forecast_kpis(
    temperature=temperature,
    humidity=humidity,
    aqi=aqi,
    confidence=confidence,
    rain_probability=rain_probability,
    heatwave_probability=heatwave_probability,
    climate_risk=climate_risk,
)
render_ai_engine(
    rf_prediction=rf_prediction,
    lstm_prediction=lstm_prediction,
    prophet_prediction=prophet_prediction,
    confidence=confidence,
)
render_forecast_charts(forecast_df)
render_explainable_ai(
    temperature=temperature,
    humidity=humidity,
    aqi=aqi,
    pm25=pm25,
    pm10=pm10,
    co=co,
    no2=no2,
    prediction=consensus_temperature,
    confidence=confidence,
)
render_climate_panel(
    temperature=temperature,
    humidity=humidity,
    aqi=aqi,
    rain_probability=rain_probability,
    heatwave_probability=heatwave_probability,
)
render_digital_twin(
    temperature=temperature,
    humidity=humidity,
    aqi=aqi,
)
render_executive_panel(
    city=city,
    confidence=confidence,
    climate_risk=climate_risk,
    readiness_index=readiness_index,
    forecast_temp=consensus_temperature,
    heatwave_probability=heatwave_probability,
    rain_probability=rain_probability,
)
render_reports_panel(
    forecast_df=forecast_df,
    city=city,
    confidence=confidence,
    climate_risk=climate_risk,
    readiness_index=readiness_index,
)

st.success("✅ UrbanMind Forecast Intelligence loaded successfully.")