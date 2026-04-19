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

# Install deps first — separate layer so it is cached on code-only changes.
COPY frontend/package*.json ./
RUN npm ci --prefer-offline

COPY frontend ./
RUN npm run build


FROM nginx:1.27-alpine

# Drop root privileges — nginx master still needs port 80, worker runs as nginx.
RUN chown -R nginx:nginx /var/cache/nginx /var/run /var/log/nginx

COPY docker/nginx.frontend.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
RUN chown -R nginx:nginx /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget -qO- http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
