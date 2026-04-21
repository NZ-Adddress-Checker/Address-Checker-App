import { Navigate } from "react-router-dom";
import { isAuthenticated, getUserGroups } from "../auth/index.js";

const REQUIRED_GROUP = "AddressValidators";

export default function ProtectedRoute({ children }) {
  if (!isAuthenticated()) {
    return <Navigate to="/" replace />;
  }

  if (!getUserGroups().includes(REQUIRED_GROUP)) {
    return (
      <div className="screen">
        <div className="card" style={{ textAlign: "center" }}>
          <h2 style={{ color: "var(--harbor-blue)", marginBottom: "0.5rem" }}>Access Denied</h2>
          <p style={{ color: "var(--ink)" }}>
            You do not have permission to access this page. Please contact your administrator.
          </p>
        </div>
      </div>
    );
  }

  return children;
}
