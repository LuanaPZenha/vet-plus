"""Implementação concreta do repositório de histórico médico (Repository Pattern)."""

from src.domain.entities.medical_history import MedicalHistoryEntry, MedicalRecordType
from src.domain.repositories.medical_history_repository import IMedicalHistoryRepository
from src.infrastructure.database.models import AnimalModel, MedicalHistoryModel


class DjangoMedicalHistoryRepository(IMedicalHistoryRepository):
    """Adaptador Django ORM para IMedicalHistoryRepository."""

    def _to_entity(self, model: MedicalHistoryModel) -> MedicalHistoryEntry:
        return MedicalHistoryEntry(
            id=model.id,
            animal_id=model.animal_id,
            description=model.description,
            record_type=MedicalRecordType(model.record_type),
            created_at=model.created_at,
        )

    def save(self, entry: MedicalHistoryEntry) -> MedicalHistoryEntry:
        animal = AnimalModel.objects.get(id=entry.animal_id)
        model = MedicalHistoryModel.objects.create(
            animal=animal,
            description=entry.description,
            record_type=entry.record_type.value,
        )
        return self._to_entity(model)

    def find_by_animal_id(self, animal_id: int) -> list[MedicalHistoryEntry]:
        queryset = MedicalHistoryModel.objects.filter(animal_id=animal_id)
        return [self._to_entity(model) for model in queryset]
