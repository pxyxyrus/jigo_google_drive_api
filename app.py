import streamlit as st
import config

auth_page = st.Page("./src/pages/auth.py", title="auth")
files_page = st.Page("./src/pages/files.py", title="files")

pg = st.navigation([auth_page, files_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()


