"""Configuração do ambiente Behave para testes BDD."""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import django
import jwt
from django.conf import settings
from django.core.management import call_command

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR.parent.parent / "shared"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework.test import APIClient  # noqa: E402


def get_response_data(response):
    if hasattr(response, "data"):
        return response.data
    if response.content:
        return json.loads(response.content)
    return {}


def before_all(context):
    if "testserver" not in settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS.append("testserver")

    call_command("migrate", verbosity=0, interactive=False)

    context.base_url = os.environ.get("CLIENTS_BASE_URL", "")
    context.api_client = APIClient()
    context.last_response = None
    context.auth_headers = {}
    context.get_response_data = get_response_data


def before_scenario(context, scenario):
    context.last_response = None
    context.auth_headers = {}


def _make_jwt_token(role="veterinarian", email="vet@behave.com"):
    payload = {
        "user_id": 1,
        "email": email,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def set_auth_token(context, role="veterinarian", email="vet@behave.com"):
    token = _make_jwt_token(role=role, email=email)
    context.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
