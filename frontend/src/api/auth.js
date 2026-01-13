import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000", // FastAPI backend
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Register user
 */
export const registerUser = (email, password) => {
  return API.post("/auth/register", {
    email,
    password,
  });
};

export const requestRegisterOTP = (email) => {
  return API.post("/auth/register/request-otp", { email });
};

export const verifyRegisterOTP = (email, password, otp) => {
  return API.post("/auth/register/verify-otp", {
    email,
    password,
    otp,
  });
};

/**
 * Verify 2FA OTP
 */
export const verify2FA = (email, otp) => {
  return API.post("/auth/verify-setup", {
    email,
    otp,
  });
};

/**
 * Login user
 */
export const loginUser = (email, password, otp) => {
  return API.post("/auth/login", {
    email,
    password,
    otp,
  });
};
