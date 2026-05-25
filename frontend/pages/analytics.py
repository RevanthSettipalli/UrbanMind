import streamlit as st

if "next_page" in st.session_state:
    page = st.session_state.pop("next_page")
    st.switch_page(f"pages/{page}.py")
