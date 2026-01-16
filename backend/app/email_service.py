import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_otp_email(to_email: str, otp: str):
    if not SENDGRID_API_KEY or not FROM_EMAIL:
        raise RuntimeError("SendGrid configuration missing")

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Your Secure Login OTP",
        html_content=f"""
        <h2>Email Verification</h2>
        <p>Your OTP is:</p>
        <h1>{otp}</h1>
        <p>This OTP is valid for 5 minutes.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("SendGrid status:", response.status_code)
    except Exception as e:
        print("SENDGRID ERROR:", str(e))
        raise
