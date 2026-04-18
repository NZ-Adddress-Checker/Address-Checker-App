FROM node:20-alpine AS build

WORKDIR /app

ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_COGNITO_DOMAIN=
ARG VITE_COGNITO_CLIENT_ID=
ARG VITE_COGNITO_REDIRECT_URI=http://localhost:8080/callback
ARG VITE_COGNITO_SCOPE=email+openid+phone

ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_COGNITO_DOMAIN=${VITE_COGNITO_DOMAIN}
ENV VITE_COGNITO_CLIENT_ID=${VITE_COGNITO_CLIENT_ID}
ENV VITE_COGNITO_REDIRECT_URI=${VITE_COGNITO_REDIRECT_URI}
ENV VITE_COGNITO_SCOPE=${VITE_COGNITO_SCOPE}

COPY frontend/package*.json ./
RUN npm ci

COPY frontend ./
RUN npm run build

FROM nginx:1.27-alpine

COPY docker/nginx.frontend.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
