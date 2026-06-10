import streamlit as st

def require_login():
    # Temporary bypass for local debugging
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = True

    return True


def logout():
    st.session_state.clear()
    st.rerun()