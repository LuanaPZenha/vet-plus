"""Utilitários para resolver IDs entre schemas/microsserviços no seed demo."""

from __future__ import annotations

import os

from django.db import connection


def _uses_postgres() -> bool:
    return os.environ.get("DATABASE_URL", "").startswith("postgres")


def get_client_id_by_email(email: str, fallback: int) -> int:
    if not _uses_postgres():
        return fallback
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM clients.clients WHERE email = %s", [email])
        row = cursor.fetchone()
    return row[0] if row else fallback


def get_animal_id_by_name(name: str, fallback: int) -> int:
    if not _uses_postgres():
        return fallback
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM animals.animals WHERE name = %s", [name])
        row = cursor.fetchone()
    return row[0] if row else fallback


def get_veterinarian_id_by_crmv(crmv: str, fallback: int) -> int:
    if not _uses_postgres():
        return fallback
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM consultations.veterinarians WHERE crmv = %s", [crmv])
        row = cursor.fetchone()
    return row[0] if row else fallback


def get_user_id_by_email(email: str, fallback: int) -> int:
    if not _uses_postgres():
        return fallback
    with connection.cursor() as cursor:
        cursor.execute('SELECT id FROM public.users WHERE email = %s', [email])
        row = cursor.fetchone()
    return row[0] if row else fallback
