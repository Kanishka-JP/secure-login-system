import { useState } from "react";
import { registerUser, verify2FA, loginUser } from "../api/auth";

import AuthCard from "../components/AuthCard";
import InputField from "../components/InputField";
import OTPBoxes from "../components/OTPBoxes";
import StepIndicator from "../components/StepIndicator";

export default function AuthPage({ onLogin }) {
  const [step, setStep] = useState(0);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [qr, setQr] = useState(null);
  const [error, setError] = useState("");

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 to-slate-900 px-4">
      <AuthCard>
        <h1 className="text-2xl font-bold text-center text-white">
          Secure Login
        </h1>
        <p className="text-center text-slate-400 mb-6">
          Two-Factor Authentication
        </p>

        <StepIndicator step={step} />

        <InputField label="Email" onChange={setEmail} />
        <InputField label="Password" type="password" onChange={setPassword} />

        {step > 0 && <OTPBoxes onChange={setOtp} />}

        {qr && step === 1 && (
          <div className="flex justify-center my-4 bg-white p-2 rounded">
            <img src={qr} className="w-40" />
          </div>
        )}

        {error && (
          <p className="text-red-400 text-sm text-center mb-3">{error}</p>
        )}

        {step === 0 && (
          <button
            onClick={async () => {
              try {
                const r = await registerUser(email, password);
                setQr(`data:image/png;base64,${r.data.qr_code_base64}`);
                setStep(1);
              } catch {
                setError("Registration failed");
              }
            }}
            className="w-full py-3 bg-blue-600 rounded-lg text-white"
          >
            Register
          </button>
        )}

        {step === 1 && (
          <button
            onClick={async () => {
              try {
                await verify2FA(email, otp);
                setStep(2);
              } catch {
                setError("Invalid OTP");
              }
            }}
            className="w-full py-3 bg-green-600 rounded-lg text-white"
          >
            Verify 2FA
          </button>
        )}

        {step === 2 && (
          <button
            onClick={async () => {
              try {
                await loginUser(email, password, otp);
                onLogin();
              } catch {
                setError("Login failed");
              }
            }}
            className="w-full py-3 bg-purple-600 rounded-lg text-white"
          >
            Login
          </button>
        )}
      </AuthCard>
    </div>
  );
}
