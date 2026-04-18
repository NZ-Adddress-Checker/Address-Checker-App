import { getDomainOrigin } from "./cognitoUrls";

const PKCE_VERIFIER_KEY = "pkce_code_verifier";
const PKCE_STATE_KEY = "pkce_state";

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

export async function buildPkceAuthorizeUrl({ domain, clientId, redirectUri, scope, isSignUp = false }) {
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
  url.searchParams.set("prompt", isSignUp ? "signup" : "login");

  return url.toString();
}

export function getPkceVerifier() {
  return sessionStorage.getItem(PKCE_VERIFIER_KEY);
}

export function validatePkceState(returnedState) {
  const expectedState = sessionStorage.getItem(PKCE_STATE_KEY);
  return Boolean(expectedState) && expectedState === returnedState;
}

export function clearPkceState() {
  sessionStorage.removeItem(PKCE_VERIFIER_KEY);
  sessionStorage.removeItem(PKCE_STATE_KEY);
}
