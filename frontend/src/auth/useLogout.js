import { useNavigate } from "react-router-dom";
import { buildAppLogoutUrl } from "./cognitoUrls";
import { clearAuthSession, markLoginRestartPending } from "./session";
import { appConfig, isCognitoConfigured } from "../config";

/**
 * Returns a logout function that:
 * 1. Clears the local auth session.
 * 2. Redirects to the Cognito logout endpoint (marking a restart so login resumes after).
 * 3. Falls back to navigating to "/" if Cognito logout URL cannot be built.
 */
export function useLogout() {
  const navigate = useNavigate();

  return function logout() {
    clearAuthSession();

    if (isCognitoConfigured()) {
      try {
        const logoutUrl = buildAppLogoutUrl({
          domain: appConfig.cognito.domain,
          clientId: appConfig.cognito.clientId,
          redirectUri: appConfig.cognito.redirectUri,
        });
        markLoginRestartPending();
        window.location.assign(logoutUrl);
        return;
      } catch {
        // Fall back to local navigation if Cognito logout URL cannot be built.
      }
    }

    navigate("/", { replace: true });
  };
}
