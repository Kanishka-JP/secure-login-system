import { useState } from "react";
import {
  sendEmailOTP,
  verifyEmailOTP,
  setPassword,
  loginUser,
} from "../api/auth";

import AuthCard from "../components/AuthCard";
import InputField from "../components/InputField";
import OTPBoxes from "../components/OTPBoxes";
import StepIndicator from "../components/StepIndicator";

export default function AuthPage({ onLogin }) {
  const [activeTab, setActiveTab] = useState("register");

  /* -------- REGISTER STATES -------- */
  const [regStep, setRegStep] = useState(0);
  const [regEmail, setRegEmail] = useState("");
  const [regOtp, setRegOtp] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regConfirm, setRegConfirm] = useState("");

  /* -------- LOGIN STATES -------- */
  const [loginStep, setLoginStep] = useState(0);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginOtp, setLoginOtp] = useState("");

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  /* ================= REGISTER FLOW ================= */

  const handleSendOTP = async () => {
    setError("");
    setSuccess("");

    if (!regEmail) {
      setError("Please enter a valid email");
      return;
    }

    try {
      setLoading(true);
      await sendEmailOTP(regEmail);
      setRegStep(1);
      setSuccess("OTP sent to your email");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to send OTP");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async () => {
    setError("");
    try {
      setLoading(true);
      await verifyEmailOTP(regEmail, regOtp);
      setRegStep(2);
      setSuccess("Email verified");
    } catch (err) {
      setError(err?.response?.data?.detail || "Invalid or expired OTP");
    } finally {
      setLoading(false);
    }
  };

  const handleSetPassword = async () => {
    setError("");
    if (regPassword !== regConfirm) {
      setError("Passwords do not match");
      return;
    }

    try {
      setLoading(true);
      await setPassword(regEmail, regPassword, regConfirm);
      setSuccess("Registration successful. Please login.");
      setActiveTab("login");
      setLoginStep(0);
    } catch (err) {
      setError(err?.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  /* ================= LOGIN FLOW ================= */

  const handleVerifyCredentials = () => {
    if (!loginEmail || !loginPassword) {
      setError("Enter email and password");
      return;
    }
    setError("");
    setLoginStep(1);
  };

  const handleLogin = async () => {
    setError("");
    try {
      setLoading(true);
      const res = await loginUser(loginEmail, loginPassword, loginOtp);
      localStorage.setItem("token", res.data.access_token);
      onLogin(loginEmail);
    } catch (err) {
      setError(err?.response?.data?.detail || "Invalid credentials or OTP");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 to-slate-900 px-4">
      <AuthCard>
        <h1 className="text-2xl font-bold text-center text-white mb-2">
          Secure Login
        </h1>
        <p className="text-center text-slate-400 mb-6">
          Email Verification & Two-Factor Authentication
        </p>

        {/* -------- TABS -------- */}
        <div className="flex mb-6 bg-slate-800 rounded-lg overflow-hidden">
          <button
            className={`flex-1 py-2 font-semibold ${
              activeTab === "register"
                ? "bg-blue-600 text-white"
                : "text-slate-400"
            }`}
            onClick={() => {
              setActiveTab("register");
              setError("");
              setSuccess("");
              setRegStep(0);
            }}
          >
            Register
          </button>

          <button
            className={`flex-1 py-2 font-semibold ${
              activeTab === "login"
                ? "bg-green-600 text-white"
                : "text-slate-400"
            }`}
            onClick={() => {
              setActiveTab("login");
              setError("");
              setSuccess("");
              setLoginStep(0);
            }}
          >
            Login
          </button>
        </div>

        {/* ================= REGISTER TAB ================= */}
        {activeTab === "register" && (
          <>
            <StepIndicator step={regStep} mode="register" />

            {regStep === 0 && (
              <>
                <InputField label="Email" onChange={setRegEmail} />
                <button
                  disabled={loading}
                  onClick={handleSendOTP}
                  className="w-full py-3 bg-blue-600 rounded-lg text-white"
                >
                  {loading ? "Sending..." : "Send OTP"}
                </button>
              </>
            )}

            {regStep === 1 && (
              <>
                <OTPBoxes onChange={setRegOtp} />
                <button
                  disabled={loading}
                  onClick={handleVerifyOTP}
                  className="w-full py-3 bg-green-600 rounded-lg text-white"
                >
                  Verify Email
                </button>
              </>
            )}

            {regStep === 2 && (
              <>
                <InputField
                  label="Create Password"
                  type="password"
                  onChange={setRegPassword}
                />
                <InputField
                  label="Confirm Password"
                  type="password"
                  onChange={setRegConfirm}
                />
                <button
                  disabled={loading}
                  onClick={handleSetPassword}
                  className="w-full py-3 bg-indigo-600 rounded-lg text-white"
                >
                  Create Account
                </button>
              </>
            )}
          </>
        )}

        {/* ================= LOGIN TAB ================= */}
        {activeTab === "login" && (
          <>
            <StepIndicator step={loginStep} mode="login" />

            {loginStep === 0 && (
              <>
                <InputField label="Email" onChange={setLoginEmail} />
                <InputField
                  label="Password"
                  type="password"
                  onChange={setLoginPassword}
                />
                <button
                  onClick={handleVerifyCredentials}
                  className="w-full py-3 bg-green-600 rounded-lg text-white"
                >
                  Verify Credentials
                </button>
              </>
            )}

            {loginStep === 1 && (
              <>
                <OTPBoxes onChange={setLoginOtp} />
                <button
                  disabled={loading}
                  onClick={handleLogin}
                  className="w-full py-3 bg-green-600 rounded-lg text-white"
                >
                  {loading ? "Logging in..." : "Login"}
                </button>
              </>
            )}
          </>
        )}

        {error && (
          <p className="text-red-400 text-sm text-center mt-4">
            {error}
          </p>
        )}

        {success && (
          <p className="text-green-400 text-sm text-center mt-4">
            {success}
          </p>
        )}
      </AuthCard>
    </div>
  );
}
