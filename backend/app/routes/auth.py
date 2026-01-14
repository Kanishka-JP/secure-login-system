from fastapi import APIRouter, HTTPException
from datetime import datetime
import pyotp

from app.database import db
from app.models import (
    EmailRequest,
    EmailOTPVerify,
    SetPasswordRequest,
    LoginRequest,
)
from app.security import (
    generate_email_otp,
    otp_expired,
    hash_password,
    verify_password,
    generate_totp_secret,
    verify_totp,
    create_jwt,
)
from app.email_service import send_otp_email
from app.config import ISSUER_NAME

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ================= STEP 1: SEND EMAIL OTP =================
@router.post("/register/send-otp")
def send_email_otp(data: EmailRequest):
    if db.collection("users").document(data.email).get().exists:
        raise HTTPException(400, "User already exists")

    otp = generate_email_otp()

    db.collection("email_otps").document(data.email).set({
        "otp": otp,
        "created_at": datetime.utcnow()
    })

    send_otp_email(data.email, otp)
    return {"message": "OTP sent to email"}


# ================= STEP 2: VERIFY EMAIL OTP =================
@router.post("/register/verify-otp")
def verify_email_otp(data: EmailOTPVerify):
    ref = db.collection("email_otps").document(data.email)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(400, "OTP not found")

    data_db = doc.to_dict()

    if otp_expired(data_db["created_at"]) or data_db["otp"] != data.otp:
        raise HTTPException(401, "Invalid or expired OTP")

    ref.update({"verified": True})
    return {"message": "Email verified"}


# ================= STEP 3: SET PASSWORD =================
@router.post("/register/set-password")
def set_password(data: SetPasswordRequest):
    if data.password != data.confirm_password:
        raise HTTPException(400, "Passwords do not match")

    otp_ref = db.collection("email_otps").document(data.email)
    otp_doc = otp_ref.get()

    if not otp_doc.exists or not otp_doc.to_dict().get("verified"):
        raise HTTPException(403, "Email not verified")

    secret = generate_totp_secret()

    db.collection("users").document(data.email).set({
        "email": data.email,
        "password_hash": hash_password(data.password),
        "totp_secret": secret,
        "created_at": datetime.utcnow()
    })

    otp_ref.delete()

    return {"message": "Registration successful"}


# ================= LOGIN (2FA) =================
@router.post("/login")
def login(data: LoginRequest):
    user_ref = db.collection("users").document(data.email)
    user = user_ref.get()

    if not user.exists:
        raise HTTPException(404, "User not found")

    user_data = user.to_dict()

    if not verify_password(data.password, user_data["password_hash"]):
        raise HTTPException(401, "Invalid password")

    if not verify_totp(user_data["totp_secret"], data.otp):
        raise HTTPException(401, "Invalid OTP")

    token = create_jwt(data.email)
    return {"access_token": token}
