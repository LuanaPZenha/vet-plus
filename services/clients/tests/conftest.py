"""Configuração Pytest."""

import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR.parent.parent / "shared"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
