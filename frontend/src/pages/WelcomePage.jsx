export default function WelcomePage({ email, onLogout }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 to-slate-900">
      <div className="bg-slate-900 p-10 rounded-2xl text-center border border-slate-700">
        <h1 className="text-4xl font-bold text-white mb-4">
          🎉 Welcome
        </h1>

        <p className="text-slate-300 mb-2">
          Hello,
          <span className="font-semibold text-white">
            {" "}{email}
          </span>
        </p>

        <p className="text-slate-400 mb-6">
          You have successfully logged in using
          Two-Factor Authentication.
        </p>

        <button
          onClick={onLogout}
          className="px-6 py-3 bg-red-600 hover:bg-red-700 transition rounded-lg text-white"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
