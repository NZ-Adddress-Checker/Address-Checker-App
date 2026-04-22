import axios from "axios";
import config from "../config";

const api = axios.create({
  baseURL: config.api.baseURL,
});

export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
}

export default api;
