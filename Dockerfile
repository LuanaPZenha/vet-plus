# Deploy Render — frontend Vet Plus+ (nginx + proxy para microsserviços)
# URL principal: https://vet-plus.onrender.com

FROM node:20-alpine AS build

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend .
RUN npm run build

FROM nginx:1.27-alpine

RUN apk add --no-cache gettext

COPY frontend/nginx.render.conf.template /etc/nginx/templates/default.conf.template
COPY frontend/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 10000

ENTRYPOINT ["/docker-entrypoint.sh"]
