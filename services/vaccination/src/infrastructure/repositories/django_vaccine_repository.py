"""Implementação concreta do repositório de vacinas (Repository Pattern)."""

from datetime import date, timedelta
from typing import Optional

from src.domain.entities.vaccine import Vaccine
from src.domain.repositories.vaccine_repository import IVaccineRepository
from src.infrastructure.database.models import VaccineModel


class DjangoVaccineRepository(IVaccineRepository):
    """Adaptador Django ORM para IVaccineRepository."""

    def _to_entity(self, model: VaccineModel) -> Vaccine:
        return Vaccine(
            id=model.id,
            animal_id=model.animal_id,
            vaccine_name=model.vaccine_name,
            application_date=model.application_date,
            next_dose_date=model.next_dose_date,
            veterinarian_id=model.veterinarian_id,
            batch_number=model.batch_number,
            notes=model.notes,
            created_at=model.created_at,
        )

    def save(self, vaccine: Vaccine) -> Vaccine:
        if vaccine.id:
            model = VaccineModel.objects.get(id=vaccine.id)
            model.animal_id = vaccine.animal_id
            model.vaccine_name = vaccine.vaccine_name
            model.application_date = vaccine.application_date
            model.next_dose_date = vaccine.next_dose_date
            model.veterinarian_id = vaccine.veterinarian_id
            model.batch_number = vaccine.batch_number
            model.notes = vaccine.notes
            model.save()
        else:
            model = VaccineModel.objects.create(
                animal_id=vaccine.animal_id,
                vaccine_name=vaccine.vaccine_name,
                application_date=vaccine.application_date,
                next_dose_date=vaccine.next_dose_date,
                veterinarian_id=vaccine.veterinarian_id,
                batch_number=vaccine.batch_number,
                notes=vaccine.notes,
            )
        return self._to_entity(model)

    def find_by_id(self, vaccine_id: int) -> Optional[Vaccine]:
        try:
            model = VaccineModel.objects.get(id=vaccine_id)
            return self._to_entity(model)
        except VaccineModel.DoesNotExist:
            return None

    def list_all(self, animal_id: int | None = None) -> list[Vaccine]:
        queryset = VaccineModel.objects.all()
        if animal_id is not None:
            queryset = queryset.filter(animal_id=animal_id)
        return [self._to_entity(model) for model in queryset]

    def find_by_animal_id(self, animal_id: int) -> list[Vaccine]:
        return self.list_all(animal_id=animal_id)

    def find_upcoming(self, within_days: int) -> list[Vaccine]:
        today = date.today()
        deadline = today + timedelta(days=within_days)
        queryset = VaccineModel.objects.filter(
            next_dose_date__isnull=False,
            next_dose_date__gte=today,
            next_dose_date__lte=deadline,
        )
        return [self._to_entity(model) for model in queryset]
