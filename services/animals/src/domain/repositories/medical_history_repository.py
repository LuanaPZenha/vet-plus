"""Interfaces de repositório - Histórico Médico (Dependency Inversion)."""

from abc import ABC, abstractmethod

from src.domain.entities.medical_history import MedicalHistoryEntry


class IMedicalHistoryRepository(ABC):
    """Contrato para persistência do histórico médico."""

    @abstractmethod
    def save(self, entry: MedicalHistoryEntry) -> MedicalHistoryEntry:
        pass

    @abstractmethod
    def find_by_animal_id(self, animal_id: int) -> list[MedicalHistoryEntry]:
        pass
