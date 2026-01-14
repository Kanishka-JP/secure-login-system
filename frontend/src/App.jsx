import { useState } from "react";
import AuthPage from "./pages/AuthPage";
import WelcomePage from "./pages/WelcomePage";

export default function App() {
  const [email, setEmail] = useState(null);

  const token = localStorage.getItem("token");

  if (!token || !email) {
    return <AuthPage onLogin={setEmail} />;
  }

  return (
    <WelcomePage
      email={email}
      onLogout={() => {
        localStorage.removeItem("token");
        setEmail(null);
      }}
    />
  );
}
