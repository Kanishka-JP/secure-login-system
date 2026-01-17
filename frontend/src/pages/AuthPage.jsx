import { useState } from "react";
import {
  sendEmailOTP,
  verifyEmailOTP,
  setPassword,
  loginUser,
  sendForgotOTP,
  verifyForgotOTP,
  resetPassword,
} from "../api/auth";

import AuthCard from "../components/AuthCard";
import InputField from "../components/InputField";
import OTPBoxes from "../components/OTPBoxes";
import StepIndicator from "../components/StepIndicator";

export default function AuthPage({ onLogin }) {
  const [tab, setTab] = useState("register"); // register | login | forgot
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  /* ================= REGISTER ================= */
  const [regStep, setRegStep] = useState(0);
  const [regEmail, setRegEmail] = useState("");
  const [regOtp, setRegOtp] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regConfirm, setRegConfirm] = useState("");

  /* ================= LOGIN ================= */
  const [loginStep, setLoginStep] = useState(0);
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [loginOtp, setLoginOtp] = useState("");

  /* ================= FORGOT ================= */
  const [fpStep, setFpStep] = useState(0);
  const [fpEmail, setFpEmail] = useState("");
  const [fpOtp, setFpOtp] = useState("");
  const [fpPassword, setFpPassword] = useState("");
  const [fpConfirm, setFpConfirm] = useState("");

  const resetMessages = () => {
    setError("");
    setSuccess("");
  };

  const primaryBtn =
    "w-full py-3 mt-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-semibold transition";
  const successBtn =
    "w-full py-3 mt-2 rounded-lg bg-green-600 hover:bg-green-700 text-white font-semibold transition";
  const disabledStyle = loading ? "opacity-50 cursor-not-allowed" : "";

  /* ================= REGISTER ================= */

  const handleSendRegOTP = async () => {
    resetMessages();
    setLoading(true);
    try {
      await sendEmailOTP(regEmail);
      setRegStep(1);
      setSuccess("OTP sent to email");
    } catch (e) {
      setError(e?.response?.data?.detail || "Failed to send OTP");
    }
    setLoading(false);
  };

  const handleVerifyRegOTP = async () => {
    resetMessages();
    setLoading(true);
    try {
      await verifyEmailOTP(regEmail, regOtp);
      setRegStep(2);
      setSuccess("Email verified");
    } catch (e) {
      setError(e?.response?.data?.detail || "Invalid OTP");
    }
    setLoading(false);
  };

  const handleCreateAccount = async () => {
    resetMessages();
    if (regPassword !== regConfirm) {
      setError("Passwords do not match");
      return;
    }
    setLoading(true);
    try {
      await setPassword(regEmail, regPassword, regConfirm);
      setSuccess("Registration successful. Please login.");
      setTab("login");
      setLoginStep(0);
    } catch (e) {
      setError(e?.response?.data?.detail || "Registration failed");
    }
    setLoading(false);
  };

  /* ================= LOGIN ================= */

  const handleVerifyCredentials = () => {
    resetMessages();
    if (!loginEmail || !loginPassword) {
      setError("Enter email and password");
      return;
    }
    setLoginStep(1);
  };

  const handleLogin = async () => {
    resetMessages();
    setLoading(true);
    try {
      const res = await loginUser(loginEmail, loginPassword, loginOtp);
      localStorage.setItem("token", res.data.access_token);
      onLogin(loginEmail);
    } catch (e) {
      setError(e?.response?.data?.detail || "Invalid OTP");
    }
    setLoading(false);
  };

  /* ================= FORGOT ================= */

  const handleSendForgotOTP = async () => {
    resetMessages();
    setLoading(true);
    try {
      await sendForgotOTP(fpEmail);
      setFpStep(1);
      setSuccess("OTP sent");
    } catch (e) {
      setError(e?.response?.data?.detail || "Failed to send OTP");
    }
    setLoading(false);
  };

  const handleVerifyForgotOTP = async () => {
    resetMessages();
    setLoading(true);
    try {
      await verifyForgotOTP(fpEmail, fpOtp);
      setFpStep(2);
    } catch (e) {
      setError(e?.response?.data?.detail || "Invalid OTP");
    }
    setLoading(false);
  };

  const handleResetPassword = async () => {
    resetMessages();
    if (fpPassword !== fpConfirm) {
      setError("Passwords do not match");
      return;
    }
    setLoading(true);
    try {
      await resetPassword(fpEmail, fpPassword, fpConfirm);
      setSuccess("Password reset successful. Please login.");
      setTab("login");
      setLoginStep(0);
    } catch (e) {
      setError(e?.response?.data?.detail || "Reset failed");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 to-slate-900 px-4">
      <AuthCard>
        <h1 className="text-2xl font-bold text-center text-white mb-4">
          Secure Login
        </h1>

        {/* Tabs */}
        {tab !== "forgot" && (
          <div className="flex mb-6 bg-slate-800 rounded-lg overflow-hidden">
            <button
              className={`flex-1 py-2 ${
                tab === "register"
                  ? "bg-blue-600 text-white"
                  : "text-slate-400"
              }`}
              onClick={() => {
                setTab("register");
                setRegStep(0);
                resetMessages();
              }}
            >
              Register
            </button>
            <button
              className={`flex-1 py-2 ${
                tab === "login"
                  ? "bg-green-600 text-white"
                  : "text-slate-400"
              }`}
              onClick={() => {
                setTab("login");
                setLoginStep(0);
                resetMessages();
              }}
            >
              Login
            </button>
          </div>
        )}

        {/* REGISTER */}
        {tab === "register" && (
          <>
            <StepIndicator step={regStep} mode="register" />

            {regStep === 0 && (
              <>
                <InputField label="Email" onChange={setRegEmail} />
                <button
                  disabled={loading}
                  onClick={handleSendRegOTP}
                  className={`${primaryBtn} ${disabledStyle}`}
                >
                  Send OTP
                </button>
              </>
            )}

            {regStep === 1 && (
              <>
                <OTPBoxes onChange={setRegOtp} />
                <button
                  disabled={loading}
                  onClick={handleVerifyRegOTP}
                  className={`${successBtn} ${disabledStyle}`}
                >
                  Verify Email
                </button>
              </>
            )}

            {regStep === 2 && (
              <>
                <InputField label="Password" type="password" onChange={setRegPassword} />
                <InputField label="Confirm Password" type="password" onChange={setRegConfirm} />
                <button
                  disabled={loading}
                  onClick={handleCreateAccount}
                  className={`${primaryBtn} ${disabledStyle}`}
                >
                  Create Account
                </button>
              </>
            )}
          </>
        )}

        {/* LOGIN */}
        {tab === "login" && (
          <>
            <StepIndicator step={loginStep} mode="login" />

            {loginStep === 0 && (
              <>
                <InputField label="Email" onChange={setLoginEmail} />
                <InputField label="Password" type="password" onChange={setLoginPassword} />

                <p
                  className="text-red-400 text-sm cursor-pointer mb-3"
                  onClick={() => {
                    setTab("forgot");
                    setFpStep(0);
                    resetMessages();
                  }}
                >
                  Forgot password?
                </p>

                <button
                  onClick={handleVerifyCredentials}
                  className={successBtn}
                >
                  Continue
                </button>
              </>
            )}

            {loginStep === 1 && (
              <>
                <OTPBoxes onChange={setLoginOtp} />
                <button
                  disabled={loading}
                  onClick={handleLogin}
                  className={`${successBtn} ${disabledStyle}`}
                >
                  Login
                </button>
              </>
            )}
          </>
        )}

        {/* FORGOT PASSWORD */}
        {tab === "forgot" && (
          <>
            {fpStep === 0 && (
              <>
                <InputField label="Email" onChange={setFpEmail} />
                <button
                  disabled={loading}
                  onClick={handleSendForgotOTP}
                  className={`${primaryBtn} ${disabledStyle}`}
                >
                  Send OTP
                </button>
              </>
            )}

            {fpStep === 1 && (
              <>
                <OTPBoxes onChange={setFpOtp} />
                <button
                  disabled={loading}
                  onClick={handleVerifyForgotOTP}
                  className={`${successBtn} ${disabledStyle}`}
                >
                  Verify OTP
                </button>
              </>
            )}

            {fpStep === 2 && (
              <>
                <InputField label="New Password" type="password" onChange={setFpPassword} />
                <InputField label="Confirm Password" type="password" onChange={setFpConfirm} />
                <button
                  disabled={loading}
                  onClick={handleResetPassword}
                  className={`${primaryBtn} ${disabledStyle}`}
                >
                  Reset Password
                </button>
              </>
            )}
          </>
        )}

        {error && <p className="text-red-400 text-sm mt-4 text-center">{error}</p>}
        {success && <p className="text-green-400 text-sm mt-4 text-center">{success}</p>}
      </AuthCard>
    </div>
  );
}
