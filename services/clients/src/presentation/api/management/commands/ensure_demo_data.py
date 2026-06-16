"""Garante 3 tutores demo no microsserviço de clientes."""

import os

from django.core.management.base import BaseCommand

from demo_seed import DEMO_CLIENTS
from src.infrastructure.database.models import ClientModel


class Command(BaseCommand):
    help = "Cria 3 tutores demo se ainda não existirem (idempotente)."

    def handle(self, *args, **options):
        if os.environ.get("SKIP_DEMO_DATA", "").lower() in ("1", "true", "yes"):
            self.stdout.write("SKIP_DEMO_DATA definido — pulando seed de clientes.")
            return

        created = 0
        for item in DEMO_CLIENTS:
            if ClientModel.objects.filter(email=item["email"]).exists():
                continue
            ClientModel.objects.create(
                full_name=item["full_name"],
                email=item["email"],
                phone=item["phone"],
                cpf=item["cpf"],
                address=item["address"],
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"Tutor demo criado: {item['full_name']}"))

        total = ClientModel.objects.count()
        if created == 0:
            self.stdout.write(f"Tutores demo já existem ({total} no total).")
        else:
            self.stdout.write(self.style.SUCCESS(f"{created} tutor(es) demo criado(s). Total: {total}"))
