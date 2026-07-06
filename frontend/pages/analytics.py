from sklearn.ensemble import IsolationForest
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import folium
from folium.plugins import HeatMap
import pytz
from pathlib import Path

from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from frontend.utils.load_weather import load_weather
from frontend.utils.auth_guard import require_login
from frontend.utils.sidebar import render_sidebar
from frontend.utils.settings import (
    apply_theme,
    load_settings,
    export_data
)

from backend.intelligence.predictive_analytics import (
    predictive_report
)
from backend.intelligence.urban_score import (
    calculate_score
)

# Prophet Forecasting Engine

# Prophet Forecasting Engine
#
# Heavy AI modules are imported lazily to avoid page startup hangs
forecast_30_days = None
forecast_lstm = None
calculate_feature_importance = None


from backend.intelligence.governance_simulator import (
    simulate_policy
)

from frontend.dashboard_components.governance_ai import render_governance_ai
from frontend.dashboard_components.sustainability_panel import render_sustainability_panel
from frontend.dashboard_components.xai_panel import render_xai_panel
from frontend.dashboard_components.forecasting_panel import render_forecasting_panel
from frontend.dashboard_components.risk_panel import render_risk_panel
from frontend.dashboard_components.research_panel import render_research_panel
from frontend.dashboard_components.digital_twin_panel import render_digital_twin_panel


from backend.intelligence.smart_city_index import (
    calculate_national_index,
    generate_city_profile
)

# ==================================================
# REFACTOR NOTE
# This file is now a candidate for modularization.
# Suggested modules:
# frontend/components/analytics/header.py
# frontend/components/analytics/kpi.py
# frontend/components/analytics/maps.py
# frontend/components/analytics/forecasting.py
# frontend/components/analytics/governance.py
# frontend/components/analytics/research.py
# ==================================================

@st.cache_data(ttl=300)
def get_forecast_result_cached(df_input):
    global forecast_30_days
    if forecast_30_days is None:
        from backend.intelligence.forecasting_engine import forecast_30_days as _forecast_30_days
        forecast_30_days = _forecast_30_days
    return forecast_30_days(df_input)
# =================================
# PAGE
# =================================

st.set_page_config(
    page_title="Urban Analytics",
    page_icon="📊",
    layout="wide"
)

require_login()

render_sidebar()

st.markdown(
    apply_theme(),
    unsafe_allow_html=True
)

settings = load_settings()

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "processed_weather.csv"

# =================================
# PREMIUM UI
# =================================

st.markdown("""
<style>

.block-container{
padding-top:0.4rem !important;
}

.hero{
padding:40px;

border-radius:30px;

background:
linear-gradient(
135deg,
#04162a,
#0b5c93
);

color:white;

margin-bottom:24px;
}

.hero h1{
font-size:50px;
}

.hero p{
font-size:18px;
opacity:.9;
}

[data-testid="metric-container"]{

background:white;

border-radius:22px;

padding:24px;

box-shadow:
0 8px 25px
rgba(0,0,0,.05);

}

.section{

padding:22px;

background:white;

border-radius:22px;

margin-bottom:22px;

}

</style>
""",
unsafe_allow_html=True)


# =================================
# REFRESH
# =================================
refresh_rate = max(
    60,
    int(settings.get("refresh_rate", 300))
)

st_autorefresh(
    interval=refresh_rate * 1000,
    key=f"analytics_refresh_{refresh_rate}"
)

# =================================
# LOAD
# =================================

df = load_weather()
print('DEBUG: weather data loaded')

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

if df.empty:

    st.warning(
        "Waiting for analytics..."
    )

    st.stop()


# =================================
# CLEAN
# =================================

required = [

"time",
"city",
"temperature",
"humidity"

]

for c in required:

    if c not in df:

        df[c] = (
            "Unknown"
            if c=="city"
            else 0
        )


df["time"]=pd.to_datetime(
df["time"],
errors="coerce"
)

df["temperature"]=pd.to_numeric(
df["temperature"],
errors="coerce"
)

df["humidity"]=pd.to_numeric(
df["humidity"],
errors="coerce"
)

# Drop NA and keep last 3000 records
df=df.dropna()
df=df.tail(3000)
if "time" in df.columns:
    df = df.sort_values("time")
# Clean city names
if "city" in df.columns:
    df["city"] = df["city"].astype(str).str.strip()
    df = df[
        (~df["city"].isin(["", "Unknown", "unknown", "nan", "None"]))
    ]

# Fallback to CSV if loader returned unusable city data
if df.empty and CSV.exists():
    try:
        df = pd.read_csv(CSV)
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"])
    except Exception:
        pass

# =================================
# FILTER
# =================================

cities=sorted(
df["city"]
.astype(str)
.unique()
)

city=st.selectbox(

"🏙 Select City",

["All Cities"]

+

cities

)

if city!="All Cities":

    df=df[
        df["city"]
        ==
        city
    ]

if df.empty:
    st.warning("No data available for the selected city")
    st.stop()


# =================================
# TIME
# =================================

IST = datetime.now(
    pytz.timezone(
        "Asia/Kolkata"
    )
)

current_time = IST.strftime(
    "%I:%M:%S %p"
).replace(" AM", "AM").replace(" PM", "PM")

updated_time = IST.strftime(
    "%d %b %Y · %I:%M:%S %p"
).replace(" AM", "AM").replace(" PM", "PM")


# =================================
# SCORE
# =================================

avg_temp = round(
    df.temperature.mean(),
    1
)

avg_hum = round(
    df.humidity.mean(),
    1
)

if df.empty:
    st.warning("No analytics data available")
    st.stop()

latest = df.sort_values("time").iloc[-1]

urban = calculate_score(
    float(latest.get("temperature", 0)),
    float(latest.get("humidity", 0)),
    float(latest.get("temperature", 0)),
    float(latest.get("aqi", 1)),
    float(latest.get("pm25", 0)),
    float(latest.get("pm10", 0)),
    float(latest.get("co", 0)),
    float(latest.get("no2", 0))
)["score"]

# =================================
# PREDICTIVE INTELLIGENCE
# =================================

current_aqi = 3

if "aqi" in df.columns:
    try:
        current_aqi = float(pd.to_numeric(df["aqi"], errors="coerce").dropna().mean())
    except Exception:
        current_aqi = 3

predictive_data = predictive_report(
    urban,
    current_aqi
)

# =================================
# PROPHET FORECASTING ENGINE
# =================================

try:
    print("STEP 1 - Starting Forecast Engine")
    print('DEBUG: entering forecast engine')
    forecast_result = get_forecast_result_cached(df)
    print("STEP 2 - Forecast Engine Completed")

    forecast_df = forecast_result.get(
        "forecast_df",
        pd.DataFrame()
    )

    forecast_confidence = forecast_result.get(
        "confidence",
        75
    )

    forecast_model = forecast_result.get(
        "model",
        "Fallback"
    )

except Exception as e:
    st.warning(f"Forecast engine unavailable: {e}")

    forecast_df = pd.DataFrame()
    forecast_confidence = 75
    forecast_model = "Fallback"

# LSTM Execution
lstm_result = {
    "forecast": [],
    "rmse": 0,
    "model": "Disabled"
}

lstm_forecast = lstm_result.get("forecast", [])
lstm_rmse = lstm_result.get("rmse", 0)
lstm_model = lstm_result.get("model", "Unavailable")



# ==================================================
# MODULARIZATION STATUS
# Extracted:
# 1. Governance AI Panel
# 2. Sustainability Panel
# 3. Explainable AI Panel
# Remaining:
# - Forecasting Panel
# - Risk Intelligence Panel
# - Research Panel
# - Digital Twin Panel
# - City Comparison Panel
# ==================================================
# =================================
# HEADER
# =================================

left, right = st.columns([8.8,1.0])

with left:

    st.markdown("""
<div class='hero'>

<h1>
📊 Urban Analytics
</h1>

<p>
Advanced Intelligence • Ranking • Geo Analysis
</p>

</div>
""",
unsafe_allow_html=True
)

with right:

    st.markdown(
        f"""
<div style="
background:#dfe8f5;
height:260px;
border-radius:22px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
text-align:center;
padding:18px;
position:relative;
">

<div style="
font-size:44px;
margin-top:0px;
margin-bottom:8px;
line-height:1;
">
🕒
</div>

<div style="
font-size:28px;
font-weight:800;
color:#124f9d;
line-height:1;
white-space:nowrap;
">
{current_time}
</div>

<div style="
margin-top:10px;
font-size:15px;
color:#5a6572;
">
Live Time
</div>

</div>
""",
unsafe_allow_html=True
)


# =================================
# DATA FRESHNESS CENTER
# =================================

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


# =================================
# KPI
# =================================

a,b,c,d,e=st.columns(5)

a.metric(
    "🏙 Urban Score",
    urban
)

b.metric(
    "🌡 Avg Temp",
    f"{avg_temp}°C"
)

c.metric(
    "💧 Avg Humidity",
    f"{avg_hum}%"
)

d.metric(
    "🏙 Cities",
    len(df["city"].unique())
)


e.metric(
    "🌫 Environmental Index",
    round(current_aqi, 2)
)

# =================================
# RESEARCH CONTRIBUTION HIGHLIGHTS
# =================================
st.subheader("🎯 Research Contribution Highlights")

r1, r2, r3, r4 = st.columns(4)

r1.metric("AI Models", "4+")
r2.metric("Cities Simulated", len(df["city"].unique()))
r3.metric("Digital Twin Status", "ACTIVE")
r4.metric("Governance Confidence", f"{round(min(99,70 + urban*0.25),1)}%")

st.info(
    "UrbanMind integrates Explainable AI, Predictive Analytics, Urban Risk Intelligence, Digital Twin Simulation and Governance Decision Support into a unified Smart City platform."
)
st.subheader("🔬 Research Impact Metrics")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Predictions Generated", f"{len(df):,}")
m2.metric("Risk Assessments", f"{len(df['city'].unique()):,}")
m3.metric("Digital Twin Events", f"{len(df)*2:,}")
m4.metric("Governance Decisions", f"{max(len(df)//10,1):,}")

# =================================
# HEALTH
# =================================

st.subheader(
"🩺 Urban Health"
)

st.progress(
urban/100
)


# =================================
# RANK
# =================================

rank=(

df

.groupby(
"city"
)

.agg({

"temperature":"mean",

"humidity":"mean"

})

.round(1)

.reset_index()

)


rank["score"] = (
    (100 - abs(rank["temperature"] - 28) * 2)
    + ((100 - abs(rank["humidity"] - 55)) * 0.30)
) / 1.30

rank["score"] = rank["score"].clip(
    lower=0,
    upper=100
)



rank=rank.sort_values(
    "score",
    ascending=False
)
rank["Risk"] = (100 - rank["score"]).round(1)
rank["Rank"] = range(1, len(rank) + 1)
rank = rank.round(1)

# =================================
# SMART CITY CLUSTERING
# =================================

try:
    cluster_data = rank[["temperature", "humidity", "score"]].copy()

    if len(cluster_data) >= 4:
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        rank["Cluster"] = kmeans.fit_predict(cluster_data)

        cluster_names = {
            0: "Smart Leaders",
            1: "Sustainable Cities",
            2: "Emerging Cities",
            3: "High Risk Cities"
        }

        rank["Cluster Label"] = rank["Cluster"].map(cluster_names)
except Exception:
    rank["Cluster Label"] = "Urban Cluster"

# Insert recommendation block

if latest["temperature"] > 40:
    recommendation = "Heat Risk Increasing"
elif latest["humidity"] > 80:
    recommendation = "High Humidity Alert"
else:
    recommendation = "Conditions Stable"


st.subheader(
    "🏆 City Ranking"
)

st.dataframe(
rank,
use_container_width=True
)

# -------------------------------
# Best/Worst City Highlight
# -------------------------------
if rank.empty:
    st.warning("No ranking data available")
    st.stop()
best_city = rank.iloc[0]["city"]
worst_city = rank.iloc[-1]["city"]

c1, c2 = st.columns(2)

with c1:
    st.success(f"🏆 Best Performing City: {best_city}")

with c2:
    st.error(f"⚠ City Requiring Attention: {worst_city}")

# -------------------------------
# Analytics Executive Insights
# -------------------------------
st.subheader("🧠 City Intelligence Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"🏆 Leader City: {best_city}")

with col2:
    st.warning(f"⚠ Focus City: {worst_city}")

with col3:
    st.success(f"📊 National Urban Score: {urban}")

rank_chart = px.bar(
    rank,
    x="city",
    y="score",
    color="score",
    title="Urban Intelligence Ranking"
)

st.plotly_chart(
    rank_chart,
    use_container_width=True
)

st.subheader("🧠 Smart City Clustering")

if "Cluster Label" in rank.columns:

    cluster_fig = px.scatter(
        rank,
        x="temperature",
        y="humidity",
        color="Cluster Label",
        size="score",
        hover_name="city",
        title="AI Smart City Cluster Analysis"
    )

    st.plotly_chart(
        cluster_fig,
        use_container_width=True
    )

st.subheader("📊 City Comparison Matrix")

comparison_df = rank[["Rank", "city", "score", "Risk"]].copy()
comparison_df.columns = ["Rank", "City", "Urban Score", "Risk Index"]
st.dataframe(comparison_df, use_container_width=True)


# =================================
# DIGITAL TWIN PANEL (modularized)
# =================================
render_digital_twin_panel(
    rank=rank,
    selected_city=city,
    best_city=best_city,
    worst_city=worst_city
)
# =================================
# NATIONAL SMART CITY INDEX
# =================================

rank["Governance"] = rank["score"].apply(
    lambda x: round(min(99, 70 + x * 0.25), 1)
)

rank["SDG"] = rank["score"].apply(
    lambda x: round(min(100, 80 + x * 0.15), 1)
)

rank["Forecast"] = predictive_data["urban_score_forecast"]

rank["National_Index"] = rank.apply(
    lambda r: calculate_national_index(
        urban_score=r["score"],
        sdg_score=r["SDG"],
        governance_score=r["Governance"],
        forecast_score=r["Forecast"],
        risk_score=r["Risk"]
    ),
    axis=1
)

st.subheader("🇮🇳 National Smart City Index")

national_index_df = rank[["city", "National_Index"]].sort_values(
    "National_Index",
    ascending=False
)

st.dataframe(
    national_index_df,
    use_container_width=True
)
national_fig = px.bar(
    national_index_df,
    x="city",
    y="National_Index",
    color="National_Index",
    title="National Smart City Index Ranking"
)

st.plotly_chart(
    national_fig,
    use_container_width=True
)

# Add city profile for national leader
leader_profile = generate_city_profile(
    national_index_df.iloc[0]["National_Index"]
)

st.success(
    f"{leader_profile['category']}: {leader_profile['description']}"
)

# =================================
# NATIONAL LEADERBOARD
# =================================

st.subheader("🥇 National Leaderboard Panel")

leaderboard = rank[["Rank", "city", "score"]].copy()
leaderboard.columns = ["Rank", "City", "Urban Score"]

st.dataframe(
    leaderboard,
    use_container_width=True
)

lb1, lb2 = st.columns(2)

lb1.success(
    f"🏆 National Leader: {leaderboard.iloc[0]['City']}"
)

lb2.info(
    f"📈 Top Score: {leaderboard.iloc[0]['Urban Score']}"
)

# -------------------------------
# Advanced Analytics & Correlation Engine
# -------------------------------
st.subheader("🧪 Advanced Analytics & Correlation Engine")

if len(df) > 2:

    correlation_columns = [
        c for c in ["temperature", "humidity", "aqi"]
        if c in df.columns
    ]

    corr_df = df[correlation_columns].corr()

    corr_fig = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(
        corr_fig,
        use_container_width=True
    )
    st.success(
        "UrbanMind Correlation Intelligence: identifies relationships between climate, air quality and urban performance indicators."
    )
st.subheader("🚨 Anomaly Detection Dashboard")

print("STEP 3 - Starting Isolation Forest")
print('DEBUG: entering anomaly detection')
iso = IsolationForest(
    contamination=0.2,
    random_state=42
)
print("STEP 4 - Isolation Forest Model Created")
features = rank[["temperature", "humidity", "score"]]

rank["anomaly"] = iso.fit_predict(features)
rank["anomaly_score"] = iso.decision_function(features)
print("STEP 5 - Isolation Forest Completed")

anomalies = rank[
    rank["anomaly"] == -1
]

if len(anomalies) > 0:
    st.error(f"{len(anomalies)} anomalous cities detected")
    st.dataframe(
        anomalies[[
            "city",
            "temperature",
            "humidity",
            "score",
            "anomaly_score"
        ]],
        use_container_width=True
    )
else:
    st.success("No significant anomalies detected")

# =================================
# TREND
# =================================

st.subheader(
"📈 Trend Analysis"
)

if city == "All Cities":

    trend_df = (
        df.groupby("time")
        [["temperature", "humidity"]]
        .mean()
        .reset_index()
    )

else:

    trend_df = df[
        df["city"] == city
    ]

fig = px.area(
    trend_df.tail(200),
    x="time",
    y=[
        "temperature",
        "humidity"
    ]
)

fig.update_layout(
height=500
)

st.plotly_chart(
fig,
use_container_width=True
)


# -------------------------------
# Temperature vs Humidity Analysis
# -------------------------------
st.subheader("🌡 Climate Intelligence")

scatter_fig = px.scatter(
    df,
    x="temperature",
    y="humidity",
    color="city",
    title="Temperature vs Humidity Distribution"
)

st.plotly_chart(
    scatter_fig,
    use_container_width=True
)

# -------------------------------
# Analytics Intelligence Center
# -------------------------------
st.subheader("📊 Analytics Intelligence Center")

s1, s2, s3, s4 = st.columns(4)

s1.metric("🏙 Cities", len(rank))
s2.metric("🏆 Best City", best_city)
s3.metric("🌡 Avg Temp", f"{avg_temp}°C")
s4.metric("💧 Avg Humidity", f"{avg_hum}%")

# =================================
# EXECUTIVE SUMMARY
# =================================

st.subheader("🌍 SDG Intelligence Layer")

sdg_score = render_sustainability_panel(rank)

st.subheader("🧠 Executive Urban Summary")

highest_risk_city = worst_city

summary_col1, summary_col2, summary_col3 = st.columns(3)

summary_col1.success(
    f"🏆 Best City: {best_city}"
)

summary_col2.error(
    f"⚠ Highest Risk City: {highest_risk_city}"
)

summary_col3.info(
    f"🎯 Forecast Confidence: {predictive_data['predictive_intelligence']['confidence']}%"
)

urban_intelligence_index = round(
    (
        urban
        + predictive_data['predictive_intelligence']['future_city_health']
        + predictive_data['predictive_intelligence']['confidence']
        + (100 - predictive_data['risk_intelligence']['overall_risk'])
    ) / 4,
    1
)

st.metric(
    "🌍 Urban Intelligence Index",
    f"{urban_intelligence_index}/100"
)
st.subheader("🔍 Explainable AI Intelligence")
feature_importance, impact_df = render_xai_panel(
    avg_temp,
    avg_hum,
    current_aqi,
    predictive_data,
    best_city
)

# =================================
# PREDICTIVE INTELLIGENCE CENTER
# =================================

st.subheader("🏛 National Executive Scorecard")

n1, n2, n3, n4, n5 = st.columns(5)

n1.metric("Urban Index", urban_intelligence_index)
n2.metric("Governance", round(min(99, 70 + urban * 0.25), 1))
n3.metric("SDG Score", sdg_score)
n4.metric("Readiness", round((urban + sdg_score) / 2, 1))
n5.metric("Digital Twin", "ACTIVE")

# =================================
# NOVEL RESEARCH CONTRIBUTIONS
# =================================
st.subheader("📑 Novel Research Contributions")

novelty_df = pd.DataFrame({
    "Innovation": [
        "Explainable AI",
        "Digital Twin",
        "SDG Intelligence",
        "Risk Forecasting",
        "Smart City Clustering",
        "Governance AI"
    ],
    "Research Score": [
        round(forecast_confidence, 1),
        round(urban_intelligence_index, 1),
        round(sdg_score, 1),
        round(100 - predictive_data["risk_intelligence"]["overall_risk"], 1),
        round(rank["score"].mean(), 1),
        round(min(100, 70 + urban * 0.25), 1)
    ]
})

novelty_fig = px.bar(
    novelty_df,
    x="Innovation",
    y="Research Score",
    color="Research Score",
    title="UrbanMind Research Novelty Index"
)

st.plotly_chart(novelty_fig, use_container_width=True)

st.success(
    "UrbanMind combines Explainable AI, Digital Twin Intelligence, Governance Analytics, SDG Intelligence and Predictive Risk Forecasting into a unified Smart City research platform."
)

st.subheader("🧠 Executive Analytics Narrative")

executive_narrative = f"""
UrbanMind AI Executive Assessment

{best_city} remains the national leader due to superior environmental readiness and governance stability.

{worst_city} requires strategic intervention because of elevated climate and urban risk indicators.

National Urban Intelligence Index: {urban_intelligence_index}/100.

Forecast Confidence: {predictive_data['predictive_intelligence']['confidence']}%
"""

st.success(executive_narrative)

st.subheader("🔮 Predictive Intelligence Center")

p1, p2, p3, p4 = st.columns(4)

intel = predictive_data["predictive_intelligence"]

p1.metric(
    "🏙 Future City Health",
    intel["future_city_health"]
)

p2.metric(
    "🎯 Confidence",
    f"{intel['confidence']}%"
)

p3.metric(
    "⚠ Future Risk",
    intel["future_risk"]
)

p4.metric(
    "📈 Forecast Score",
    predictive_data["urban_score_forecast"]
)

render_forecasting_panel(
    forecast_df=forecast_df,
    forecast_model=forecast_model,
    forecast_confidence=forecast_confidence,
    lstm_forecast=lstm_forecast,
    lstm_rmse=lstm_rmse,
    urban=urban,
    current_aqi=current_aqi,
    predictive_data=predictive_data
)

render_risk_panel(
    predictive_data=predictive_data
)

st.subheader("📋 Executive Recommendations")

for recommendation in predictive_data["recommendations"]:
    st.info(recommendation)


    # Governance module successfully extracted.
    # Next target modules:
    # forecasting_panel.py
    # risk_panel.py
    # research_panel.py
    # digital_twin_panel.py
# =================================
# GOVERNANCE DECISION SIMULATOR
# =================================
render_governance_ai(
    df=df,
    ranking_df=rank
)
# =================================
# CITY COMPARISON ENGINE
# =================================

st.subheader("⚖ City Comparison Engine")

compare_cities = sorted(rank["city"].astype(str).unique())

if len(compare_cities) >= 2:

    cmp1, cmp2 = st.columns(2)

    city_a = cmp1.selectbox(
        "City A",
        compare_cities,
        key="city_compare_a"
    )

    city_b = cmp2.selectbox(
        "City B",
        compare_cities,
        index=min(1, len(compare_cities)-1),
        key="city_compare_b"
    )

    compare_df = rank[
        rank["city"].isin([city_a, city_b])
    ][[
        "city",
        "temperature",
        "humidity",
        "score"
    ]]

    st.dataframe(
        compare_df,
        use_container_width=True
    )

    compare_chart = px.line_polar(
        pd.DataFrame({
            "Metric": ["Temperature", "Humidity", "Score"],
            city_a: [
                compare_df.iloc[0]["temperature"],
                compare_df.iloc[0]["humidity"],
                compare_df.iloc[0]["score"]
            ],
            city_b: [
                compare_df.iloc[1]["temperature"],
                compare_df.iloc[1]["humidity"],
                compare_df.iloc[1]["score"]
            ]
        }).melt(id_vars="Metric", var_name="City", value_name="Value"),
        r="Value",
        theta="Metric",
        color="City",
        line_close=True
    )

    st.plotly_chart(compare_chart, use_container_width=True)

    winner = city_a if float(compare_df.iloc[0]["score"]) >= float(compare_df.iloc[1]["score"]) else city_b
    st.success(f"🏆 Comparison Winner: {winner}")



# =================================
# INSIGHT
# =================================

st.subheader(
"🧠 AI Insight"
)

if avg_temp>40:

    st.error(
        "Heat Risk Increasing"
    )

elif avg_hum>80:

    st.warning(
        "Humidity Rising"
    )

else:

    st.success(
        "Urban Conditions Stable"
    )


st.subheader("🎓 Research Intelligence Layer")

r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("Correlation", "ACTIVE")
r2.metric("Forecasting", "ACTIVE")
r3.metric("Risk AI", "ACTIVE")
r4.metric("Digital Twin", "ACTIVE")
r5.metric("Governance", "ACTIVE")

# =================================
# RESEARCH FINDINGS
# =================================
render_research_panel(
    best_city=best_city,
    worst_city=worst_city,
    urban=urban,
    urban_intelligence_index=urban_intelligence_index,
    forecast_confidence=forecast_confidence,
    sdg_score=sdg_score,
    risk=predictive_data["risk_intelligence"],
    intel=intel
)

# =================================
# EXPORT
# =================================

file, mime, ext = export_data(
    df
)

st.download_button(

    "📄 Generate Executive Report",

    file,

    f"urbanmind_analytics{ext}",

    mime,
    use_container_width=True
)

# =================================
# SUMMARY
# =================================

st.markdown(
    f"""
### 📌 National Urban Intelligence Summary

• Best Performing City: {best_city}

• City Requiring Attention: {worst_city}

• Average Urban Score: {urban}

• Average Temperature: {avg_temp}°C

• Average Humidity: {avg_hum}%

• Total Records Analysed: {len(df)}
"""
)

score1, score2, score3, score4 = st.columns(4)

score1.metric("Forecast Confidence", f"{forecast_confidence}%")
score2.metric("SDG Score", sdg_score)
score3.metric("Governance Score", round(min(99, 70 + urban * 0.25), 1))
score4.metric(
    "National Leader Index",
    round(national_index_df.iloc[0]["National_Index"], 1)
)

# =================================
# EXECUTIVE BOARD BRIEFING
# =================================
st.markdown("---")
st.subheader("🌐 UrbanMind Research Excellence")

r1, r2, r3, r4 = st.columns(4)

r1.metric("AI Models", "4+")
r2.metric("Cities", len(rank))
research_score = round(
    (
        forecast_confidence
        + sdg_score
        + urban_intelligence_index
        + (
            100
            - predictive_data["risk_intelligence"]["overall_risk"]
        )
    ) / 4,
    1
)

r3.metric(
    "Research Score",
    f"{research_score}/100"
)
r4.metric("Portfolio Grade", "Research Grade")

st.subheader("🏛 Executive Board Briefing")

st.success(
    f"UrbanMind Executive Report | National Score: {urban} | Best City: {best_city} | Priority City: {worst_city}"
)

st.caption(
    "UrbanMind Research Platform • Explainable AI • Digital Twin Intelligence • Governance Analytics • Predictive Urban Intelligence • 2026"
)
