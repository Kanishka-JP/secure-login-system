import bcrypt
import pyotp
import jwt
import random
import string
from datetime import datetime, timedelta, timezone
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

def generate_email_otp():
    return "".join(random.choices(string.digits, k=6))

OTP_VALIDITY_MINUTES = 5

@router.post("/register/verify-otp")
def verify_email_otp(data: EmailOTPVerify):
    ref = db.collection("email_otps").document(data.email)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(400, "OTP not found")

    otp_data = doc.to_dict()

    created_at = otp_data.get("created_at")
    if not created_at:
        raise HTTPException(400, "Invalid OTP record")

    # Firestore Timestamp → datetime
    if hasattr(created_at, "to_datetime"):
        created_at = created_at.to_datetime()

    # Normalize to UTC
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    if now - created_at > timedelta(minutes=OTP_VALIDITY_MINUTES):
        ref.delete()
        raise HTTPException(400, "OTP expired")

    if otp_data.get("otp") != data.otp:
        raise HTTPException(401, "Invalid OTP")

    ref.update({"verified": True})
    return {"message": "Email verified"}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def generate_totp_secret():
    return pyotp.random_base32()

def verify_totp(secret: str, otp: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

def create_jwt(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

