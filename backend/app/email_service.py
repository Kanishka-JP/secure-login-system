from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import FROM_EMAIL, SENDGRID_API_KEY

def send_otp_email(to_email: str, otp: str):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Your Email Verification OTP",
        html_content=f"""
        <h2>Secure Login</h2>
        <p>Your OTP is:</p>
        <h1>{otp}</h1>
        <p>This OTP is valid for 5 minutes.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print("SENDGRID ERROR:", e)
        raise
