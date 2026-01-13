const steps = ["Register", "Verify 2FA", "Login"];

export default function StepIndicator({ step }) {
  return (
    <div className="flex justify-between mb-6 text-sm">
      {steps.map((s, i) => (
        <span
          key={s}
          className={i === step ? "text-blue-400 font-semibold" : "text-slate-500"}
        >
          {s}
        </span>
      ))}
    </div>
  );
}
