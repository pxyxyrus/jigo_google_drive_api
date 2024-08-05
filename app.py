import streamlit as st

auth_page = st.Page("./pages/auth.py", title="auth")
files_page = st.Page("./pages/files.py", title="files")

pg = st.navigation([auth_page, files_page])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()


