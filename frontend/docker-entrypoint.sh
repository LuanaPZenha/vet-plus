#!/bin/sh
set -e

export PORT="${PORT:-10000}"

# Defaults para Render (evita nginx crash quando env vars não estão configuradas)
export AUTH_URL="${AUTH_URL:-https://vet-plus-auth.onrender.com}"
export CLIENTS_URL="${CLIENTS_URL:-https://vet-plus-clients.onrender.com}"
export ANIMALS_URL="${ANIMALS_URL:-https://vet-plus-animals.onrender.com}"
export CONSULTATIONS_URL="${CONSULTATIONS_URL:-https://vet-plus-consultations.onrender.com}"
export VACCINATION_URL="${VACCINATION_URL:-https://vet-plus-vaccination.onrender.com}"
export INVENTORY_URL="${INVENTORY_URL:-https://vet-plus-inventory.onrender.com}"

export AUTH_URL="${AUTH_URL%/}"
export CLIENTS_URL="${CLIENTS_URL%/}"
export ANIMALS_URL="${ANIMALS_URL%/}"
export CONSULTATIONS_URL="${CONSULTATIONS_URL%/}"
export VACCINATION_URL="${VACCINATION_URL%/}"
export INVENTORY_URL="${INVENTORY_URL%/}"

export AUTH_HOST="${AUTH_HOST:-${AUTH_URL#https://}}"
export AUTH_HOST="${AUTH_HOST#http://}"
export AUTH_HOST="${AUTH_HOST%%/*}"

export CLIENTS_HOST="${CLIENTS_HOST:-${CLIENTS_URL#https://}}"
export CLIENTS_HOST="${CLIENTS_HOST#http://}"
export CLIENTS_HOST="${CLIENTS_HOST%%/*}"

export ANIMALS_HOST="${ANIMALS_HOST:-${ANIMALS_URL#https://}}"
export ANIMALS_HOST="${ANIMALS_HOST#http://}"
export ANIMALS_HOST="${ANIMALS_HOST%%/*}"

export CONSULTATIONS_HOST="${CONSULTATIONS_HOST:-${CONSULTATIONS_URL#https://}}"
export CONSULTATIONS_HOST="${CONSULTATIONS_HOST#http://}"
export CONSULTATIONS_HOST="${CONSULTATIONS_HOST%%/*}"

export VACCINATION_HOST="${VACCINATION_HOST:-${VACCINATION_URL#https://}}"
export VACCINATION_HOST="${VACCINATION_HOST#http://}"
export VACCINATION_HOST="${VACCINATION_HOST%%/*}"

export INVENTORY_HOST="${INVENTORY_HOST:-${INVENTORY_URL#https://}}"
export INVENTORY_HOST="${INVENTORY_HOST#http://}"
export INVENTORY_HOST="${INVENTORY_HOST%%/*}"

envsubst '${PORT} ${AUTH_URL} ${AUTH_HOST} ${CLIENTS_URL} ${CLIENTS_HOST} ${ANIMALS_URL} ${ANIMALS_HOST} ${CONSULTATIONS_URL} ${CONSULTATIONS_HOST} ${VACCINATION_URL} ${VACCINATION_HOST} ${INVENTORY_URL} ${INVENTORY_HOST}' \
  < /etc/nginx/templates/default.conf.template \
  > /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'
