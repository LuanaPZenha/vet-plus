#!/bin/sh
set -e

export PORT="${PORT:-10000}"

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

cat > /usr/share/nginx/html/config.js <<EOF
window.__VET_PLUS_ENV__ = {
  AUTH_URL: "${AUTH_URL}",
  CLIENTS_URL: "${CLIENTS_URL}",
  ANIMALS_URL: "${ANIMALS_URL}",
  CONSULTATIONS_URL: "${CONSULTATIONS_URL}",
  VACCINATION_URL: "${VACCINATION_URL}",
  INVENTORY_URL: "${INVENTORY_URL}"
};
EOF

envsubst '${PORT}' \
  < /etc/nginx/templates/default.conf.template \
  > /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'
