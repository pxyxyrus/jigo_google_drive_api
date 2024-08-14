import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# Path to your client_secret.json file
CLIENT_SECRETS_FILE = "credentials.json"

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

# Redirect URI
REDIRECT_URI = "http://localhost:8501/auth"


# Function to get the authorization URL
def get_authorization_url(flow):
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return authorization_url

# Function to initialize the OAuth flow
def init_flow():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URI
    return flow

# Function to save credentials in session state
def save_credentials_to_session(credentials):
    st.session_state['credentials'] = credentials

# Function to get credentials from session state
def get_credentials_from_session():
    if 'credentials' in st.session_state and st.session_state['credentials']:
        return st.session_state['credentials']
    return None


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
    st.switch_page("./pages/files.py")
    # Use the credentials to access Google Drive or other Google APIs
    # drive_service = build('drive', 'v3', credentials=credentials)
else:
    st.write("Please authenticate to access Google Drive.")


