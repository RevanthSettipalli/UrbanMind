import streamlit as st


def require_login():
    if not st.session_state.get("logged_in", False):

        st.warning("🔐 Login Required")

        st.info(
            "Please open the Login page from the sidebar."
        )

        st.stop()


def logout():
    st.session_state.clear()

    st.rerun()