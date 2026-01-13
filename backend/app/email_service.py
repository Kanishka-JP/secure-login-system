import smtplib
from email.mime.text import MIMEText
from app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD

def send_otp_email(to_email: str, otp: str):
    msg = MIMEText(f"Your verification OTP is: {otp}\n\nValid for 5 minutes.")
    msg["Subject"] = "Email Verification OTP"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
