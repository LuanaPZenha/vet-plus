"""Garante 3 medicamentos demo no microsserviço de estoque."""

import os
from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from demo_seed import DEMO_MEDICINES
from src.infrastructure.database.models import MedicineModel


class Command(BaseCommand):
    help = "Cria 3 medicamentos demo se ainda não existirem (idempotente)."

    def handle(self, *args, **options):
        if os.environ.get("SKIP_DEMO_DATA", "").lower() in ("1", "true", "yes"):
            self.stdout.write("SKIP_DEMO_DATA definido — pulando seed de estoque.")
            return

        created = 0
        for item in DEMO_MEDICINES:
            if MedicineModel.objects.filter(name=item["name"]).exists():
                continue
            MedicineModel.objects.create(
                name=item["name"],
                generic_name=item["generic_name"],
                category=item["category"],
                unit=item["unit"],
                quantity=Decimal(item["quantity"]),
                min_stock=Decimal(item["min_stock"]),
                batch_number=item.get("batch_number"),
                expiration_date=(
                    date.fromisoformat(item["expiration_date"])
                    if item.get("expiration_date")
                    else None
                ),
                supplier=item.get("supplier"),
                unit_price=Decimal(item["unit_price"]) if item.get("unit_price") else None,
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"Medicamento demo criado: {item['name']}"))

        total = MedicineModel.objects.count()
        if created == 0:
            self.stdout.write(f"Medicamentos demo já existem ({total} no total).")
        else:
            self.stdout.write(
                self.style.SUCCESS(f"{created} medicamento(s) demo criado(s). Total: {total}")
            )
