import streamlit as st
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader


st.set_page_config(
    page_title="UrbanMind Login",
    layout="centered"
)


with open(
    "frontend/auth.yaml"
) as file:

    config = yaml.load(
        file,
        Loader=SafeLoader
    )


authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)


authenticator.login()


if st.session_state.get(
    "authentication_status"
):

    st.success(
        "Login Successful"
    )

    st.switch_page(
    "pages/dashboard.py"
)


elif st.session_state.get(
    "authentication_status"
) is False:

    st.error(
        "Wrong Username / Password"
    )


else:

    st.warning(
        "Enter Login Credentials"
    )