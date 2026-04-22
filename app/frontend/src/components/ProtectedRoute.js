import { useAuth } from "react-oidc-context";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const auth = useAuth();
  if (auth.isLoading) return <p>Loading...</p>;
  if (!auth.isAuthenticated) return <Navigate to="/" />;
  return children;
}
