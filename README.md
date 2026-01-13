# 🔐 Secure Login System with Email OTP & 2FA (Google Authenticator)

A full-stack **secure authentication system** built using **FastAPI**, **React (Vite)**, **Firebase (Firestore)**, and **JWT**, implementing **email verification OTP** during registration and **Google Authenticator–based Two-Factor Authentication (2FA)** during login.

---

## 📌 Key Features

### ✅ Registration (Email Verification)
- Email & Password signup
- **Email OTP verification** (SMTP using App Password)
- Prevents fake or invalid email registrations

### ✅ Login (Strong Authentication)
- Email + Password
- **Time-based OTP (TOTP) via Google Authenticator**
- JWT token issued after successful login

### ✅ Security Best Practices
- Password hashing
- Time-based OTP (RFC 6238)
- JWT authentication
- Environment variables for secrets
- `.gitignore` protection for sensitive files

---

## 🧠 Authentication Flow

### 🔹 Registration Flow
```
User → Email + Password
     → Email OTP sent (SMTP)
     → OTP verification
     → User account created
     → TOTP secret generated (for future login)
```

### 🔹 Login Flow
```
User → Email + Password
     → Google Authenticator OTP
     → JWT token issued
     → Welcome Dashboard
```

✔ Email OTP = Verification  
✔ Google Authenticator OTP = Authentication (2FA)

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Firebase Firestore
- PyOTP
- JWT
- SMTP (Gmail App Password)

### Frontend
- React (Vite)
- Tailwind CSS v4
- Axios

---

## 📁 Project Structure

```
Secure login/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   └── auth.py
│   │   ├── security.py
│   │   ├── email_service.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── venv/
│   ├── .env
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
│
└── README.md
```

---

## 🔐 Environment Variables

All sensitive credentials are stored in `.env` and excluded from GitHub.

### backend/.env
```
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

ISSUER_NAME=SecureLogin

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USER=yourmail@gmail.com
EMAIL_PASSWORD=your_app_password
```

---

## ▶️ How to Run Locally

### Backend
```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```
cd frontend
npm install
npm run dev
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | /auth/register/request-otp | Send email OTP |
| POST | /auth/register/verify-otp | Verify email OTP & register |
| POST | /auth/login | Login with password + TOTP |
| GET  | /auth/qr/{email} | Get Google Authenticator QR |

---

## 🔒 Security Highlights

- Email OTP prevents fake registrations
- TOTP prevents account takeover
- JWT ensures stateless authentication
- Secrets protected using environment variables
- Time-limited OTP expiry

---

## 🎓 Academic Explanation

Email OTP is used for user verification, while Google Authenticator TOTP is used for two-factor authentication during login. Secrets are stored using environment variables and excluded from version control.
