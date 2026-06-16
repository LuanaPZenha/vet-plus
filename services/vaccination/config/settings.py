"""Configuração Django - Microsserviço de Vacinação."""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
_shared_dir = BASE_DIR / "shared"
if not _shared_dir.exists():
    _shared_dir = BASE_DIR.parent.parent / "shared"
sys.path.insert(0, str(_shared_dir))

from django_settings import get_common_settings  # noqa: E402

_settings = get_common_settings(BASE_DIR, "Vacinação", db_schema="vaccination")
globals().update(_settings)

INSTALLED_APPS = _settings["INSTALLED_APPS"] + ["src.presentation.api"]

REST_FRAMEWORK = {
    **_settings["REST_FRAMEWORK"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "jwt_auth.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

VACCINE_REMINDER_DAYS_AHEAD = int(
    __import__("os").environ.get("VACCINE_REMINDER_DAYS_AHEAD", "7")
)

ANIMALS_SERVICE_URL = __import__("os").environ.get("ANIMALS_SERVICE_URL", "http://127.0.0.1:8003")
