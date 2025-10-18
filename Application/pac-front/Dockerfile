# Stage 1: Build Vue app
FROM node:24 as builder

WORKDIR /app
COPY . .

ARG VITE_AUTH_API_URL
ENV VITE_AUTH_API_URL=$VITE_AUTH_API_URL
ARG VITE_AGENTIC_API_URL
ENV VITE_RECAPTCHA_SITE_KEY=$VITE_RECAPTCHA_SITE_KEY

RUN npm install && npm run build


# Stage 2: Serve with NGINX
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
