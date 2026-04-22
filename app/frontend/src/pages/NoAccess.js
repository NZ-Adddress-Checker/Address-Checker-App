import { useAuth } from "react-oidc-context";
import config from "../config";

export default function NoAccess() {
  const auth = useAuth();

  const handleLogout = () => {
    auth.removeUser();
    window.location.href = `${config.cognito.domain}/logout?client_id=${config.cognito.clientId}&logout_uri=${encodeURIComponent(config.cognito.logoutUri)}`;
  };

  return (
    <div style={{ padding: "24px", fontFamily: "sans-serif" }}>
      <h2>No access to this feature.</h2>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}
