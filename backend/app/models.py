from pydantic import BaseModel, EmailStr


# ---------- COMMON ----------

class EmailRequest(BaseModel):
    email: EmailStr


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class SetPasswordRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str


# ---------- LOGIN ----------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    otp: str  # Google Authenticator OTP
