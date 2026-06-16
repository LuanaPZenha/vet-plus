"""Configuração base Django para microsserviços Vet Plus+."""

import os
from pathlib import Path

import dj_database_url


def get_base_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def get_database_config(base_dir: Path, db_schema: str | None = None) -> dict:
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        config = dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
        if db_schema:
            config.setdefault("OPTIONS", {})
            config["OPTIONS"]["options"] = f"-c search_path={db_schema},public"
        return {"default": config}
    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": base_dir / "db.sqlite3",
        }
    }


def get_allowed_hosts() -> list[str]:
    """Hosts permitidos: env ALLOWED_HOSTS + hostname do Render + defaults."""
    defaults = [
        "localhost",
        "127.0.0.1",
        ".onrender.com",
        ".railway.app",
        "vet-plus.onrender.com",
    ]
    render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if render_hostname:
        defaults.append(render_hostname)
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if render_url.startswith("https://"):
        defaults.append(render_url.removeprefix("https://").split("/")[0])
    env_value = os.environ.get("ALLOWED_HOSTS", "")
    from_env = [h.strip() for h in env_value.split(",") if h.strip()]
    return list(dict.fromkeys(from_env + defaults))


def get_csrf_trusted_origins() -> list[str]:
    """Origens confiáveis para CSRF (Render + frontend local)."""
    origins = [
        "https://vet-plus.onrender.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    for key in ("RENDER_EXTERNAL_URL", "FRONTEND_URL"):
        value = os.environ.get(key, "").rstrip("/")
        if value:
            origins.append(value)
    extra = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
    origins.extend(item.strip() for item in extra.split(",") if item.strip())
    return list(dict.fromkeys(origins))


def get_common_settings(
    base_dir: Path,
    service_name: str,
    db_schema: str | None = None,
) -> dict:
    secret_key = os.environ.get("SECRET_KEY", "dev-insecure-key")
    debug = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")
    allowed_hosts = get_allowed_hosts()

    return {
        "SECRET_KEY": secret_key,
        "DEBUG": debug,
        "ALLOWED_HOSTS": allowed_hosts,
        "CSRF_TRUSTED_ORIGINS": get_csrf_trusted_origins(),
        "INSTALLED_APPS": [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "rest_framework",
            "drf_spectacular",
        ],
        "MIDDLEWARE": [
            "shared.cors_middleware.CorsMiddleware",
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        "ROOT_URLCONF": "config.urls",
        "TEMPLATES": [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ],
        "WSGI_APPLICATION": "config.wsgi.application",
        "DATABASES": get_database_config(base_dir, db_schema=db_schema),
        "AUTH_PASSWORD_VALIDATORS": [
            {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
            {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
            {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
        ],
        "LANGUAGE_CODE": "pt-br",
        "TIME_ZONE": "America/Sao_Paulo",
        "USE_I18N": True,
        "USE_TZ": True,
        "STATIC_URL": "static/",
        "DEFAULT_AUTO_FIELD": "django.db.models.BigAutoField",
        "REST_FRAMEWORK": {
            "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
            "DEFAULT_AUTHENTICATION_CLASSES": [],
            "DEFAULT_PERMISSION_CLASSES": [],
        },
        "SPECTACULAR_SETTINGS": {
            "TITLE": f"Vet Plus+ - {service_name}",
            "DESCRIPTION": f"API REST do microsserviço {service_name}",
            "VERSION": "1.0.0",
            "SERVE_INCLUDE_SCHEMA": False,
        },
    }
