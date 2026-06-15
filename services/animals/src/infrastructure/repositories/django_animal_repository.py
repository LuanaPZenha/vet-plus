"""Implementação concreta do repositório de animais (Repository Pattern)."""

from typing import Optional

from src.domain.entities.animal import Animal
from src.domain.repositories.animal_repository import IAnimalRepository
from src.infrastructure.database.models import AnimalModel


class DjangoAnimalRepository(IAnimalRepository):
    """Adaptador Django ORM para IAnimalRepository."""

    def _to_entity(self, model: AnimalModel) -> Animal:
        weight = float(model.weight) if model.weight is not None else None
        return Animal(
            id=model.id,
            name=model.name,
            species=model.species,
            breed=model.breed,
            birth_date=model.birth_date,
            weight=weight,
            client_id=model.client_id,
            created_at=model.created_at,
        )

    def save(self, animal: Animal) -> Animal:
        model = AnimalModel.objects.create(
            name=animal.name,
            species=animal.species,
            breed=animal.breed,
            birth_date=animal.birth_date,
            weight=animal.weight,
            client_id=animal.client_id,
        )
        return self._to_entity(model)

    def find_by_id(self, animal_id: int) -> Optional[Animal]:
        try:
            model = AnimalModel.objects.get(id=animal_id)
            return self._to_entity(model)
        except AnimalModel.DoesNotExist:
            return None

    def list_all(self, client_id: int | None = None) -> list[Animal]:
        queryset = AnimalModel.objects.all()
        if client_id is not None:
            queryset = queryset.filter(client_id=client_id)
        return [self._to_entity(model) for model in queryset]

    def exists(self, animal_id: int) -> bool:
        return AnimalModel.objects.filter(id=animal_id).exists()
