import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up the SMTP server
smtp_server = "smtp.gmail.com"  # e.g., smtp.gmail.com for Gmail

def send_email(from_email, to_email, body, key):
    # Create a MIMEMultipart object
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, 587)  # Port 587 for TLS
    server.starttls()  # Secure the connection
    server.login(from_email, key)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
