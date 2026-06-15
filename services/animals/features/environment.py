"""Configuração do ambiente Behave."""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR.parent.parent / "shared"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()


def before_all(context):
    from django.core.management import call_command
    from django.test.runner import DiscoverRunner

    context.test_runner = DiscoverRunner(verbosity=0, interactive=False)
    context.test_runner.setup_test_environment()
    context.db_config = context.test_runner.setup_databases()
    call_command("migrate", verbosity=0, interactive=False)


def before_scenario(context, scenario):
    from rest_framework.test import APIClient

    context.client = APIClient()
    context.last_response = None
    context.last_animal_id = None


def after_scenario(context, scenario):
    context.client = None
    context.last_response = None


def after_all(context):
    context.test_runner.teardown_databases(context.db_config)
    context.test_runner.teardown_test_environment()
