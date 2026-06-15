"""App Django para API de clientes."""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.presentation.api"
    label = "api"
