import smtplib
from email.mime.text import MIMEText

from faedoguerra import settings


def send_multiple_emails(addresses, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.GMAIL_USERNAME
    msg['To'] = ', '.join(addresses)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(settings.GMAIL_USERNAME, settings.GMAIL_APP_PASSWORD)
       smtp_server.sendmail(settings.GMAIL_USERNAME, addresses, msg.as_string())


def send_email(address, subject, body):
    send_multiple_emails([address], subject, body)
