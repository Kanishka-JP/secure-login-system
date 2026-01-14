import smtplib
from email.mime.text import MIMEText
from app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD

def send_otp_email(to_email: str, otp: str):
    try:
        body = f"""
Your Secure Login verification code is:

{otp}

This OTP is valid for 5 minutes.
If you did not request this, please ignore this email.
"""
        msg = MIMEText(body)
        msg["Subject"] = "Secure Login – Email Verification"
        msg["From"] = EMAIL_USER
        msg["To"] = to_email

        with smtplib.SMTP_SSL(EMAIL_HOST, int(EMAIL_PORT), timeout=10) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        # IMPORTANT: log error so Render shows it
        print("EMAIL ERROR:", str(e))
        raise RuntimeError("Failed to send email")
