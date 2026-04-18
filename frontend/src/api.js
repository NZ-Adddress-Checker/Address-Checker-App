import axios from "axios";
import { getToken } from "./auth/index.js";
import { appConfig } from "./config";

const api = axios.create({
  baseURL: appConfig.apiBaseUrl,
  timeout: 3000,
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function checkAddress(address) {
  const response = await api.post("/address-check", { address });
  return response.data;
}
