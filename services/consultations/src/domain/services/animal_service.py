"""Portas de serviço externo usadas pelo Facade."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class AnimalReference:
    """Referência simplificada a um animal de outro microsserviço."""

    id: int
    name: str
    species: str
    client_id: int


class IAnimalService(ABC):
    """Porta para buscar dados de animais (microsserviço de Animais)."""

    @abstractmethod
    def get_animal(self, animal_id: int) -> Optional[AnimalReference]:
        """Retorna dados do animal ou None se não encontrado."""


class IMedicalHistoryService(ABC):
    """Porta para atualizar histórico médico (microsserviço de Animais)."""

    @abstractmethod
    def add_record(self, animal_id: int, description: str, record_type: str) -> dict:
        """Adiciona entrada ao histórico médico do animal."""
