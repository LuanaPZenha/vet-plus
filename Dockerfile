# Deploy Render — frontend Vet Plus+ (React + nginx + APIs embutidas)
# URL principal: https://vet-plus.onrender.com

FROM node:20-alpine AS build

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend .
RUN npm run build

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx gettext libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /etc/nginx/sites-enabled/default

WORKDIR /app

COPY services/clients/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY shared /app/shared
COPY services/clients /app/services/clients
COPY services/animals /app/services/animals
COPY services/consultations /app/services/consultations
COPY services/vaccination /app/services/vaccination
COPY services/inventory /app/services/inventory

COPY --from=build /app/dist /usr/share/nginx/html

COPY frontend/nginx.render.conf.template /etc/nginx/templates/default.conf.template
COPY frontend/docker-entrypoint.sh /docker-entrypoint.sh
COPY frontend/start-api-services.sh /start-api-services.sh
RUN sed -i 's/\r$//' /docker-entrypoint.sh /start-api-services.sh \
    && chmod +x /docker-entrypoint.sh /start-api-services.sh

EXPOSE 10000

ENTRYPOINT ["/docker-entrypoint.sh"]
