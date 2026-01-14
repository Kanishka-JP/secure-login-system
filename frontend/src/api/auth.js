import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

/* -------- REGISTRATION -------- */

// Step 1: Send email OTP
export const sendEmailOTP = (email) =>
  API.post("/auth/register/send-otp", { email });

// Step 2: Verify email OTP
export const verifyEmailOTP = (email, otp) =>
  API.post("/auth/register/verify-otp", { email, otp });

// Step 3: Set password
export const setPassword = (email, password, confirm_password) =>
  API.post("/auth/register/set-password", {
    email,
    password,
    confirm_password,
  });

/* -------- LOGIN -------- */

export const loginUser = (email, password, otp) =>
  API.post("/auth/login", { email, password, otp });

// Get Google Authenticator QR
export const getQRCode = (email) =>
  API.get(`/auth/qr/${email}`);
