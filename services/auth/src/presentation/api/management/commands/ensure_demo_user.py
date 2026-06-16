"""Garante usuário demo para login inicial (Render / ambiente vazio)."""

import os

from django.core.management.base import BaseCommand

from src.infrastructure.database.models import UserModel


class Command(BaseCommand):
    help = "Cria o usuário demo se ainda não existir (idempotente)."

    def handle(self, *args, **options):
        if os.environ.get("SKIP_DEMO_USER", "").lower() in ("1", "true", "yes"):
            self.stdout.write("SKIP_DEMO_USER definido — pulando criação do usuário demo.")
            return

        email = os.environ.get("DEMO_ADMIN_EMAIL", "admin@vet.com")
        password = os.environ.get("DEMO_ADMIN_PASSWORD", "senha1234")
        full_name = os.environ.get("DEMO_ADMIN_NAME", "Admin Demo")

        if UserModel.objects.filter(email=email).exists():
            self.stdout.write(f"Usuário demo já existe: {email}")
            return

        UserModel.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            role=UserModel.Role.ADMIN,
            is_staff=True,
        )
        self.stdout.write(self.style.SUCCESS(f"Usuário demo criado: {email}"))
