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
    <div>
      <button onClick={handleStart}>Start</button>
    </div>
  );
}
