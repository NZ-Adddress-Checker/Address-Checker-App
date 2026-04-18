function normalizeBaseUrl(value, fallback) {
  if (!value) {
    return fallback;
  }

  try {
    const parsed = new URL(value);
    return parsed.origin;
  } catch {
    return fallback;
  }
}

export const appConfig = {
  apiBaseUrl: normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL, "http://localhost:8000"),
  cognito: {
    domain: import.meta.env.VITE_COGNITO_DOMAIN || "",
    clientId: import.meta.env.VITE_COGNITO_CLIENT_ID || "",
    redirectUri: import.meta.env.VITE_COGNITO_REDIRECT_URI || "",
    scope: import.meta.env.VITE_COGNITO_SCOPE || "openid+email+profile",
  },
};

export function isCognitoConfigured() {
  const cfg = appConfig.cognito;
  return Boolean(cfg.domain && cfg.clientId && cfg.redirectUri && cfg.scope);
}
