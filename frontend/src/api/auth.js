import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

/* -------- REGISTER (STEP 1: SEND EMAIL OTP) -------- */
export const requestRegisterOTP = (email, password) =>
  API.post("/auth/register/request-otp", { email, password });

/* -------- REGISTER (STEP 2: VERIFY EMAIL OTP) -------- */
export const verifyRegisterOTP = (email, password, otp) =>
  API.post("/auth/register/verify-otp", { email, password, otp });

/* -------- LOGIN (PASSWORD + GOOGLE AUTH OTP) -------- */
export const loginUser = (email, password, otp) =>
  API.post("/auth/login", { email, password, otp });
