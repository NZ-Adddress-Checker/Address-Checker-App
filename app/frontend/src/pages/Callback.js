import { useEffect } from "react";
import { useAuth } from "react-oidc-context";
import { useNavigate } from "react-router-dom";

export default function Callback() {
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.isLoading) return;

    if (auth.error) {
      navigate("/");
      return;
    }

    if (auth.isAuthenticated) {
      const groups = auth.user?.profile?.["cognito:groups"] || [];
      if (groups.includes("AddressValidators")) {
        navigate("/dashboard");
      } else {
        navigate("/no-access");
      }
    } else {
      // Loading finished but not authenticated — direct navigation or failed callback
      navigate("/");
    }
  }, [auth.isLoading, auth.isAuthenticated, auth.error, navigate]);

  return <p>Logging in...</p>;
}
