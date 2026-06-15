"""Configuração Behave para Auth Service."""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

def before_all(context):
    context.base_url = os.environ.get("AUTH_BASE_URL", "http://localhost:8001")
