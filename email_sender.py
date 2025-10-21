import smtplib as sl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import time
from db import Session
from db.models.SMTPConfig import SMTPConfig
from mimetypes import guess_type
import socket

class EmailSender:
    def __init__(self):
        try:
            session = Session()
            smtpConfig = session.query(SMTPConfig).first()
            if not smtpConfig:
                raise ValueError("SMTP Not Configured")

            self.smtp_host = smtpConfig.smtp_host
            self.smtp_port = smtpConfig.smtp_port
            self.smtp_email = smtpConfig.smtp_email
            self.smtp_password = smtpConfig.smtp_password

            session.close()
        except Exception as e:
            raise e

    def send_mail(self, toMailIds, subject, body, attachments):
        server = None  # Initialize server to None
        try:
            print(toMailIds)
            msg = MIMEMultipart()
            msg["From"] = self.smtp_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            for attachment in attachments:
                mime_type = guess_type(attachment.name)
                attachment_data = attachment.read()
                if(mime_type):
                    attach_file = MIMEApplication(attachment_data,mime_type)
                    attach_file.add_header('Content-Disposition', 'attachment', filename=attachment.name)
                    msg.attach(attach_file)

            try:
                server = sl.SMTP_SSL(host=self.smtp_host, port=self.smtp_port, timeout=10) #added timeout
                server.login(self.smtp_email, self.smtp_password)

                for to in toMailIds:
                    try:
                        print(f"Sending email to {to}...")
                        server.sendmail(self.smtp_email, to, msg.as_string())
                        time.sleep(2)
                    except sl.SMTPException as send_error:
                        print(f"SMTP error sending email to {to}: {send_error}")
                    except Exception as send_error:
                        print(f"Failed to send email to {to}: {send_error}")
            except socket.timeout:
                raise TimeoutError("SMTP connection timed out.")
            except sl.SMTPAuthenticationError:
                raise sl.SMTPAuthenticationError("SMTP authentication error. Check your credentials.")
            except Exception as connection_error:
                raise Exception(f"SMTP connection failed: {connection_error}")

        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            raise e
        finally:
            if server:
                try:
                    server.quit() #use quit instead of close for smtp
                except Exception as close_error:
                    print(f"Error closing SMTP connection: {close_error}")
                    

def test_email_with_smtp(smtp_host,smtp_port,smtp_email,smtp_password,test_mail):
    try:
        server = sl.SMTP_SSL(smtp_host,smtp_port)
        server.login(smtp_email, smtp_password)
        msg = MIMEMultipart()
        msg["From"] = smtp_email
        msg["Subject"] = "Test Email"
        msg.attach(MIMEText("Test Email Body", "html"))
        server.sendmail(smtp_email, test_mail, msg.as_string())
        server.quit()
    except Exception as e:
        raise e
    