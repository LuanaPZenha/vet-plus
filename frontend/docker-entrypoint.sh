#!/bin/sh
set -e

export PORT="${PORT:-10000}"

envsubst '${PORT} ${AUTH_URL} ${AUTH_HOST} ${CLIENTS_URL} ${CLIENTS_HOST} ${ANIMALS_URL} ${ANIMALS_HOST} ${CONSULTATIONS_URL} ${CONSULTATIONS_HOST} ${VACCINATION_URL} ${VACCINATION_HOST} ${INVENTORY_URL} ${INVENTORY_HOST}' \
  < /etc/nginx/templates/default.conf.template \
  > /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'
