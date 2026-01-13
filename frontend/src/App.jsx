import { useState } from "react";
import AuthPage from "./pages/AuthPage";
import WelcomePage from "./pages/WelcomePage";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  return loggedIn ? (
    <WelcomePage onLogout={() => setLoggedIn(false)} />
  ) : (
    <AuthPage onLogin={() => setLoggedIn(true)} />
  );
}
