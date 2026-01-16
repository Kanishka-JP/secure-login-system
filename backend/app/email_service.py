from resend import Resend
from app.config import RESEND_API_KEY, FROM_EMAIL

resend = Resend(api_key=RESEND_API_KEY)

def send_otp_email(to_email: str, otp: str):
    try:
        resend.emails.send({
            "from": FROM_EMAIL,
            "to": to_email,
            "subject": "Your Secure Login OTP",
            "html": f"""
                <div style="font-family:Arial">
                  <h2>Secure Login Verification</h2>
                  <p>Your OTP is:</p>
                  <h1>{otp}</h1>
                  <p>This OTP is valid for 5 minutes.</p>
                </div>
            """
        })
    except Exception as e:
        print("EMAIL ERROR:", e)
        raise RuntimeError("Email service unavailable")
