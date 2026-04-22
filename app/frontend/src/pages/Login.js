import { useEffect } from "react";
import { useAuth } from "react-oidc-context";
import config from "../config";

export default function Login() {
  const auth = useAuth();

  useEffect(() => {
    if (auth.isLoading) return; // wait until OIDC client is fully initialised
    if (localStorage.getItem("autostart") === "1") {
      localStorage.removeItem("autostart");
      auth.signinRedirect();
    }
  }, [auth]);

  const handleStart = () => {
    // Only remove an existing user — safe to skip on a fresh context
    if (!auth.isLoading && auth.isAuthenticated) {
      auth.removeUser();
    }
    localStorage.setItem("autostart", "1");
    window.location.href = `${config.cognito.domain}/logout?client_id=${config.cognito.clientId}&logout_uri=${encodeURIComponent(config.cognito.logoutUri)}`;
  };

  return (
    <div style={{
      minHeight: "100vh",
      backgroundImage: "url('https://flagcdn.com/w2560/nz.jpg')",
      backgroundSize: "cover",
      backgroundPosition: "center",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
    }}>
      <div style={{
        backgroundColor: "rgba(0, 0, 0, 0.55)",
        borderRadius: "12px",
        padding: "48px 64px",
        textAlign: "center",
      }}>
        <h1 style={{ color: "white", fontSize: "2rem", marginBottom: "28px", fontFamily: "sans-serif" }}>
          Welcome to NZ address validator
        </h1>
        <button onClick={handleStart}>Start</button>
      </div>
    </div>
  );
}
