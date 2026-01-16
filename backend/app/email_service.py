import resend
from app.config import RESEND_API_KEY, FROM_EMAIL

# Configure API key
resend.api_key = RESEND_API_KEY


def send_otp_email(to_email: str, otp: str):
    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": to_email,
            "subject": "Your Secure Login OTP",
            "html": f"""
                <div style="font-family:Arial, sans-serif">
                    <h2>Secure Login Verification</h2>
                    <p>Your One-Time Password (OTP) is:</p>
                    <h1 style="letter-spacing:3px">{otp}</h1>
                    <p>This OTP is valid for 5 minutes.</p>
                </div>
            """
        })
    except Exception as e:
        print("EMAIL ERROR:", e)
        raise RuntimeError("Email service unavailable")
