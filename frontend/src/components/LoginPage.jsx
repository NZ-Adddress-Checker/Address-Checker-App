import { useState } from "react";
import { buildCognitoLogoutUrl, buildPkceAuthorizeUrl, resetLoginSession } from "../auth";
import { appConfig, isCognitoConfigured } from "../config";

const { cognito } = appConfig;

export default function LoginPage() {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionReset, setSessionReset] = useState(false);

  const onLogin = async () => {
    setError("");
    try {
      setLoading(true);
      const loginUrl = await buildPkceAuthorizeUrl({
        domain: cognito.domain,
        clientId: cognito.clientId,
        redirectUri: cognito.redirectUri,
        scope: cognito.scope,
      });
      window.location.assign(loginUrl);
    } catch (err) {
      setLoading(false);
      setError(err instanceof Error ? err.message : "Unable to start Cognito login");
    }
  };

  const onResetSession = () => {
    resetLoginSession();
    setError("");
    setSessionReset(true);

    if (isCognitoConfigured()) {
      try {
        const redirectUrl = new URL(cognito.redirectUri);
        const logoutUri = `${redirectUrl.origin}/`;
        const logoutUrl = buildCognitoLogoutUrl({
          domain: cognito.domain,
          clientId: cognito.clientId,
          logoutUri,
        });
        window.location.assign(logoutUrl);
        return;
      } catch {
        // Ignore malformed logout configuration and keep local reset behavior.
      }
    }
  };

  return (
    <main className="screen login-screen">
      <section className="card login-card">
        <h1>NZ Address Checker</h1>
        {isCognitoConfigured() ? (
          <button type="button" className="button" onClick={onLogin} disabled={loading}>
            {loading ? "Redirecting..." : "Login"}
          </button>
        ) : (
          <p className="error">
            Cognito is not configured. Set VITE_COGNITO_DOMAIN, VITE_COGNITO_CLIENT_ID,
            VITE_COGNITO_REDIRECT_URI, and VITE_COGNITO_SCOPE in frontend/.env.
          </p>
        )}
        {error && <p className="error">{error}</p>}
        {sessionReset && <p>Login session reset. If prompted, sign in again.</p>}
      </section>
      <button type="button" className="reset-login-button" onClick={onResetSession}>
        Reset login session
      </button>
    </main>
  );
}
