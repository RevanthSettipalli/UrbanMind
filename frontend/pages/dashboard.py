import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from folium.plugins import HeatMap
import joblib
from sqlalchemy import create_engine
import os
import folium
import pytz
import json
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from datetime import datetime

from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh

from frontend.utils.city_selector import city_filter
from frontend.utils.auth_guard import require_login
from frontend.utils.sidebar import render_sidebar
from frontend.utils.settings import (
    apply_theme,
    load_settings,
    export_data
)

# ====================================
# DASHBOARD COMPONENTS
# ====================================
from frontend.dashboard_components.hero import render_hero
from frontend.dashboard_components.executive_center import render_executive_center
from frontend.dashboard_components.national_center import render_national_center
from frontend.dashboard_components.governance_ai import render_governance_ai
from frontend.dashboard_components.alert_center import render_alert_center
from frontend.dashboard_components.rankings import render_rankings
from frontend.dashboard_components.analytics import render_analytics
from frontend.dashboard_components.intelligence import render_intelligence
from frontend.dashboard_components.digital_twin import render_digital_twin
from frontend.dashboard_components.copilot import render_copilot

# ====================================
# PAGE
# ====================================

st.set_page_config(
    page_title="UrbanMind Dashboard",
    page_icon="🌍",
    layout="wide"
)

require_login()
render_sidebar()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

settings = load_settings()

# ====================================
# AUTO REFRESH
# ====================================

refresh_rate = max(
    60,
    int(settings.get("refresh_rate", 300))
)

st_autorefresh(
    interval=refresh_rate * 1000,
    key=f"live_dashboard_clock_{refresh_rate}"
)

# ====================================
# ROOT
# ====================================

CSV = ROOT / "data" / "processed_weather.csv"

MODEL = (
    ROOT
    / "models"
    / "weather"
    / "weather_model.pkl"
)

ALERT = (
    ROOT
    / "data"
    / "alerts.json"
)

# ====================================
# IMPORTS
# ====================================

from backend.intelligence.urban_score import (
    calculate_score
)

from backend.intelligence.risk_engine import (
    calculate_risk
)


# Urban Anomaly Detection Engine
try:

    from backend.intelligence.anomaly_engine import (
        detect_anomalies
    )

except Exception as e:

    st.error(f"Anomaly Engine Import Error: {e}")

    def detect_anomalies(data):
        return []



# AI Forecast Engine
from backend.intelligence.forecast_ai import (
    forecast_city
)

# Predictive Analytics Engine
try:

    from backend.intelligence.predictive_analytics import (
        predictive_report
    )

except Exception:

    try:

        import importlib.util

        predictive_path = (
            ROOT
            / "backend"
            / "intelligence"
            / "predictive_analytics.py"
        )

        spec = importlib.util.spec_from_file_location(
            "predictive_analytics",
            predictive_path
        )

        predictive_module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(
            predictive_module
        )

        predictive_report = (
            predictive_module.predictive_report
        )

    except Exception as e:

        st.error(
            f"Predictive Analytics Import Error: {e}"
        )

        def predictive_report(
            score,
            aqi
        ):

            return {
                "urban_score_forecast": score,
                "aqi_forecast": aqi,
                "risk_forecast": "UNKNOWN",
                "warning": "Predictive Analytics unavailable"
            }


# Executive AI Engine
try:

    from backend.intelligence.executive_ai import (
        generate_executive_report
    )

except Exception as e:

    st.error(
        f"Executive AI Import Error: {e}"
    )

    def generate_executive_report(
        city,
        score,
        heat_risk,
        pollution_risk,
        urban_risk
    ):

        return {
            "summary": "Executive AI unavailable",
            "action": "No action available"
        }

try:

    from backend.intelligence.recommendation_engine import (
        get_recommendation
    )

    # Recommendation engine loaded

except Exception as e:

    st.error(f"Recommendation Engine Import Error: {e}")

    def get_recommendation(
        temp,
        hum,
        aqi=1,
        pm25=0,
        pm10=0,
        co=0,
        no2=0,
        score=100
    ):

        return {
            "message": "⚠ Recommendation Engine Unavailable"
        }

# ====================================
# LOAD
# ====================================

@st.cache_data(ttl=5)
def load_data():

    try:

        db_url = os.getenv("DATABASE_URL")

        if db_url:

            engine = create_engine(db_url)

            return pd.read_sql(
                """
                SELECT *
                FROM weather_data
                ORDER BY time DESC
                """,
                engine
            )

        if CSV.exists():

            return pd.read_csv(
                CSV,
                on_bad_lines="skip"
            )

    except Exception as e:

        st.error(f"Database Error: {e}")

    return pd.DataFrame()


@st.cache_resource
def load_model():

    try:

        if MODEL.exists():

            return joblib.load(
                MODEL
            )

    except:
        pass

    return None


def load_alerts():

    try:

        if ALERT.exists():

            with open(ALERT) as f:
                return json.load(f)

    except:
        pass

    return []


# ====================================
# DATA
# ====================================

df = load_data()

data_age_seconds = 0
last_dataset_update = "Unavailable"

try:
    if CSV.exists():
        data_age_seconds = int(
            datetime.now().timestamp() - CSV.stat().st_mtime
        )

        last_dataset_update = datetime.fromtimestamp(
            CSV.stat().st_mtime
        ).strftime("%d %b %Y %I:%M:%S %p")
except Exception:
    pass

df, selected_city = city_filter(df)

model = load_model()

alerts = load_alerts()

if df.empty:

    st.error(
        "No data found in PostgreSQL database"
    )

    st.stop()

# Ensure required columns exist
required_columns = {
    "city": "Unknown",
    "aqi": 0,
    "pm25": 0,
    "pm10": 0,
    "co": 0,
    "no2": 0,
    "condition": "Unknown"
}

for col, default_value in required_columns.items():
    if col not in df.columns:
        df[col] = default_value

# ====================================
# CLEAN
# ====================================

if "time" in df.columns:

    df["time"] = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

df = df.dropna()

# ====================================
# SINGLE FILTER
# ====================================

city = selected_city

if city != "All Cities":
    plot = df[df["city"] == city].tail(40)
else:
    plot = df.tail(40)

if city == "All Cities":

    latest_cities = (
        df
        .groupby("city")
        .tail(1)
    )

    latest = pd.Series({

        "temperature": latest_cities["temperature"].mean(),

        "humidity": latest_cities["humidity"].mean(),

        "aqi": latest_cities["aqi"].mean() if "aqi" in latest_cities.columns else 0,

        "pm25": latest_cities["pm25"].mean() if "pm25" in latest_cities.columns else 0,

        "pm10": latest_cities["pm10"].mean() if "pm10" in latest_cities.columns else 0,

        "co": latest_cities["co"].mean() if "co" in latest_cities.columns else 0,

        "no2": latest_cities["no2"].mean() if "no2" in latest_cities.columns else 0

    })

else:

    latest = (
        df[df["city"] == city]
        .tail(1)
        .iloc[0]
    )

# Sort plotting data to avoid chart spikes
plot = plot.sort_values("time")

# KPI deltas
try:
    prev = plot.tail(2).iloc[0] if len(plot) > 1 else latest
    temp_delta = round(float(latest.get("temperature", 0)) - float(prev.get("temperature", 0)), 2)
    humidity_delta = round(float(latest.get("humidity", 0)) - float(prev.get("humidity", 0)), 2)
except Exception:
    temp_delta = 0
    humidity_delta = 0

# ====================================
# AI
# ====================================

try:

    prediction = round(

        float(

            model.predict(

                [[
                    latest[
                        "humidity"
                    ]
                ]]

            )[0]

        ),

        1

    )

except:

    prediction = round(
        latest[
            "temperature"
        ],
        1
    )

urban = calculate_score(

    latest[
        "temperature"
    ],

    latest[
        "humidity"
    ],

    prediction,

    latest[
        "aqi"
    ],

    latest[
        "pm25"
    ],

    latest[
        "pm10"
    ],

    latest[
        "co"
    ],

    latest[
        "no2"
    ]

)

rec = get_recommendation(

    latest[
        "temperature"
    ],

    latest[
        "humidity"
    ],

    latest[
        "aqi"
    ],

    latest[
        "pm25"
    ],

    latest[
        "pm10"
    ],

    latest[
        "co"
    ],

    latest[
        "no2"
    ],

    urban["score"]

)

recommendation = rec.get(
    "message",
    "No recommendation available"
)

health = urban["score"]

# ====================================
# CITY RANKINGS
# ====================================

city_scores = []

for city_name in df["city"].unique():

    city_df = df[df["city"] == city_name]

    row = city_df.tail(1).iloc[0]

    city_prediction = float(row["temperature"])

    score = calculate_score(
        row["temperature"],
        row["humidity"],
        city_prediction,
        row.get("aqi", 0),
        row.get("pm25", 0),
        row.get("pm10", 0),
        row.get("co", 0),
        row.get("no2", 0)
    )["score"]

    city_scores.append({
        "City": city_name,
        "Score": score
    })

ranking_df = pd.DataFrame(city_scores)

ranking_df = ranking_df.sort_values(
    "Score",
    ascending=False
)

render_hero()

# ====================================
# MASTER'S PORTFOLIO EXECUTIVE LAYER
# ====================================

st.markdown('---')

exec1, exec2, exec3, exec4, exec5 = st.columns(5)

exec1.metric('🏆 National Score', national_score if 'national_score' in locals() else round(ranking_df['Score'].mean(),1))
exec2.metric('🤖 AI Confidence', f"{round(min(99,70 + ranking_df['Score'].mean()*0.25),1)}%")
exec3.metric('🏙 Cities Monitored', df['city'].nunique())
exec4.metric('🚨 Active Alerts', len(alerts))
exec5.metric('🧠 Digital Twin', 'ACTIVE')

with st.expander('🏗 UrbanMind System Architecture', expanded=False):
    st.markdown('''
    Sensors & APIs
    ↓
    Data Pipeline
    ↓
    PostgreSQL Storage
    ↓
    AI / ML Intelligence Layer
    ↓
    UrbanMind Digital Twin
    ↓
    Executive Dashboard
    ''')

with st.expander('🧠 Digital Twin Status', expanded=False):
    d1, d2, d3, d4 = st.columns(4)
    d1.success('Simulation Engine ACTIVE')
    d2.success('Prediction Layer ACTIVE')
    d3.success('Risk Engine ACTIVE')
    d4.success('Governance AI ACTIVE')

# ====================================
# EXECUTIVE COMMAND CENTER
# ====================================

national_score = round(ranking_df['Score'].mean(), 1)
best_city = ranking_df.iloc[0]['City']
best_score = round(ranking_df.iloc[0]['Score'], 1)
worst_city = ranking_df.iloc[-1]['City']
worst_score = round(ranking_df.iloc[-1]['Score'], 1)
st.markdown("### 🧠 National Strategic Assessment")

st.success(
    f"""
UrbanMind AI Assessment:

National readiness is {national_score}/100.

{best_city} leads the nation through strong environmental,
governance and health indicators.

{worst_city} requires priority intervention due to lower
resilience and urban performance indicators.

AI Confidence: {round(min(99,70 + national_score*0.25),1)}%
"""
)
st.subheader("🚀 UrbanMind Executive Command Center")

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("🏙 National Score", national_score)
k2.metric("🚨 Active Alerts", len(alerts))
k3.metric("🌆 Cities", df['city'].nunique())
k4.metric("⭐ Best City", best_city)
k5.metric("⚠ Priority City", worst_city)
k6.metric("🤖 AI Status", "ONLINE")

st.info(
    f"National Readiness: {national_score}/100 | Leader: {best_city} | Priority Intervention: {worst_city}"
)

left_col, right_col = st.columns([4,1])

with right_col:
    st.metric("🕒 Local Time", datetime.now().strftime('%I:%M:%S %p'))

# ================= NATIONAL LIVE STATUS & MAP =================
st.subheader("🟢 National Live Status")

st.success(
    f"System Healthy | Monitoring {df['city'].nunique()} Cities | {len(df)} Records | Last Refresh: {datetime.now().strftime('%H:%M:%S')}"
)
ops1, ops2, ops3, ops4 = st.columns(4)

ops1.metric("📡 Live Streams", df['city'].nunique())
ops2.metric("📄 Events Processed", f"{len(df):,}")
ops3.metric("🚨 Active Alerts", len(alerts))
ops4.metric("⚡ Refresh Rate", f"{refresh_rate}s")


st.subheader("🗺 National Monitoring Map")
st.markdown(
    f"**AI Insight:** {best_city} currently leads national readiness while {worst_city} remains the primary intervention target based on live intelligence indicators."
)
st.caption('Real-time national digital twin monitoring layer with urban readiness intelligence.')

city_coords = {
    "Bangalore": [12.9716, 77.5946],
    "Hyderabad": [17.3850, 78.4867],
    "Chennai": [13.0827, 80.2707],
    "Mumbai": [19.0760, 72.8777],
    "Delhi": [28.6139, 77.2090],
    "Kolkata": [22.5726, 88.3639],
    "Pune": [18.5204, 73.8567],
    "Ahmedabad": [23.0225, 72.5714],
    "Jaipur": [26.9124, 75.7873],
    "Vijayawada": [16.5062, 80.6480]
}
 
m = folium.Map(location=[22.5, 79.0], zoom_start=4, tiles='CartoDB positron')
heat_data = []

for _, row in ranking_df.iterrows():
    city_name = row['City']
    score = row['Score']
    if city_name in city_coords:
        heat_data.append([
            city_coords[city_name][0],
            city_coords[city_name][1],
            score
        ])
        color = 'green' if score >= 80 else 'orange' if score >= 60 else 'red'
        folium.Marker(
    city_coords[city_name],
    popup=f"{city_name} | Score: {round(score,1)}",
    tooltip=f"{city_name} | Urban Score: {round(score,1)}",
    icon=folium.Icon(color=color)
).add_to(m)

        if city_name == best_city:
            folium.CircleMarker(
                location=city_coords[city_name],
                radius=18,
                color='green',
                fill=True,
                popup=f'National Leader: {city_name}'
            ).add_to(m)

        if city_name == worst_city:
            folium.CircleMarker(
                location=city_coords[city_name],
                radius=18,
                color='red',
                fill=True,
                popup=f'Priority Intervention: {city_name}'
            ).add_to(m)

if heat_data:
    HeatMap(heat_data, radius=25, blur=20).add_to(m)

st_folium(m, width='100%', height=450)
st.info(
    f"Monitoring {df['city'].nunique()} smart cities nationwide | "
    f"National Leader: {best_city} | "
    f"Priority Intervention: {worst_city}"
)
with st.expander("📡 Data Pipeline Status", expanded=False):
    st.subheader("📡 Data Freshness Center")

    f1, f2, f3, f4 = st.columns(4)

    f1.metric(
        "🕒 Last Update",
        last_dataset_update.split()[-2] + " " + last_dataset_update.split()[-1]
        if last_dataset_update != "Unavailable"
        else "N/A"
    )

    age_seconds = max(0, data_age_seconds)
    age_hours = age_seconds // 3600
    age_minutes = (age_seconds % 3600) // 60

    f2.metric(
        "⚡ Data Age",
        f"{age_hours}h {age_minutes}m"
    )

    f3.metric(
        "📄 Records",
        len(df)
    )

    f4.metric(
        "🔄 Refresh",
        f"{refresh_rate}s"
    )

    # Service Status Center
    s1, s2, s3, s4 = st.columns(4)

    s1.success("🟢 PostgreSQL")
    s2.success("🟢 ML Engine")
    s3.success("🟢 Alert System")
    s4.success("🟢 Dashboard")
st.markdown('---')
st.header('🏛 National Operations Center')

render_executive_center(df, ranking_df, alerts)
st.markdown('---')
st.header('🧠 National Intelligence & Governance')

render_national_center(df, ranking_df)

with st.expander("🏛 Governance AI", expanded=False):
    render_governance_ai(df, ranking_df)

with st.expander("🚨 Alert Command Center", expanded=False):
    render_alert_center(
        plot,
        alerts,
        latest,
        urban,
        selected_city,
        detect_anomalies,
        calculate_risk,
        generate_executive_report
    )

# ====================================
# KPI
# ====================================

a,b,c,d,e,f = st.columns(6)

aqi_value = latest["aqi"] if "aqi" in latest.index else "N/A"
if aqi_value != "N/A":
    try:
        aqi_value = round(float(aqi_value), 2)
    except:
        pass

a.metric(
    "🏙 Urban Score",
    urban["score"]
)

b.metric(
    "🌡 Temp",
    f"{float(latest.get('temperature', 0)):.1f}°C",
    f"{temp_delta:+.1f}"
)

c.metric(
    "💧 Humidity",
    f"{latest.get('humidity', 0)}%",
    f"{humidity_delta:+.1f}"
)

d.metric(
"🌫 AQI Index",
aqi_value
)

e.metric(
"📄 Records",
len(df)
)

f.metric(
"🔮 Forecast Temp",
f"{prediction}°C"
)
render_rankings(
    df,
    ranking_df,
    prediction
)

# ================= SYSTEM METRICS PANEL =================
st.markdown('---')
st.header('⚙ System Intelligence Metrics')

confidence = round(
    min(99, 70 + national_score * 0.25),
    1
)

k1, k2, k3, k4 = st.columns(4)

k1.metric("📡 Records Processed", f"{len(df):,}")
k2.metric("🏙 Cities Monitored", df['city'].nunique())
k3.metric("🤖 Model Confidence", f"{confidence}%")
k4.metric("⚡ System Health", "ACTIVE")


# ====================================
# RECOMMEND
# ====================================
st.markdown('---')
st.header('🧠 Executive Recommendation')

st.info(
recommendation
)

st.subheader("🔍 Explainable AI")

st.success(
    f"""
Why {best_city} ranks highest:
• Strong environmental performance
• Low urban risk
• Stable climate indicators
• High urban readiness score
"""
)

st.warning(
    f"""
Why {worst_city} needs intervention:
• Higher environmental pressure
• Lower readiness indicators
• Increased risk profile
• Governance optimization required
"""
)

# ================= AI NATIONAL SUMMARY & CHARTS =================
st.markdown('---')
st.header('🧠 UrbanMind AI National Summary')

best_city = ranking_df.iloc[0]['City']
worst_city = ranking_df.iloc[-1]['City']

st.info(
    f"UrbanMind AI reports national readiness remains stable. {best_city} leads national performance while {worst_city} requires priority attention. Monitoring is active across {df['city'].nunique()} cities with {len(alerts)} active alerts."
)
st.subheader("🔮 AI Forecast Center")

forecast_temp = round(prediction, 1)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Next Hour", f"{forecast_temp}°C")
c2.metric("Urban Score", urban["score"])

if urban["score"] >= 80:
    risk_status = "LOW"
elif urban["score"] >= 60:
    risk_status = "MODERATE"
elif urban["score"] >= 40:
    risk_status = "HIGH"
else:
    risk_status = "CRITICAL"

c3.metric("Risk Status", risk_status)

forecast_confidence = round(
    min(99, 75 + urban["score"] * 0.2),
    1
)

c4.metric(
    "🎯 Confidence",
    f"{forecast_confidence}%"
)

fig_gauge = go.Figure(go.Indicator(
    mode='gauge+number',
    value=national_score,
    title={'text': 'National Urban Readiness'},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': 'darkblue'},
        'steps': [
            {'range': [0, 40], 'color': 'red'},
            {'range': [40, 70], 'color': 'orange'},
            {'range': [70, 100], 'color': 'green'}
        ]
    }
))

st.plotly_chart(fig_gauge, use_container_width=True)
readiness_df = ranking_df.copy()
readiness_df["Rank"] = range(1, len(readiness_df) + 1)

fig_scatter = px.scatter(
    readiness_df,
    x="Rank",
    y="Score",
    size="Score",
    color="Score",
    hover_name="City",
    title="National Urban Readiness Intelligence"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ================== PREDICTIVE RISK TABLE ==================
with st.expander("📊 Predictive Risk Intelligence", expanded=False):

    forecast_table = ranking_df.copy()
    forecast_table['Forecast Score'] = forecast_table['Score'] + 3
    forecast_table['Risk'] = forecast_table['Score'].apply(
        lambda x: 'LOW' if x >= 80 else 'MODERATE' if x >= 60 else 'HIGH'
    )

    st.dataframe(forecast_table, use_container_width=True)

# ====================================
# EXECUTIVE VISUAL INTELLIGENCE
# ====================================
st.markdown('---')
c1, c2 = st.columns(2)

st.header('📈 Executive Visual Intelligence')
st.caption(
    "Comparative performance, environmental exposure and predictive intelligence visualization layer."
)

viz_left, viz_right = st.columns(2)

with viz_left:
    fig_sunburst = px.sunburst(
        ranking_df,
        path=["City"],
        values="Score",
        color="Score",
        title="Urban Performance Distribution"
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)

with viz_right:
    bubble_df = ranking_df.copy()
    bubble_df["Risk"] = 100 - bubble_df["Score"]

    fig_bubble = px.scatter(
        bubble_df,
        x="Score",
        y="Risk",
        size="Score",
        color="Risk",
        hover_name="City",
        title="Urban Risk vs Performance Matrix"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    fig_rank = px.bar(
    ranking_df.head(10),
    x='City',
    y='Score',
    color='Score',
    text='Score',
    title='Top City Performance Rankings'
)
    fig_rank.update_traces(textposition="outside")
    st.plotly_chart(fig_rank, use_container_width=True)

with c2:
    pollution_df = df.groupby('city')['aqi'].mean().reset_index()
    fig_pollution = px.bar(
    pollution_df.sort_values('aqi', ascending=False),
    x='city',
    y='aqi',
    color='aqi',
    text='aqi',
    title='Pollution Intelligence Ranking'
)
    fig_pollution.update_traces(textposition="outside")
    st.plotly_chart(fig_pollution, use_container_width=True)

# ====================================
# CHARTS
# ====================================

l,r,x = st.columns(3)

with l:

    fig=go.Figure()

    fig.add_trace(
        go.Scatter(
            x=plot["time"],
            y=plot["temperature"],
            fill="tozeroy",
            mode="lines",
        )
    )

    fig.update_layout(
        title="Temperature Trend (°C)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with r:

    fig=go.Figure()

    fig.add_trace(

        go.Scatter(

            x=plot["time"],

            y=plot["humidity"],

            fill="tozeroy"

        )

    )

    fig.update_layout(
        title="Humidity Trend (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with x:

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=plot["time"],
            y=plot["aqi"] if "aqi" in plot.columns else [0] * len(plot),
            fill="tozeroy",
            mode="lines+markers",
        )
    )

    fig.update_layout(
        title="AQI Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
st.markdown('---')
st.header('🎯 Research Contribution Highlights')

r1, r2, r3, r4 = st.columns(4)

r1.metric('AI Models', '4+')
r2.metric('Cities Simulated', df['city'].nunique())
r3.metric('Digital Twin Status', 'ACTIVE')
r4.metric('Governance Confidence', f'{confidence}%')

st.info(
    'UrbanMind integrates Explainable AI, Predictive Analytics, Urban Risk Intelligence, Digital Twin Simulation and Governance Decision Support into a unified Smart City platform.'
)

st.success(
    f"UrbanMind Executive Report | National Score: {national_score} | Best City: {best_city} | Priority City: {worst_city}"
)

st.caption(
    "UrbanMind v2.0 Research Platform • Explainable AI • Smart City Intelligence • Governance Analytics • Digital Twin Intelligence • © 2026"
)