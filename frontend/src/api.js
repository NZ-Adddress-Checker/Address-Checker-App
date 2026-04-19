import axios from "axios";
import { clearAuthSession, getToken } from "./auth/index.js";
import { appConfig } from "./config";

const api = axios.create({
  baseURL: appConfig.apiBaseUrl,
  timeout: 8000,
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401, clear session and reload to the login page.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearAuthSession();
      window.location.replace("/");
    }
    return Promise.reject(error);
  }
);

export async function checkAddress(address) {
  const response = await api.post("/address-check", { address });
  return response.data;
}

export async function getAddressSuggestions() {
  const response = await api.get("/address-suggestions");
  const items = response.data?.items;
  return Array.isArray(items) ? items : [];
}

export async function checkUserAccess() {
  const response = await api.get("/auth/check-access");
  return response.data;
}
