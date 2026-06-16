"""Garante 3 animais demo no microsserviço de animais."""

import os
from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from demo_seed import DEMO_ANIMALS
from demo_seed_utils import get_client_id_by_email
from src.infrastructure.database.models import AnimalModel


class Command(BaseCommand):
    help = "Cria 3 animais demo se ainda não existirem (idempotente)."

    def handle(self, *args, **options):
        if os.environ.get("SKIP_DEMO_DATA", "").lower() in ("1", "true", "yes"):
            self.stdout.write("SKIP_DEMO_DATA definido — pulando seed de animais.")
            return

        created = 0
        for index, item in enumerate(DEMO_ANIMALS):
            if AnimalModel.objects.filter(name=item["name"]).exists():
                continue
            client_id = get_client_id_by_email(item["client_email"], fallback=index + 1)
            AnimalModel.objects.create(
                name=item["name"],
                species=item["species"],
                breed=item["breed"],
                birth_date=date.fromisoformat(item["birth_date"]),
                weight=Decimal(item["weight"]),
                client_id=client_id,
            )
            created += 1
            self.stdout.write(
                self.style.SUCCESS(f"Animal demo criado: {item['name']} (tutor #{client_id})")
            )

        total = AnimalModel.objects.count()
        if created == 0:
            self.stdout.write(f"Animais demo já existem ({total} no total).")
        else:
            self.stdout.write(self.style.SUCCESS(f"{created} animal(is) demo criado(s). Total: {total}"))
