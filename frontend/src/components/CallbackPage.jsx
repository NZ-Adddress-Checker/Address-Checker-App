import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  clearPkceState,
  exchangeCodeForTokens,
  parseAuthResult,
  setToken,
  setTokens,
  validatePkceState,
} from "../auth";
import { appConfig, isCognitoConfigured } from "../config";

const { cognito } = appConfig;

function toFriendlyCognitoError(error, errorDescription) {
  const details = [error, errorDescription].filter(Boolean).join(" ").toLowerCase();

  if (details.includes("invalid challenge transition")) {
    return "Cognito user state is out of sync (invalid challenge transition). In AWS Cognito, set the user to CONFIRMED with a permanent password, then sign out of Cognito and try login again.";
  }

  if (details.includes("unauthorized_client")) {
    return "Cognito app client is not allowed for this OAuth flow. Enable Authorization code grant and verify callback URL settings.";
  }

  if (error || errorDescription) {
    return `Cognito returned an error: ${error}${
      errorDescription ? ` (${errorDescription})` : ""
    }`;
  }

  return "Cognito returned an unknown error. Check user state and app client OAuth settings.";
}

export default function CallbackPage() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("Signing you in...");

  useEffect(() => {
    const run = async () => {
      if (!isCognitoConfigured()) {
        setMessage("Cognito is not configured. Verify frontend environment values.");
        return;
      }

      const result = parseAuthResult();

      if (result.error) {
        setMessage(toFriendlyCognitoError(result.error, result.errorDescription));
        return;
      }

      if (result.code) {
        if (!validatePkceState(result.state)) {
          setMessage("Invalid login state. Please try signing in again.");
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
          setMessage(err instanceof Error ? err.message : "Token exchange failed");
          return;
        }
      }

      if (result.token) {
        setToken(result.token);
        navigate("/address", { replace: true });
        return;
      }

      setMessage("No token or authorization code was returned. Check callback URL and OAuth settings.");
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
