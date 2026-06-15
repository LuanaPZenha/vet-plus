"""Interfaces de repositório - Vacinas (Dependency Inversion)."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.vaccine import Vaccine


class IVaccineRepository(ABC):
    """Contrato para persistência de vacinas."""

    @abstractmethod
    def save(self, vaccine: Vaccine) -> Vaccine:
        pass

    @abstractmethod
    def find_by_id(self, vaccine_id: int) -> Optional[Vaccine]:
        pass

    @abstractmethod
    def list_all(self, animal_id: int | None = None) -> list[Vaccine]:
        pass

    @abstractmethod
    def find_by_animal_id(self, animal_id: int) -> list[Vaccine]:
        pass

    @abstractmethod
    def find_upcoming(self, within_days: int) -> list[Vaccine]:
        pass
