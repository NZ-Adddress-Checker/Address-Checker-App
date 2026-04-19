import { useNavigate } from "react-router-dom";
import { buildAppLogoutUrl, clearAuthSession } from "../auth/index.js";
import { appConfig, isCognitoConfigured } from "../config";

/**
 * Shared logout hook — clears the local session then redirects to Cognito
 * logout (if configured) or falls back to the app root.
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
        window.location.assign(logoutUrl);
        return;
      } catch {
        // Fall back to local redirect if Cognito logout URL cannot be built.
      }
    }

    navigate("/", { replace: true });
  };
}
