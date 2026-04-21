const TOKEN_KEY = "auth_tokens";

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

/**
 * Decodes a JWT payload safely, handling base64url encoding (no padding, - and _ chars).
 * Returns null if the token is malformed.
 */
function decodeJwtPayload(token) {
  try {
    const base64url = token.split(".")[1];
    // Convert base64url → base64 and restore padding
    const base64 = base64url.replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), "=");
    return JSON.parse(atob(padded));
  } catch {
    return null;
  }
}

function isTokenExpired() {
  const tokens = readTokenStore();
  if (!tokens?.expiresIn || !tokens?.savedAt) {
    return false;
  }
  const elapsedSeconds = (Date.now() - tokens.savedAt) / 1000;
  return elapsedSeconds >= tokens.expiresIn;
}

export function getToken() {
  const tokens = readTokenStore();
  return tokens?.idToken || tokens?.accessToken || null;
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

export function clearTokenStorage() {
  localStorage.removeItem(TOKEN_KEY);
}

export function isAuthenticated() {
  return Boolean(getToken()) && !isTokenExpired();
}

export function getUserGroups() {
  const tokens = readTokenStore();
  const idToken = tokens?.idToken;
  if (!idToken) return [];
  const payload = decodeJwtPayload(idToken);
  return payload?.["cognito:groups"] ?? [];
}
