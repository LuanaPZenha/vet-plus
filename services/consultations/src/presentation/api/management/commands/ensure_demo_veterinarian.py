"""Garante veterinário demo para agendamento inicial (Docker / Render)."""

import os

from django.core.management.base import BaseCommand
from django.db import ProgrammingError, connection

from src.infrastructure.database.models import VeterinarianModel


class Command(BaseCommand):
    help = "Cria o veterinário demo se ainda não existir (idempotente)."

    def handle(self, *args, **options):
        if os.environ.get("SKIP_DEMO_VETERINARIAN", "").lower() in ("1", "true", "yes"):
            self.stdout.write("SKIP_DEMO_VETERINARIAN definido — pulando criação do veterinário demo.")
            return

        if not self._veterinarians_table_ready():
            self.stdout.write(
                self.style.WARNING(
                    "Tabela veterinarians indisponível — execute migrate antes do seed demo."
                )
            )
            return

        user_id = int(os.environ.get("DEMO_VET_USER_ID", "1"))
        full_name = os.environ.get("DEMO_VET_NAME", "Dr. Admin Vet")
        crmv = os.environ.get("DEMO_VET_CRMV", "SP-10001")
        specialty = os.environ.get("DEMO_VET_SPECIALTY", "Clínica Geral")

        try:
            if VeterinarianModel.objects.filter(user_id=user_id).exists():
                self.stdout.write(f"Veterinário demo já existe para user_id={user_id}")
                return

            if VeterinarianModel.objects.filter(crmv=crmv).exists():
                self.stdout.write(f"CRMV demo já cadastrado: {crmv}")
                return

            VeterinarianModel.objects.create(
                user_id=user_id,
                full_name=full_name,
                crmv=crmv,
                specialty=specialty,
            )
        except ProgrammingError:
            self.stdout.write(
                self.style.WARNING("Não foi possível criar veterinário demo — tabela indisponível.")
            )
            return

        self.stdout.write(self.style.SUCCESS(f"Veterinário demo criado: {full_name} ({crmv})"))

    @staticmethod
    def _veterinarians_table_ready() -> bool:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT to_regclass(current_schema() || '.veterinarians') IS NOT NULL"
                )
                return bool(cursor.fetchone()[0])
        except ProgrammingError:
            return False
