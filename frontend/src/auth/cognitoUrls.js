export function getDomainOrigin(domain) {
  try {
    return new URL(domain).origin;
  } catch {
    throw new Error("VITE_COGNITO_DOMAIN must be a full URL");
  }
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

export function buildAppLogoutUrl({ domain, clientId, redirectUri }) {
  const logoutUri = `${new URL(redirectUri).origin}/`;
  return buildCognitoLogoutUrl({ domain, clientId, logoutUri });
}
