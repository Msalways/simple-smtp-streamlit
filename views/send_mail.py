import time
import streamlit as st
import pandas as pd
import streamlit_quill as sq
from email_sender import EmailSender

st.title('Send Mail')

with st.form(key='send_mail_form'):
    subject = st.text_input('Subject')
    st.write("Email Body")
    message = sq.st_quill(html=True, placeholder="Compose Mail")
    attachments = st.file_uploader("Upload Attachments", accept_multiple_files=True)
    emailExcel = st.file_uploader("Upload Email Excel File", type=['xlsx'])

    submitted = st.form_submit_button(label='Send', disabled=st.session_state.get('save_spinner_active', False))

    if submitted:
        st.session_state['save_spinner_active'] = True
        st.rerun()

if st.session_state.get('save_spinner_active', False):
    try:
        smtpConfig = EmailSender()
        if not emailExcel:
            st.warning("Please upload List of Emails file")
            st.session_state['save_spinner_active'] = False
            st.rerun()
            raise ValueError("Please upload List of Emails")
        elif not emailExcel.name.endswith('.xlsx'):
            st.error("Uploaded file is not XLSX")
            st.session_state['save_spinner_active'] = False
            st.rerun()
            raise ValueError("Uploaded file is not XLSX")
        else:
            df = pd.read_excel(emailExcel)
            if "emailId" not in df.columns:
                st.error("The 'emailId' column is missing in the Excel file.")
                st.session_state['save_spinner_active'] = False
                st.rerun()
                raise ValueError("The 'emailId' column is missing in the Excel file.")
            else:
                emailIds = df['emailId'].dropna().tolist()
                with st.spinner("Sending emails..."):
                    smtpConfig.send_mail(toMailIds=emailIds, subject=subject, body=message, attachments=attachments)
                    st.success("Mail Sent Successfully")
    except ValueError:
        pass
    except Exception as send_error:
        st.error(f"Failed to send emails: {send_error}")
    finally:
        st.session_state['save_spinner_active'] = False
        time.sleep(3)
        st.rerun()