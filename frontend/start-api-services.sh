#!/bin/sh
set -e

export SECRET_KEY="${SECRET_KEY:-dev-insecure-key}"
export DEBUG="${DEBUG:-False}"
export ALLOWED_HOSTS="${ALLOWED_HOSTS:-.onrender.com,localhost,127.0.0.1}"
export ANIMALS_SERVICE_URL="${ANIMALS_SERVICE_URL:-http://127.0.0.1:8003}"
export AUTH_VERIFY_URL="${AUTH_VERIFY_URL:-}"
export DEMO_VET_USER_ID="${DEMO_VET_USER_ID:-1}"

start_service() {
  port="$1"
  dir="$2"
  schema="$3"
  cd "/app/services/$dir"
  export PYTHONPATH="/app/services/$dir:/app:/app/shared"
  if [ -n "$schema" ] && [ -n "$DATABASE_URL" ]; then
    python /app/shared/prepare_postgres_schema.py "$schema"
  fi
  python manage.py migrate --noinput
  if [ "$dir" = "consultations" ]; then
    python manage.py ensure_demo_veterinarian || echo "ensure_demo_veterinarian: ignorado (tabela ainda não pronta)"
  fi
  gunicorn config.wsgi:application \
    --bind "127.0.0.1:${port}" \
    --workers 1 \
    --threads 1 \
    --worker-class sync \
    --timeout 120 \
    --worker-tmp-dir /dev/shm \
    >/tmp/gunicorn-${dir}.log 2>&1 &
  echo $! > "/tmp/gunicorn-${dir}.pid"
  echo "API ${dir} listening on 127.0.0.1:${port}"
}

start_service 8002 clients clients
start_service 8003 animals animals
start_service 8004 consultations consultations
start_service 8005 vaccination vaccination
start_service 8006 inventory inventory

sleep 2
