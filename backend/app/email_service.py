import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_otp_email(to_email: str, otp: str):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Email Verification OTP",
        html_content=f"""
        <h3>Secure Login</h3>
        <p>Your OTP is:</p>
        <h2>{otp}</h2>
        <p>This OTP is valid for 5 minutes.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("EMAIL ERROR:", e)
        raise
