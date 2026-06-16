"""Garante 3 vacinas demo no microsserviço de vacinação."""

import os
from datetime import date

from django.core.management.base import BaseCommand

from demo_seed import DEMO_VACCINES
from demo_seed_utils import get_animal_id_by_name, get_veterinarian_id_by_crmv
from src.infrastructure.database.models import VaccineModel


class Command(BaseCommand):
    help = "Cria 3 vacinas demo se ainda não existirem (idempotente)."

    def handle(self, *args, **options):
        if os.environ.get("SKIP_DEMO_DATA", "").lower() in ("1", "true", "yes"):
            self.stdout.write("SKIP_DEMO_DATA definido — pulando seed de vacinas.")
            return

        created = 0
        for index, item in enumerate(DEMO_VACCINES):
            animal_id = get_animal_id_by_name(item["animal_name"], fallback=index + 1)
            veterinarian_id = get_veterinarian_id_by_crmv(
                item["veterinarian_crmv"],
                fallback=index + 1,
            )

            exists = VaccineModel.objects.filter(
                animal_id=animal_id,
                vaccine_name=item["vaccine_name"],
                application_date=date.fromisoformat(item["application_date"]),
            ).exists()
            if exists:
                continue

            next_dose = item.get("next_dose_date")
            VaccineModel.objects.create(
                animal_id=animal_id,
                vaccine_name=item["vaccine_name"],
                application_date=date.fromisoformat(item["application_date"]),
                next_dose_date=date.fromisoformat(next_dose) if next_dose else None,
                veterinarian_id=veterinarian_id,
                batch_number=item.get("batch_number"),
                notes=item.get("notes"),
            )
            created += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Vacina demo criada: {item['vaccine_name']} — {item['animal_name']}"
                )
            )

        total = VaccineModel.objects.count()
        if created == 0:
            self.stdout.write(f"Vacinas demo já existem ({total} no total).")
        else:
            self.stdout.write(self.style.SUCCESS(f"{created} vacina(s) demo criada(s). Total: {total}"))
