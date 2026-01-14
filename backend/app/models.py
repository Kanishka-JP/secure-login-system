from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    email: EmailStr

class EmailOTPVerify(BaseModel):
    email: EmailStr
    otp: str

class SetPasswordRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    otp: str
