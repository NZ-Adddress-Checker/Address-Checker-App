import { useEffect, useState } from "react";
import {
  buildAppLogoutUrl,
  buildPkceAuthorizeUrl,
  clearAuthSession,
  consumeLoginRestartPending,
  markLoginRestartPending,
} from "../auth/index.js";
import { AUTH_MESSAGES } from "../constants/authMessages";
import { appConfig, isCognitoConfigured } from "../config";

const { cognito } = appConfig;

export default function LoginPage() {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const beginLogin = async (isSignUp = false) => {
    setError("");
    try {
      setLoading(true);
      const loginUrl = await buildPkceAuthorizeUrl({
        domain: cognito.domain,
        clientId: cognito.clientId,
        redirectUri: cognito.redirectUri,
        scope: cognito.scope,
        isSignUp,
      });
      window.location.assign(loginUrl);
    } catch (err) {
      setLoading(false);
      setError(err instanceof Error ? err.message : AUTH_MESSAGES.startLoginFailed);
    }
  };

  const onLogin = async () => {
    setError("");

    try {
      if (isCognitoConfigured()) {
        clearAuthSession();
        markLoginRestartPending();
        window.location.assign(
          buildAppLogoutUrl({
            domain: cognito.domain,
            clientId: cognito.clientId,
            redirectUri: cognito.redirectUri,
          })
        );
        return;
      }

      await beginLogin(false);
    } catch (err) {
      consumeLoginRestartPending();
      setLoading(false);
      setError(err instanceof Error ? err.message : AUTH_MESSAGES.startLoginFailed);
    }
  };

  useEffect(() => {
    if (!consumeLoginRestartPending()) {
      return;
    }

    void beginLogin(false);
  }, []);

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
            {AUTH_MESSAGES.loginConfigMissing}
          </p>
        )}
        {error && <p className="error">{error}</p>}
      </section>
    </main>
  );
}
