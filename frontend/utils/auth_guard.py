import streamlit as st


def require_login():

    if st.session_state.get("logged_in"):
        return True

    if st.session_state.get("user"):
        st.session_state["logged_in"] = True
        return True

    st.switch_page("pages/login.py")
    st.stop()


def logout():
    st.session_state.clear()
    st.switch_page("pages/login.py")
    st.stop()