import streamlit as st


def require_login():
    if not st.session_state.get("logged_in", False):
        st.warning("🔐 Login Required")

        st.switch_page(
            "pages/login.py"
        )

        st.stop()


def logout():
    st.session_state.clear()

    st.switch_page(
        "pages/login.py"
    )