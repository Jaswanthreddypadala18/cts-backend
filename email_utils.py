
import smtplib
from email.message import EmailMessage
from config import settings

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.MAIL_FROM
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as s:
        s.starttls()
        s.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        s.send_message(msg)
