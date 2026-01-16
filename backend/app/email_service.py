import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_otp_email(to_email: str, otp: str):
    if not RESEND_API_KEY or not FROM_EMAIL:
        raise RuntimeError("Resend configuration missing")

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": FROM_EMAIL,
            "to": [to_email],
            "subject": "Your Secure Login OTP",
            "html": f"""
                <h2>Email Verification</h2>
                <p>Your OTP is:</p>
                <h1>{otp}</h1>
                <p>This OTP is valid for 5 minutes.</p>
            """,
        },
        timeout=10,
    )

    if response.status_code not in (200, 201):
        print("RESEND ERROR:", response.text)
        raise RuntimeError("Failed to send email via Resend")
