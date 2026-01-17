import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 seconds safety timeout
});

/* ---------- REGISTRATION ---------- */

export const sendEmailOTP = (email) =>
  API.post("/auth/register/send-otp", { email });

export const verifyEmailOTP = (email, otp) =>
  API.post("/auth/register/verify-otp", { email, otp });

export const setPassword = (email, password, confirm_password) =>
  API.post("/auth/register/set-password", {
    email,
    password,
    confirm_password,
  });

/* ---------- LOGIN ---------- */

export const loginUser = (email, password, otp) =>
  API.post("/auth/login", {
    email,
    password,
    otp,
  });

/* ---------- FORGOT PASSWORD ---------- */

export const sendForgotOTP = (email) =>
  API.post("/auth/forgot/send-otp", { email });

export const verifyForgotOTP = (email, otp) =>
  API.post("/auth/forgot/verify-otp", { email, otp });

export const resetPassword = (email, password, confirm_password) =>
  API.post("/auth/forgot/reset-password", {
    email,
    password,
    confirm_password,
  });

export default API;
