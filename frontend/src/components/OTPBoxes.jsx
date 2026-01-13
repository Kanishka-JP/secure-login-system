import { useRef } from "react";

export default function OTPBoxes({ onChange }) {
  const refs = Array.from({ length: 6 }, () => useRef());

  const handleChange = (i, val) => {
    if (!/^\d?$/.test(val)) return;
    refs[i].current.value = val;

    const code = refs.map(r => r.current.value).join("");
    onChange(code);

    if (val && refs[i + 1]) refs[i + 1].current.focus();
  };

  return (
    <div className="flex justify-between gap-2 my-4">
      {refs.map((ref, i) => (
        <input
          key={i}
          ref={ref}
          maxLength={1}
          className="w-12 h-12 text-center text-lg rounded-lg bg-slate-800 text-white border border-slate-600 focus:ring-2 focus:ring-green-500"
          onChange={(e) => handleChange(i, e.target.value)}
        />
      ))}
    </div>
  );
}
