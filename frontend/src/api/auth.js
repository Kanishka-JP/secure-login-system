import axios from "axios";

const API = axios.create({
  baseURL:import.meta.env.VITE_API_BASE_URL, // FastAPI backend
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
