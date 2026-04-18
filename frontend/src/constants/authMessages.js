export const AUTH_MESSAGES = {
  cognitoNotConfigured: "Cognito is not configured. Verify frontend environment values.",
  loginConfigMissing:
    "Cognito is not configured. Set VITE_COGNITO_DOMAIN, VITE_COGNITO_CLIENT_ID, VITE_COGNITO_REDIRECT_URI, and VITE_COGNITO_SCOPE in frontend/.env.",
  invalidLoginState: "Invalid login state. Please try signing in again.",
  noAuthResult: "No token or authorization code was returned. Check callback URL and OAuth settings.",
  tokenExchangeFailed: "Token exchange failed",
  startLoginFailed: "Unable to start Cognito login",
  invalidSession: "Your session is invalid or expired. Please log in again.",
  requestTimedOut: "The validation request timed out. Try again.",
  addressValidationFailed: "Address validation failed. Please try again.",
  emptyAddress: "Please enter an address.",
  invalidChallengeTransition:
    "Cognito user state is out of sync (invalid challenge transition). In AWS Cognito, set the user to CONFIRMED with a permanent password, then sign out of Cognito and try login again.",
  unauthorizedClient:
    "Cognito app client is not allowed for this OAuth flow. Enable Authorization code grant and verify callback URL settings.",
  unknownCognitoError:
    "Cognito returned an unknown error. Check user state and app client OAuth settings.",
};

export function getFriendlyCognitoErrorMessage(error, errorDescription) {
  const details = [error, errorDescription].filter(Boolean).join(" ").toLowerCase();

  if (details.includes("invalid challenge transition")) {
    return AUTH_MESSAGES.invalidChallengeTransition;
  }

  if (details.includes("unauthorized_client")) {
    return AUTH_MESSAGES.unauthorizedClient;
  }

  if (error || errorDescription) {
    return `Cognito returned an error: ${error}${
      errorDescription ? ` (${errorDescription})` : ""
    }`;
  }

  return AUTH_MESSAGES.unknownCognitoError;
}
