from fastapi import APIRouter, HTTPException
from datetime import datetime
import pyotp

from app.database import db
from app.models import RegisterRequest, OTPVerifyRequest, LoginRequest
from app.email_service import send_otp_email
from app.security import (
    hash_password,
    verify_password,
    generate_totp_secret,
    verify_totp,
    create_jwt,
    generate_email_otp,
    otp_expired,
)
from app.config import ISSUER_NAME

router = APIRouter(prefix="/auth", tags=["Authentication"])


# =========================================================
# 1️⃣ REQUEST EMAIL OTP (REGISTRATION – STEP 1)
# =========================================================
@router.post("/register/request-otp")
def request_register_otp(data: RegisterRequest):
    user_ref = db.collection("users").document(data.email)

    if user_ref.get().exists:
        raise HTTPException(status_code=400, detail="User already exists")

    otp = generate_email_otp()

    db.collection("email_otps").document(data.email).set({
        "otp": otp,
        "created_at": datetime.utcnow()
    })

    send_otp_email(data.email, otp)

    return {"message": "OTP sent to email"}


# =========================================================
# 2️⃣ VERIFY EMAIL OTP & CREATE USER (REGISTRATION – STEP 2)
# =========================================================
@router.post("/register/verify-otp")
def verify_register_otp(data: OTPVerifyRequest):
    otp_ref = db.collection("email_otps").document(data.email)
    otp_doc = otp_ref.get()

    if not otp_doc.exists:
        raise HTTPException(status_code=400, detail="OTP not found")

    otp_data = otp_doc.to_dict()

    if otp_expired(otp_data["created_at"]) or otp_data["otp"] != data.otp:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    # Generate TOTP secret for future login (2FA)
    secret = generate_totp_secret()

    db.collection("users").document(data.email).set({
        "email": data.email,
        "password_hash": hash_password(data.password),
        "totp_secret": secret,
        "two_fa_enabled": True,
        "created_at": datetime.utcnow()
    })

    otp_ref.delete()

    return {"message": "Registration successful"}


# =========================================================
# 3️⃣ LOGIN (PASSWORD + GOOGLE AUTHENTICATOR OTP)
# =========================================================
@router.post("/login")
def login(data: LoginRequest):
    user_ref = db.collection("users").document(data.email)
    user = user_ref.get()

    if not user.exists:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.to_dict()

    if not verify_password(data.password, user_data["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    if not verify_totp(user_data["totp_secret"], data.otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")

    token = create_jwt(data.email)

    return {
        "message": "Login successful",
        "access_token": token
    }


# =========================================================
# 4️⃣ GET QR CODE (OPTIONAL – SHOW AFTER REGISTRATION)
# =========================================================
@router.get("/qr/{email}")
def get_qr(email: str):
    user_ref = db.collection("users").document(email)
    user = user_ref.get()

    if not user.exists:
        raise HTTPException(status_code=404, detail="User not found")

    secret = user.to_dict()["totp_secret"]
    totp = pyotp.TOTP(secret)

    uri = totp.provisioning_uri(
        name=email,
        issuer_name=ISSUER_NAME
    )

    return {"otpauth_uri": uri}
