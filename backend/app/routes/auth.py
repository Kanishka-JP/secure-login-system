from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import pyotp
import qrcode
import io
import base64

from app.database import db
from app.models import (
    EmailRequest,
    EmailOTPVerify,
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


# ================= STEP 1: SEND EMAIL OTP =================
@router.post("/register/send-otp")
def send_email_otp_route(data: EmailRequest):
    if db.collection("users").document(data.email).get().exists:
        raise HTTPException(400, "User already exists")

    otp = generate_email_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    db.collection("email_otps").document(data.email).set({
        "otp": otp,
        "expires_at": expires_at,
        "verified": False,
    })

    try:
        send_otp_email(data.email, otp)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Email service unavailable. Try again later."
        )

        return {"message": "OTP sent to email"}


# ================= STEP 2: VERIFY EMAIL OTP =================
@router.post("/register/verify-otp")
def verify_email_otp(data: EmailOTPVerify):
    ref = db.collection("email_otps").document(data.email)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(400, "OTP not found")

    data_db = doc.to_dict()

    if otp_expired(data_db.get("created_at")):
        raise HTTPException(401, "OTP expired")

    if data_db.get("otp") != data.otp:
        raise HTTPException(401, "Invalid OTP")

    ref.update({"verified": True})
    return {"message": "Email verified"}


# ================= STEP 3: SET PASSWORD + GENERATE 2FA =================
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


# ================= LOGIN (EMAIL + PASSWORD → 2FA) =================
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

    return {
        "message": "Login successful",
        "access_token": token
    }
