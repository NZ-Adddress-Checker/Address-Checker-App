import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  clearPkceState,
  exchangeCodeForTokens,
  parseAuthResult,
  setTokens,
  validatePkceState,
} from "../auth";
import {
  AUTH_MESSAGES,
  getFriendlyCognitoErrorMessage,
} from "../constants/authMessages";
import { appConfig, isCognitoConfigured } from "../config";

const { cognito } = appConfig;

export default function CallbackPage() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("Signing you in...");

  useEffect(() => {
    const run = async () => {
      if (!isCognitoConfigured()) {
        setMessage(AUTH_MESSAGES.cognitoNotConfigured);
        return;
      }

      const result = parseAuthResult();

      if (result.error) {
        setMessage(getFriendlyCognitoErrorMessage(result.error, result.errorDescription));
        return;
      }

      if (result.code) {
        if (!validatePkceState(result.state)) {
          setMessage(AUTH_MESSAGES.invalidLoginState);
          return;
        }

        try {
          const tokens = await exchangeCodeForTokens({
            domain: cognito.domain,
            clientId: cognito.clientId,
            redirectUri: cognito.redirectUri,
            code: result.code,
          });
          setTokens(tokens);
          clearPkceState();
          navigate("/address", { replace: true });
          return;
        } catch (err) {
          setMessage(err instanceof Error ? err.message : AUTH_MESSAGES.tokenExchangeFailed);
          return;
        }
      }

      setMessage(AUTH_MESSAGES.noAuthResult);
    };

    run();
  }, [navigate]);

  return (
    <main className="screen">
      <section className="card">
        <h1>{message}</h1>
      </section>
    </main>
  );
}
