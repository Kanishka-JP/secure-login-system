export default function WelcomePage({ onLogout }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 to-slate-900">
      <div className="bg-slate-900 p-10 rounded-2xl text-center border border-slate-700">
        <h1 className="text-4xl font-bold text-white mb-4">
          🎉 Welcome
        </h1>
        <p className="text-slate-400 mb-6">
          Login successful with 2-Factor Authentication
        </p>

        <button
          onClick={onLogout}
          className="px-6 py-3 bg-red-600 rounded-lg text-white"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
