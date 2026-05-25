import streamlit as st


def require_login():

    if st.session_state.get("logged_in"):
        return True

    if st.session_state.get("user"):
        st.session_state["logged_in"] = True
        return True

    st.switch_page("pages/login.py")


def logout():

    keep = {}

    st.session_state.clear()

    st.session_state.update(keep)

    st.switch_page("pages/login.py")