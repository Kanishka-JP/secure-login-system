from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta, timezone
import pyotp
import qrcode
import io
import base64

from app.database import db
from app.models import (
    EmailRequest,
    OTPVerifyRequest,
    SetPasswordRequest,
    LoginRequest,
)
from app.security import (
    generate_email_otp,
    hash_password,
    verify_password,
    generate_totp_secret,
    verify_totp,
    create_jwt,
)
from app.email_service import send_otp_email
from app.config import ISSUER_NAME

router = APIRouter(prefix="/auth", tags=["Authentication"])

OTP_VALIDITY_MINUTES = 5


# ================= REGISTER : SEND EMAIL OTP =================
@router.post("/register/send-otp")
def send_email_otp_route(data: EmailRequest):
    if db.collection("users").document(data.email).get().exists:
        raise HTTPException(400, "User already exists")

    otp = generate_email_otp()

    db.collection("email_otps").document(data.email).set({
        "otp": otp,
        "created_at": datetime.now(timezone.utc),
    })

    try:
        send_otp_email(data.email, otp)
    except Exception:
        raise HTTPException(500, "Email service unavailable")

    return {"message": "OTP sent to email"}


# ================= REGISTER : VERIFY EMAIL OTP =================
@router.post("/register/verify-otp")
def verify_email_otp(data: OTPVerifyRequest):
    ref = db.collection("email_otps").document(data.email)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(400, "OTP not found")

    otp_data = doc.to_dict()
    created_at = otp_data.get("created_at")

    if hasattr(created_at, "to_datetime"):
        created_at = created_at.to_datetime()

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) - created_at > timedelta(minutes=OTP_VALIDITY_MINUTES):
        ref.delete()
        raise HTTPException(400, "OTP expired")

    if otp_data.get("otp") != data.otp:
        raise HTTPException(401, "Invalid OTP")

    ref.update({"verified": True})
    return {"message": "Email verified"}


# ================= REGISTER : SET PASSWORD + GENERATE 2FA =================
@router.post("/register/set-password")
def set_password(data: SetPasswordRequest):
    if data.password != data.confirm_password:
        raise HTTPException(400, "Passwords do not match")

    otp_ref = db.collection("email_otps").document(data.email)
    otp_doc = otp_ref.get()

    if not otp_doc.exists or not otp_doc.to_dict().get("verified"):
        raise HTTPException(403, "Email not verified")

    secret = generate_totp_secret()
    totp = pyotp.TOTP(secret)

    otpauth_uri = totp.provisioning_uri(
        name=data.email,
        issuer_name=ISSUER_NAME
    )

    # Generate QR
    qr = qrcode.make(otpauth_uri)
    buf = io.BytesIO()
    qr.save(buf)
    qr_base64 = base64.b64encode(buf.getvalue()).decode()

    db.collection("users").document(data.email).set({
        "email": data.email,
        "password_hash": hash_password(data.password),
        "totp_secret": secret,
        "created_at": datetime.utcnow(),
    })

    otp_ref.delete()

    return {
        "message": "Registration successful",
        "qr_code_base64": qr_base64,
    }


# ================= LOGIN (ALWAYS 2FA) =================
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


# ================= FORGOT PASSWORD : SEND OTP =================
@router.post("/forgot/send-otp")
def send_forgot_otp(data: EmailRequest):
    if not db.collection("users").document(data.email).get().exists:
        raise HTTPException(404, "User not found")

    otp = generate_email_otp()

    db.collection("password_reset_otps").document(data.email).set({
        "otp": otp,
        "created_at": datetime.now(timezone.utc),
    })

    try:
        send_otp_email(data.email, otp)
    except Exception:
        raise HTTPException(500, "Email service unavailable")

    return {"message": "OTP sent"}


# ================= FORGOT PASSWORD : VERIFY OTP =================
@router.post("/forgot/verify-otp")
def verify_forgot_otp(data: OTPVerifyRequest):
    ref = db.collection("password_reset_otps").document(data.email)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(400, "OTP not found")

    otp_data = doc.to_dict()
    created_at = otp_data.get("created_at")

    if hasattr(created_at, "to_datetime"):
        created_at = created_at.to_datetime()

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) - created_at > timedelta(minutes=OTP_VALIDITY_MINUTES):
        ref.delete()
        raise HTTPException(400, "OTP expired")

    if otp_data.get("otp") != data.otp:
        raise HTTPException(401, "Invalid OTP")

    ref.update({"verified": True})
    return {"message": "OTP verified"}


# ================= FORGOT PASSWORD : RESET =================
@router.post("/forgot/reset-password")
def reset_password(data: SetPasswordRequest):
    if data.password != data.confirm_password:
        raise HTTPException(400, "Passwords do not match")

    otp_ref = db.collection("password_reset_otps").document(data.email)
    otp_doc = otp_ref.get()

    if not otp_doc.exists or not otp_doc.to_dict().get("verified"):
        raise HTTPException(403, "OTP not verified")

    db.collection("users").document(data.email).update({
        "password_hash": hash_password(data.password)
    })

    otp_ref.delete()
    return {"message": "Password reset successful"}
