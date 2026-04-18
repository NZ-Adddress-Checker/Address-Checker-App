import { getDomainOrigin } from "./cognitoUrls";
import { getPkceVerifier } from "./pkce";

export async function exchangeCodeForTokens({ domain, clientId, redirectUri, code }) {
  const codeVerifier = getPkceVerifier();
  if (!codeVerifier) {
    throw new Error("Missing PKCE code verifier. Start login again.");
  }

  const domainOrigin = getDomainOrigin(domain);
  const tokenUrl = new URL("/oauth2/token", domainOrigin);
  const body = new URLSearchParams({
    grant_type: "authorization_code",
    client_id: clientId,
    code,
    redirect_uri: redirectUri,
    code_verifier: codeVerifier,
  });

  const response = await fetch(tokenUrl.toString(), {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body.toString(),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error_description || data.error || "Token exchange failed");
  }

  return data;
}

export function parseAuthResult() {
  const queryParams = new URLSearchParams(window.location.search);

  return {
    code: queryParams.get("code"),
    state: queryParams.get("state"),
    error: queryParams.get("error"),
    errorDescription: queryParams.get("error_description"),
  };
}
