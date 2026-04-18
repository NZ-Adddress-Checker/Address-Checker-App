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
  return Boolean(getToken());
}
