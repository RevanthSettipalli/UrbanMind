

import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


CITY_COORDINATES = {
    "Delhi": [28.61, 77.20],
    "Mumbai": [19.07, 72.87],
    "Hyderabad": [17.38, 78.48],
    "Chennai": [13.08, 80.27],
    "Bangalore": [12.97, 77.59],
    "Kolkata": [22.57, 88.36],
    "Vijayawada": [16.50, 80.64],
    "Pune": [18.52, 73.85],
    "Ahmedabad": [23.02, 72.57],
    "Jaipur": [26.91, 75.78]
}


def render_digital_twin_panel(rank, selected_city, best_city, worst_city):
    try:
        st.subheader("🗺 Urban Digital Twin")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Cities Mapped",
            len(rank)
        )

        c2.metric(
            "National Leader",
            best_city
        )

        c3.metric(
            "Priority City",
            worst_city
        )

        rank = rank.copy()

        rank["risk"] = rank.apply(
            lambda r: (
                "🔥 Heat Risk"
                if r["temperature"] >= 40
                else (
                    "🌧 High Humidity"
                    if r["humidity"] >= 80
                    else "✅ Stable"
                )
            ),
            axis=1,
        )

        rank["color"] = rank["score"].apply(
            lambda x: "green" if x >= 90 else ("orange" if x >= 75 else "red")
        )

        m = folium.Map(
            location=[21, 79],
            zoom_start=5,
            tiles="CartoDB positron"
        )

        map_data = (
            rank
            if selected_city == "All Cities"
            else rank[rank["city"] == selected_city]
        )

        heat_data = []

        for _, r in map_data.iterrows():
            city_name = str(r["city"])

            if city_name not in CITY_COORDINATES:
                continue

            lat, lon = CITY_COORDINATES[city_name]

            heat_data.append([lat, lon, float(r["score"])] )

            recommendation = (
                "Heat Risk Increasing"
                if r["temperature"] > 40
                else (
                    "High Humidity Alert"
                    if r["humidity"] > 80
                    else "Conditions Stable"
                )
            )

            folium.CircleMarker(
                location=[lat, lon],
                radius=18,
                fill=True,
                fill_opacity=0.9,
                color=r["color"],
                fill_color=r["color"],
                tooltip=city_name,
                popup=f"""
🏙 {city_name}
⭐ Score: {r['score']:.0f}
🌡 Temp: {r['temperature']:.1f}°C
💧 Humidity: {r['humidity']:.1f}%
⚠ Recommendation: {recommendation}
"""
            ).add_to(m)

            if city_name == best_city:
                folium.Marker([lat, lon], tooltip="🏆 National Leader").add_to(m)

            if city_name == worst_city:
                folium.Marker([lat, lon], tooltip="⚠ Priority Intervention").add_to(m)

        if heat_data:
            HeatMap(
                heat_data,
                radius=25,
                blur=20,
                min_opacity=0.4
            ).add_to(m)

        st.success(
            "Digital Twin Network Active • Real-time Urban Monitoring Enabled"
        )

        st_folium(
            m,
            height=450,
            use_container_width=True
        )

        st.download_button(
            "📥 Export Digital Twin Data",
            rank.to_csv(index=False),
            "digital_twin_data.csv",
            "text/csv"
        )
    except Exception as e:
        st.error(f"Digital Twin Error: {e}")