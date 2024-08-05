import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Function to authenticate with Google
def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive.readonly'],
        redirect_uri='http://localhost:8501/files'
    )
    creds = flow.run_local_server(port=0)
    return creds

# Authentication Page
st.title("Google Drive Authentication")

# Authenticate the user when the button is clicked
if 'credentials' not in st.session_state:
    st.session_state.credentials = None

if st.session_state.credentials is None:
    if st.button("Authenticate with Google"):
        creds = authenticate()
        st.session_state.credentials = creds


# Save credentials to a session file for the file explorer to use
if st.session_state.credentials:
    st.switch_page("./pages/files.py")

