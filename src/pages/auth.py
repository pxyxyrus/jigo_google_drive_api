import streamlit as st
from src.google_helper import *

st.title("Google Drive OAuth2 with Streamlit")

if 'credentials' not in st.session_state:
    st.session_state['credentials'] = None

if st.session_state['credentials'] is None:
    flow = init_flow()
    authorization_url = get_authorization_url(flow)
    st.link_button("Authenticate with Google", authorization_url)

    # Get authorization response code from URL
    if 'code' in st.query_params and st.query_params['code']:
        code = st.query_params['code']
        flow.fetch_token(code=code)
        credentials = flow.credentials
        save_credentials_to_session(credentials)
        st.rerun()

credentials = get_credentials_from_session()
if credentials:
    st.write("You are authenticated!")
    st.switch_page("./src/pages/files.py")
else:
    st.write("Please authenticate to access Google Drive.")


