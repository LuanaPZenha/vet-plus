"""Configuração Pytest."""

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import django
import jwt
import pytest
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR.parent.parent / "shared"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def make_jwt_token(
    user_id: int = 1,
    email: str = "vet@test.com",
    role: str = "veterinarian",
) -> str:
    """Gera token JWT para testes."""
    expiration = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": expiration,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


@pytest.fixture
def auth_headers():
    token = make_jwt_token()
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture
def tutor_auth_headers():
    token = make_jwt_token(user_id=10, email="tutor@test.com", role="tutor")
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}
