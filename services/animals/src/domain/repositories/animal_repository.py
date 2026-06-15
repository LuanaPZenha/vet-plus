"""Interfaces de repositório - Animais (Dependency Inversion)."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.animal import Animal


class IAnimalRepository(ABC):
    """Contrato para persistência de animais."""

    @abstractmethod
    def save(self, animal: Animal) -> Animal:
        pass

    @abstractmethod
    def find_by_id(self, animal_id: int) -> Optional[Animal]:
        pass

    @abstractmethod
    def list_all(self, client_id: int | None = None) -> list[Animal]:
        pass

    @abstractmethod
    def exists(self, animal_id: int) -> bool:
        pass
