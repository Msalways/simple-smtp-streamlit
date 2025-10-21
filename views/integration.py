import streamlit as st
from db import Session
from db.models.SMTPConfig import SMTPConfig
from email_sender import test_email_with_smtp

st.header('Integration')
st.subheader('SMTP Credentials')

# Open a new database session
session = Session()
smtpConfig = session.query(SMTPConfig).first()

# Debugging - Display current configuration in Streamlit
# st.write("Current Config:", "No SMTP configuration found." if not smtpConfig)

if not smtpConfig:
    st.write("SMTP Not Configured")

with st.form(key='smtp_form'):
    smtp_host = st.text_input('SMTP Host', value=smtpConfig.smtp_host if smtpConfig else '')
    smtp_port = st.number_input('SMTP Port', value=smtpConfig.smtp_port if smtpConfig else 465, min_value=1, max_value=65535)
    smtp_email = st.text_input('SMTP Email', value=smtpConfig.smtp_email if smtpConfig else '')
    smtp_password = st.text_input('SMTP Password', type='password')
    test_mail = st.text_input('Test Mail')
    
    submitted = st.form_submit_button(label='Save')
    if submitted:
        try:
            # Delete existing config (if any) and save new config
            # session.query(SMTPConfig).delete()
            test_email_with_smtp(smtp_host, smtp_port, smtp_email, smtp_password, test_mail )
            if smtpConfig:
                smtpConfig.smtp_host = smtp_host
                smtpConfig.smtp_port = smtp_port
                smtpConfig.smtp_email = smtp_email
                smtpConfig.smtp_password = smtp_password
            else:         
                session.add(SMTPConfig(smtp_host=smtp_host, smtp_port=smtp_port, smtp_email=smtp_email, smtp_password=smtp_password))
            session.commit()
            st.success('SMTP Configuration Saved Successfully')
        except Exception as e:
            st.error(f"Error saving SMTP configuration: {e}")
        finally:
            session.close() 
