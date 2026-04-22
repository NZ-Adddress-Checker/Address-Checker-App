import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { AuthProvider } from "react-oidc-context";
import config from "./config";

const cognitoAuthConfig = {
  authority: config.cognito.authority,
  client_id: config.cognito.clientId,
  redirect_uri: config.cognito.redirectUri,
  response_type: "code",
  scope: config.cognito.scope,
};

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AuthProvider {...cognitoAuthConfig}>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
