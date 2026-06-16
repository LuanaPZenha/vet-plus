"""Garante usuários demo para login e cadastro de veterinários."""

import os

from django.core.management.base import BaseCommand

from demo_seed import DEMO_USERS
from src.infrastructure.database.models import UserModel


class Command(BaseCommand):
    help = "Cria 3 usuários demo se ainda não existirem (idempotente)."

    def handle(self, *args, **options):
        if os.environ.get("SKIP_DEMO_USER", "").lower() in ("1", "true", "yes"):
            self.stdout.write("SKIP_DEMO_USER definido — pulando criação dos usuários demo.")
            return

        created = 0
        for item in DEMO_USERS:
            if UserModel.objects.filter(email=item["email"]).exists():
                continue
            UserModel.objects.create_user(
                email=item["email"],
                password=item["password"],
                full_name=item["full_name"],
                role=item["role"],
                is_staff=item["is_staff"],
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"Usuário demo criado: {item['email']}"))

        if created == 0:
            self.stdout.write(f"Usuários demo já existem ({UserModel.objects.count()} no total).")
        else:
            self.stdout.write(self.style.SUCCESS(f"{created} usuário(s) demo criado(s)."))
