import streamlit as st
import zipfile
from src.google_helper import *



# Function to list non-Google Docs editor files in a specific folder
def list_files(folder_id='root', load_next_page=False):
    if 'file_cache' not in st.session_state:
        st.session_state.file_cache = {}
    
    if 'files' not in st.session_state:
        st.session_state.files = {}


    if folder_id in st.session_state.file_cache and not load_next_page:
        return st.session_state.file_cache[folder_id]['files']
    
    query = (
        f"'{folder_id}' in parents and trashed=false and "
        "mimeType != 'application/vnd.google-apps.document' and "
        "mimeType != 'application/vnd.google-apps.spreadsheet' and "
        "mimeType != 'application/vnd.google-apps.presentation' and "
        "mimeType != 'application/vnd.google-apps.form'"
    )

    next_page_token = None
    if folder_id in st.session_state.file_cache:
        next_page_token = st.session_state.file_cache['folder_id'].get('nextPageToken', None)
    results = get_files(query, next_page_token)
    files = results.get('files', [])
    next_page_token = results.get('nextPageToken')
    st.session_state.file_cache[folder_id] = {
        'files': files,
        'nextPageToken': next_page_token
    }

    for f in files:
        st.session_state.files[f['id']] = f

    return files



def navigate_to_folder(folder_id, folder_name):
    st.session_state.path.append(folder_id)
    st.session_state.names.append(folder_name)


def go_back():
    if len(st.session_state.path) > 1:
        st.session_state.path.pop()
        st.session_state.names.pop()


# File Explorer Page
st.title("Google Drive File Explorer")

creds = get_credentials_from_session()

if creds is None:
    st.warning("Please authenticate first on the Authentication page.")
    if st.button("Go to Authentication"):
        st.switch_page("./src/pages/auth.py")

else:
    init_service()
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
    files = list_files(current_folder_id)

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


    with col2:  
        st.header("Files")
        for file in all_files:
            is_selected = any(f['id'] == file['id'] for f in st.session_state.selected_files)

            def on_change(fid):
                if st.session_state[fid]:
                    f = st.session_state.files[fid]
                    st.session_state.selected_files.append(f)
                else:
                    selected_files = [f for f in st.session_state.selected_files if f['id'] != fid]
                    st.session_state.selected_files = selected_files

            st.checkbox(file['name'], key=file['id'], value=is_selected, on_change=on_change, args=[file['id']])


    selected_files = st.session_state.selected_files
    if selected_files:
        if st.button("Download Selected Files as ZIP"):
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for file in selected_files:
                        file_io = download_file(file['id'])
                        zip_file.writestr(f"{file['name']}", file_io.getvalue())
                st.session_state.selected_files.clear()
                zip_buffer.seek(0)
                st.download_button(
                    label="Download ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="selected_files.zip",
                    mime="application/zip"
                )