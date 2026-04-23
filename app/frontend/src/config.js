const config = {
  cognito: {
    authority:
      process.env.REACT_APP_COGNITO_AUTHORITY ||
      "https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_2oQQDAKa4",
    clientId:
      process.env.REACT_APP_COGNITO_CLIENT_ID || "4p7i1nq2t426jufkh0pe7fgo2u",
    domain:
      process.env.REACT_APP_COGNITO_DOMAIN ||
      "https://ap-southeast-22oqqdaka4.auth.ap-southeast-2.amazoncognito.com",
    redirectUri:
      process.env.REACT_APP_REDIRECT_URI || "http://localhost:5002/callback",
    logoutUri:
      process.env.REACT_APP_LOGOUT_URI || "http://localhost:5002/",
    scope: "email openid phone",
  },
  api: {
    baseURL: process.env.REACT_APP_API_URL || "http://localhost:5001/api",
  },
};

export default config;
