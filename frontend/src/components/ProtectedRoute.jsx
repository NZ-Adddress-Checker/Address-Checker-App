import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { isAuthenticated } from "../auth/index.js";
import { checkUserAccess } from "../api";
import AccessDeniedPage from "./AccessDeniedPage";

export default function ProtectedRoute({ children }) {
  const [loading, setLoading] = useState(true);
  const [hasAccess, setHasAccess] = useState(false);
  const [username, setUsername] = useState(null);

  useEffect(() => {
    let isMounted = true;

    const verifyAccess = async () => {
      if (!isAuthenticated()) {
        setLoading(false);
        return;
      }

      try {
        const result = await checkUserAccess();
        if (isMounted) {
          setHasAccess(result.has_access);
          setUsername(result.username);
        }
      } catch (err) {
        if (!isMounted) return;
        // Deny access by default — only grant if we got an explicit `has_access: true`.
        if (err.response?.status === 403) {
          setHasAccess(false);
        } else {
          // Network/server errors: deny access and log for visibility.
          console.error("Access check failed — denying by default:", err);
          setHasAccess(false);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    void verifyAccess();

    return () => {
      isMounted = false;
    };
  }, []);

  if (!isAuthenticated()) {
    return <Navigate to="/" replace />;
  }

  if (loading) {
    return (
      <main className="screen">
        <section className="card">
          <p>Verifying access...</p>
        </section>
      </main>
    );
  }

  if (!hasAccess) {
    return <AccessDeniedPage username={username} />;
  }

  return children;
}
