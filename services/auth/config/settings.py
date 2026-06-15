"""Configuração Django - Microsserviço de Autenticação."""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
_shared_dir = BASE_DIR / "shared"
if not _shared_dir.exists():
    _shared_dir = BASE_DIR.parent.parent / "shared"
sys.path.insert(0, str(_shared_dir))

from django_settings import get_common_settings  # noqa: E402

_settings = get_common_settings(BASE_DIR, "Autenticação")
globals().update(_settings)

INSTALLED_APPS = _settings["INSTALLED_APPS"] + ["src.presentation.api.apps.ApiConfig"]

AUTH_USER_MODEL = "api.UserModel"

REST_FRAMEWORK = {
    **_settings["REST_FRAMEWORK"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}

JWT_EXPIRATION_HOURS = 24
