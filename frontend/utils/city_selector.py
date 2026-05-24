import streamlit as st


def city_filter(df):

    if "city" not in df.columns:
        df["city"] = "Vijayawada"

    cities = ["All Cities"]

    cities += sorted(
        df["city"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected = st.selectbox(
        "🏙 Select City",
        cities,
        key=f"city_{st.session_state.get('page','main')}"
    )

    if selected != "All Cities":

        filtered = df[
            df["city"] == selected
        ]

    else:
        filtered = df

    return filtered, selected
