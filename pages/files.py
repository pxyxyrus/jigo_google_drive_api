import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import zipfile
from google.auth.transport.requests import Request

# Function to load credentials
def load_credentials():
    if 'credentials' not in st.session_state:
        st.session_state.credentials = None
    return st.session_state.credentials


# Function to list non-Google Docs editor files in a specific folder
def list_files(service, folder_id='root', load_next_page=False):
    if 'file_cache' not in st.session_state:
        st.session_state.file_cache = {}
    
    if folder_id in st.session_state.file_cache and not load_next_page:
        print("Using cache")
        return st.session_state.file_cache[folder_id]['files']
    
    query = (
        f"'{folder_id}' in parents and trashed=false and "
        "mimeType != 'application/vnd.google-apps.document' and "
        "mimeType != 'application/vnd.google-apps.spreadsheet' and "
        "mimeType != 'application/vnd.google-apps.presentation' and "
        "mimeType != 'application/vnd.google-apps.form'"
    )

    nextPageToken = None
    if folder_id in st.session_state.file_cache:
        nextPageToken = st.session_state.file_cache['folder_id'].get('nextPageToken', None)
    results = service.files().list(
        q=query,
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType)",
        pageToken=nextPageToken
    ).execute()
    files = results.get('files', [])
    nextPageToken = results.get('nextPageToken')
    st.session_state.file_cache[folder_id] = {
        'files': files,
        'nextPageToken': nextPageToken
    }
    return files


# Function to download a file
def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file_io = io.BytesIO()
    downloader = MediaIoBaseDownload(file_io, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_io.seek(0)
    return file_io


def navigate_to_folder(folder_id, folder_name):
    st.session_state.path.append(folder_id)
    st.session_state.names.append(folder_name)


def go_back():
    if len(st.session_state.path) > 1:
        st.session_state.path.pop()
        st.session_state.names.pop()


# File Explorer Page
st.title("Google Drive File Explorer")

creds = load_credentials()

if creds is None:
    st.warning("Please authenticate first on the Authentication page.")
else:
    service = build('drive', 'v3', credentials=creds)

    if 'path' not in st.session_state:
        st.session_state.path = ['root']
        st.session_state.names = ['My Drive']

    nav_path = ' / '.join(st.session_state.names)
    st.write(f"Current Path: {nav_path}")

    if len(st.session_state.path) > 1:
        if st.button("Go Back"):
            go_back()
            st.rerun()

    current_folder_id = st.session_state.path[-1]
    files = list_files(service, current_folder_id)

    if 'selected_files' not in st.session_state:
        st.session_state.selected_files = []

    folders = [f for f in files if f['mimeType'] == 'application/vnd.google-apps.folder']
    all_files = [f for f in files if f['mimeType'] != 'application/vnd.google-apps.folder']

    col1, col2 = st.columns(2)

    with col1:
        st.header("Folders")
        for folder in folders:
            if st.button(folder['name']):
                navigate_to_folder(folder['id'], folder['name'])
                st.rerun()

    
    selected_files = st.session_state.selected_files
    with col2:  
        st.header("Files")
        for file in all_files:
            is_selected = any(f['id'] == file['id'] for f in selected_files)
            if st.checkbox(file['name'], key=file['id'], value=is_selected):
                if not is_selected:
                    selected_files.append(file)
                    st.rerun()
            else:
                if is_selected:
                    selected_files = [f for f in selected_files if f['id'] != file['id']]
                    st.session_state.selected_files = selected_files
                    st.rerun()

    if selected_files:
        if st.button("Download Selected Files as ZIP"):
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for file in selected_files:
                        file_io = download_file(service, file['id'])
                        zip_file.writestr(f"{file['name']}", file_io.getvalue())
                zip_buffer.seek(0)
                st.download_button(
                    label="Download ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="selected_files.zip",
                    mime="application/zip"
                )