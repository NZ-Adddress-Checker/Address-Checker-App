import { useCallback, useEffect, useState } from "react";
import {
  buildPkceAuthorizeUrl,
  consumeLoginRestartPending,
  useLogout,
} from "../auth/index.js";
import { AUTH_MESSAGES } from "../constants/authMessages";
import { appConfig, isCognitoConfigured } from "../config";

const { cognito } = appConfig;

export default function LoginPage() {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const logout = useLogout();

  const beginLogin = useCallback(async () => {
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
      setError(err instanceof Error ? err.message : AUTH_MESSAGES.startLoginFailed);
    }
  }, []);

  const onLogin = async () => {
    setError("");
    try {
      if (isCognitoConfigured()) {
        logout();
        return;
      }
      await beginLogin();
    } catch (err) {
      setLoading(false);
      setError(err instanceof Error ? err.message : AUTH_MESSAGES.startLoginFailed);
    }
  };

  useEffect(() => {
    if (!consumeLoginRestartPending()) {
      return;
    }
    void beginLogin();
  }, [beginLogin]);

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
