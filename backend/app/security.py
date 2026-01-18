import bcrypt
import pyotp
import random
import string
import re
from datetime import datetime, timedelta

from jose import jwt
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MINUTES


# ================= EMAIL OTP =================

def generate_email_otp() -> str:
    """Generate a 6-digit numeric OTP"""
    return "".join(random.choices(string.digits, k=6))

def otp_expired(created_at, minutes: int = 5) -> bool:
    """
    Check if OTP is expired.
    Firestore timestamps are UTC-aware.
    """
    if hasattr(created_at, "to_datetime"):
        created_at = created_at.to_datetime()

    return datetime.utcnow() > created_at + timedelta(minutes=minutes)


# ================= PASSWORD =================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def is_strong_password(password: str) -> bool:
    # length check (UPDATED)
    if len(password) < 12 or len(password) > 36:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        return False

    return True


# ================= GOOGLE AUTHENTICATOR =================

def generate_totp_secret() -> str:
    return pyotp.random_base32()

def verify_totp(secret: str, otp: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(otp, valid_window=1)


# ================= JWT =================

def create_jwt(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
