const TOKEN_KEY = "auth_tokens";
const PKCE_VERIFIER_KEY = "pkce_code_verifier";
const PKCE_STATE_KEY = "pkce_state";

function readTokenStore() {
  const raw = localStorage.getItem(TOKEN_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch {
    localStorage.removeItem(TOKEN_KEY);
    return null;
  }
}

export function getToken() {
  const tokens = readTokenStore();
  return tokens?.idToken || tokens?.accessToken || null;
}

export function setToken(token) {
  if (!token) {
    clearToken();
    return;
  }

  setTokens({ access_token: token });
}

export function setTokens(tokens) {
  const tokenStore = {
    idToken: tokens.id_token || null,
    accessToken: tokens.access_token || null,
    refreshToken: tokens.refresh_token || null,
    tokenType: tokens.token_type || "Bearer",
    expiresIn: typeof tokens.expires_in === "number" ? tokens.expires_in : null,
    savedAt: Date.now(),
  };

  localStorage.setItem(TOKEN_KEY, JSON.stringify(tokenStore));
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

function toBase64Url(bytes) {
  const binary = String.fromCharCode(...bytes);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function randomString(length = 64) {
  const bytes = new Uint8Array(length);
  crypto.getRandomValues(bytes);
  return toBase64Url(bytes).slice(0, length);
}

async function sha256Base64Url(input) {
  const data = new TextEncoder().encode(input);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return toBase64Url(new Uint8Array(digest));
}

function getDomainOrigin(domain) {
  try {
    return new URL(domain).origin;
  } catch {
    throw new Error("VITE_COGNITO_DOMAIN must be a full URL");
  }
}

export async function buildPkceAuthorizeUrl({ domain, clientId, redirectUri, scope }) {
  if (!domain || !clientId || !redirectUri || !scope) {
    throw new Error("Missing Cognito configuration values");
  }

  const domainOrigin = getDomainOrigin(domain);

  const codeVerifier = randomString(96);
  const state = randomString(48);
  const codeChallenge = await sha256Base64Url(codeVerifier);

  sessionStorage.setItem(PKCE_VERIFIER_KEY, codeVerifier);
  sessionStorage.setItem(PKCE_STATE_KEY, state);

  const url = new URL("/oauth2/authorize", domainOrigin);
  url.searchParams.set("response_type", "code");
  url.searchParams.set("client_id", clientId);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("scope", scope.replace(/\+/g, " "));
  url.searchParams.set("code_challenge", codeChallenge);
  url.searchParams.set("code_challenge_method", "S256");
  url.searchParams.set("state", state);
  url.searchParams.set("prompt", "login");

  return url.toString();
}

export function validatePkceState(returnedState) {
  const expectedState = sessionStorage.getItem(PKCE_STATE_KEY);
  return Boolean(expectedState) && expectedState === returnedState;
}

export function clearPkceState() {
  sessionStorage.removeItem(PKCE_VERIFIER_KEY);
  sessionStorage.removeItem(PKCE_STATE_KEY);
}

export function resetLoginSession() {
  clearToken();
  clearPkceState();
}

export async function exchangeCodeForTokens({ domain, clientId, redirectUri, code }) {
  const codeVerifier = sessionStorage.getItem(PKCE_VERIFIER_KEY);
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

export function buildCognitoLogoutUrl({ domain, clientId, logoutUri }) {
  if (!domain || !clientId || !logoutUri) {
    throw new Error("Missing Cognito logout configuration values");
  }

  const domainOrigin = getDomainOrigin(domain);
  const url = new URL("/logout", domainOrigin);
  url.searchParams.set("client_id", clientId);
  url.searchParams.set("logout_uri", logoutUri);
  return url.toString();
}

export function parseAuthResult() {
  const hash = window.location.hash.replace(/^#/, "");
  const hashParams = new URLSearchParams(hash);
  const queryParams = new URLSearchParams(window.location.search);

  const error = hashParams.get("error") || queryParams.get("error");
  const errorDescription =
    hashParams.get("error_description") || queryParams.get("error_description");

  const token = hashParams.get("id_token") || hashParams.get("access_token");
  const code = queryParams.get("code");
  const state = queryParams.get("state");

  return {
    token,
    code,
    state,
    error,
    errorDescription,
  };
}

export function isAuthenticated() {
  return Boolean(getToken());
}
