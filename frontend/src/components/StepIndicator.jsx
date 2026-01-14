export default function StepIndicator({ step, mode }) {
  const steps =
    mode === "register"
      ? ["Email", "Verify Email", "Create Password"]
      : ["Credentials", "2FA"];

  return (
    <div className="flex justify-between mb-6">
      {steps.map((label, index) => (
        <div key={index} className="flex-1 text-center">
          <div
            className={`w-8 h-8 mx-auto rounded-full flex items-center justify-center text-sm font-bold
              ${
                step >= index
                  ? "bg-blue-600 text-white"
                  : "bg-slate-700 text-slate-400"
              }`}
          >
            {index + 1}
          </div>
          <p className="text-xs mt-2 text-slate-400">{label}</p>
        </div>
      ))}
    </div>
  );
}
