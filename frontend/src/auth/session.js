import { clearPkceState } from "./pkce";
import { clearTokenStorage } from "./tokenStorage";

export const RESTART_LOGIN_KEY = "restart_cognito_login";

export function clearAuthSession() {
  clearTokenStorage();
  clearPkceState();
}

export function markLoginRestartPending() {
  sessionStorage.setItem(RESTART_LOGIN_KEY, "true");
}

export function consumeLoginRestartPending() {
  if (sessionStorage.getItem(RESTART_LOGIN_KEY) !== "true") {
    return false;
  }

  sessionStorage.removeItem(RESTART_LOGIN_KEY);
  return true;
}
