import streamlit as st

from db import init_db

init_db()


integrationPage = st.Page(
    page="views/integration.py",
    title="Integration"
    
)

sendMailPage = st.Page(
    page="views/send_mail.py",
    title="Send Mail",
    default=True
)

pg = st.navigation(
    pages=[sendMailPage,integrationPage]
    
)

pg.run()