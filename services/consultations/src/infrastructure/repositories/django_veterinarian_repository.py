"""Implementação concreta do repositório de veterinários (Repository Pattern)."""

from typing import Optional

from src.domain.entities.veterinarian import Veterinarian
from src.domain.repositories.veterinarian_repository import IVeterinarianRepository
from src.infrastructure.database.models import VeterinarianModel


class DjangoVeterinarianRepository(IVeterinarianRepository):
    """Adaptador Django ORM para IVeterinarianRepository."""

    def _to_entity(self, model: VeterinarianModel) -> Veterinarian:
        return Veterinarian(
            id=model.id,
            user_id=model.user_id,
            full_name=model.full_name,
            crmv=model.crmv,
            specialty=model.specialty,
            created_at=model.created_at,
        )

    def save(self, veterinarian: Veterinarian) -> Veterinarian:
        model = VeterinarianModel.objects.create(
            user_id=veterinarian.user_id,
            full_name=veterinarian.full_name,
            crmv=veterinarian.crmv,
            specialty=veterinarian.specialty,
        )
        return self._to_entity(model)

    def find_by_id(self, veterinarian_id: int) -> Optional[Veterinarian]:
        try:
            model = VeterinarianModel.objects.get(id=veterinarian_id)
            return self._to_entity(model)
        except VeterinarianModel.DoesNotExist:
            return None

    def find_by_user_id(self, user_id: int) -> Optional[Veterinarian]:
        try:
            model = VeterinarianModel.objects.get(user_id=user_id)
            return self._to_entity(model)
        except VeterinarianModel.DoesNotExist:
            return None

    def crmv_exists(self, crmv: str) -> bool:
        return VeterinarianModel.objects.filter(crmv=crmv.strip()).exists()

    def list_all(self) -> list[Veterinarian]:
        return [self._to_entity(model) for model in VeterinarianModel.objects.all()]

    def exists(self, veterinarian_id: int) -> bool:
        return VeterinarianModel.objects.filter(id=veterinarian_id).exists()
