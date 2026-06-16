#!/bin/sh
set -e

export PORT="${PORT:-10000}"
export AUTH_URL="${AUTH_URL:-https://vet-plus-auth.onrender.com}"
export AUTH_HOST="${AUTH_HOST:-vet-plus-auth.onrender.com}"
export AUTH_URL="${AUTH_URL%/}"
export AUTH_VERIFY_URL="${AUTH_VERIFY_URL:-${AUTH_URL}/api/verify-token/}"

. /start-api-services.sh

cat > /usr/share/nginx/html/config.js <<EOF
window.__VET_PLUS_ENV__ = {
  USE_API_PROXY: true,
  AUTH_URL: "${AUTH_URL}",
  BUILD_SHA: "${RENDER_GIT_COMMIT:-desconhecido}"
};
EOF

envsubst '${PORT} ${AUTH_URL} ${AUTH_HOST}' \
  < /etc/nginx/templates/default.conf.template \
  > /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'
