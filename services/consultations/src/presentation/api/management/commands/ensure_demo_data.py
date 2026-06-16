"""Garante 3 veterinários e 3 consultas demo."""

import os
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from demo_seed import DEMO_CONSULTATIONS, DEMO_VETERINARIANS
from demo_seed_utils import get_animal_id_by_name, get_user_id_by_email
from src.infrastructure.database.models import ConsultationModel, VeterinarianModel


class Command(BaseCommand):
    help = "Cria 3 veterinários e 3 consultas demo (idempotente)."

    def handle(self, *args, **options):
        if os.environ.get("SKIP_DEMO_DATA", "").lower() in ("1", "true", "yes"):
            self.stdout.write("SKIP_DEMO_DATA definido — pulando seed de consultas.")
            return

        vet_created = 0
        for index, item in enumerate(DEMO_VETERINARIANS):
            if VeterinarianModel.objects.filter(crmv=item["crmv"]).exists():
                continue
            user_id = get_user_id_by_email(item["user_email"], fallback=item["user_id"])
            VeterinarianModel.objects.create(
                user_id=user_id,
                full_name=item["full_name"],
                crmv=item["crmv"],
                specialty=item["specialty"],
            )
            vet_created += 1
            self.stdout.write(self.style.SUCCESS(f"Veterinário demo criado: {item['full_name']}"))

        consult_created = 0
        for index, item in enumerate(DEMO_CONSULTATIONS):
            animal_id = get_animal_id_by_name(item["animal_name"], fallback=index + 1)
            veterinarian = VeterinarianModel.objects.filter(crmv=item["veterinarian_crmv"]).first()
            if veterinarian is None:
                self.stdout.write(
                    self.style.WARNING(
                        f"Veterinário {item['veterinarian_crmv']} não encontrado — pulando consulta."
                    )
                )
                continue

            exists = ConsultationModel.objects.filter(
                animal_id=animal_id,
                veterinarian=veterinarian,
                scheduled_at=timezone.make_aware(datetime.fromisoformat(item["scheduled_at"])),
            ).exists()
            if exists:
                continue

            ConsultationModel.objects.create(
                animal_id=animal_id,
                veterinarian=veterinarian,
                scheduled_at=timezone.make_aware(datetime.fromisoformat(item["scheduled_at"])),
                type=item["type"],
                notes=item["notes"],
            )
            consult_created += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Consulta demo criada: {item['animal_name']} com {veterinarian.full_name}"
                )
            )

        if vet_created == 0 and consult_created == 0:
            self.stdout.write(
                "Consultas demo já existem "
                f"({VeterinarianModel.objects.count()} vets, "
                f"{ConsultationModel.objects.count()} consultas)."
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Seed consultas: +{vet_created} vet(s), +{consult_created} consulta(s)."
                )
            )
