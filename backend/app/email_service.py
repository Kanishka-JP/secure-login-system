import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_otp_email(to_email: str, otp: str):
    if not RESEND_API_KEY:
        raise RuntimeError("RESEND_API_KEY not set")

    if not FROM_EMAIL:
        raise RuntimeError("FROM_EMAIL not set")

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
            "html": f"<h1>Your OTP is {otp}</h1>",
        },
        timeout=10,
    )

    print("Resend status:", response.status_code)
    print("Resend response:", response.text)

    response.raise_for_status()
