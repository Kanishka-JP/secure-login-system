# 🔐 Secure Login System  
**Email OTP · Google Authenticator (2FA) · Forgot Password · Strong Password Policy**

A full-stack secure authentication system built with **React (Vite)**, **FastAPI**, and **Firebase Firestore**, implementing industry-grade authentication and password security.

---

## 🚀 Features

### ✅ Registration
- Email OTP verification
- Strong password creation
- Google Authenticator (TOTP) QR code setup
- Secure user account creation

### ✅ Login
- Email + Password verification
- Mandatory Google Authenticator OTP for every login
- JWT-based authentication

### ✅ Forgot Password
- Email OTP verification
- Secure password reset
- Database update with new password

### ✅ Security
- OTP expiration
- OTP resend with 60-second cooldown
- Google Authenticator (TOTP)
- bcrypt password hashing
- JWT authentication

---

## 🔒 Password Policy (Strict)

Passwords **must meet ALL conditions**:

- Minimum **12 characters**
- Maximum **36 characters**
- At least:
  - **1 uppercase letter**
  - **1 lowercase letter**
  - **1 number**
  - **1 special character** (`! @ # $ % ^ & *` etc.)

❌ Passwords that do not meet these rules are rejected during:
- Registration
- Password reset

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- Axios
- Tailwind CSS

### Backend
- FastAPI
- Firebase Firestore
- PyOTP (Google Authenticator)
- bcrypt
- JWT
- SendGrid / SMTP Email Service

---

## ▶️ Run Locally

### Backend
```bash
uvicorn app.main:app --reload
```

### Frontend
```bash
npm run dev
```

---

## ⏱️ OTP Rules

| Feature | Value |
|------|------|
OTP Expiry | 5 minutes
Resend OTP Cooldown | 60 seconds
2FA | Mandatory

---

## 📄 License

This project is licensed under the MIT License. Feel free to fork and customize, but credit is appreciated.
