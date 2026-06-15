"""Implementação concreta do repositório de consultas (Repository Pattern)."""

from typing import Optional

from src.domain.entities.consultation import Consultation, ConsultationStatus, ConsultationType
from src.domain.repositories.consultation_repository import IConsultationRepository
from src.infrastructure.database.models import ConsultationModel, VeterinarianModel


class DjangoConsultationRepository(IConsultationRepository):
    """Adaptador Django ORM para IConsultationRepository."""

    def _to_entity(self, model: ConsultationModel) -> Consultation:
        price = float(model.price) if model.price is not None else None
        return Consultation(
            id=model.id,
            animal_id=model.animal_id,
            veterinarian_id=model.veterinarian_id,
            scheduled_at=model.scheduled_at,
            status=ConsultationStatus(model.status),
            type=ConsultationType(model.type),
            price=price,
            notes=model.notes,
            diagnosis=model.diagnosis,
            prescription=model.prescription,
            created_at=model.created_at,
        )

    def save(self, consultation: Consultation) -> Consultation:
        veterinarian = VeterinarianModel.objects.get(id=consultation.veterinarian_id)
        model = ConsultationModel.objects.create(
            animal_id=consultation.animal_id,
            veterinarian=veterinarian,
            scheduled_at=consultation.scheduled_at,
            status=consultation.status.value,
            type=consultation.type.value,
            price=consultation.price,
            notes=consultation.notes,
            diagnosis=consultation.diagnosis,
            prescription=consultation.prescription,
        )
        return self._to_entity(model)

    def update(self, consultation: Consultation) -> Consultation:
        model = ConsultationModel.objects.get(id=consultation.id)
        model.status = consultation.status.value
        model.price = consultation.price
        model.diagnosis = consultation.diagnosis
        model.prescription = consultation.prescription
        model.notes = consultation.notes
        model.save()
        return self._to_entity(model)

    def find_by_id(self, consultation_id: int) -> Optional[Consultation]:
        try:
            model = ConsultationModel.objects.select_related("veterinarian").get(id=consultation_id)
            return self._to_entity(model)
        except ConsultationModel.DoesNotExist:
            return None

    def list_all(
        self,
        animal_id: int | None = None,
        veterinarian_id: int | None = None,
        status: ConsultationStatus | None = None,
    ) -> list[Consultation]:
        queryset = ConsultationModel.objects.select_related("veterinarian").all()
        if animal_id is not None:
            queryset = queryset.filter(animal_id=animal_id)
        if veterinarian_id is not None:
            queryset = queryset.filter(veterinarian_id=veterinarian_id)
        if status is not None:
            queryset = queryset.filter(status=status.value)
        return [self._to_entity(model) for model in queryset]

    def exists(self, consultation_id: int) -> bool:
        return ConsultationModel.objects.filter(id=consultation_id).exists()
