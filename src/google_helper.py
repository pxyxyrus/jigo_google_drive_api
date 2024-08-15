from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from google.auth.transport.requests import Request
import streamlit as st
from config import config

# Path to your client_secret.json file
CLIENT_SECRETS_FILE = config['google']['client_secrets_file']

# Define the scopes
# For this app we only need access to Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

# Redirect URI
REDIRECT_URI = config['google']['redirect_uri']

service = None


# ------------- Helper functions for the OAuth2.0 flow ------------------

# Function to get the authorization URL
def get_authorization_url(flow):
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return authorization_url

# Function to initialize the and returns the flow object for OAuth2.0
def init_flow():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URI
    return flow


# ------------- Helper functions for credentials obtained from the flow object after OAuth2.0 ------------------

# Function to save credentials in session state
def save_credentials_to_session(credentials):
    st.session_state['credentials'] = credentials

# Function to get credentials from session state
def get_credentials_from_session():
    if 'credentials' in st.session_state and st.session_state['credentials']:
        return st.session_state['credentials']
    return None



# ------------- Helper functions for initing a google api service using the credentials -----------------------

def init_service():
    global service
    if service is None:
        creds = get_credentials_from_session()
        service = build('drive', 'v3', credentials=creds)


def get_files(query, page_size=100, next_page_token=None, fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, size)"):
    return service.files().list(
        q=query,
        pageSize=page_size,
        fields=fields,
        pageToken=next_page_token
    ).execute()


# Function to download a file
def download_file(file_id):
    global service
    request = service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_io.seek(0)
    return file_io

