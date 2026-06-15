#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PYTHONPATH="${ROOT}/services/auth:${ROOT}/shared:${PYTHONPATH:-}"
export ALLOWED_HOSTS="${ALLOWED_HOSTS:-.railway.app,localhost,127.0.0.1}"
export DEBUG="${DEBUG:-False}"

cd "${ROOT}/services/auth"

echo ">> Rodando migracoes..."
python manage.py migrate --noinput

echo ">> Iniciando API de autenticacao na porta ${PORT:-8000}..."
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 120
