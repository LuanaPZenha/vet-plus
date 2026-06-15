"""Contratos de repositório - Consultas (Repository Pattern)."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.consultation import Consultation, ConsultationStatus


class IConsultationRepository(ABC):
    """
    Interface do repositório de consultas.

    Repository Pattern: abstrai a persistência, permitindo trocar
    Django ORM, MongoDB ou qualquer outro mecanismo sem alterar o domínio.
    """

    @abstractmethod
    def save(self, consultation: Consultation) -> Consultation:
        """Persiste uma nova consulta."""

    @abstractmethod
    def update(self, consultation: Consultation) -> Consultation:
        """Atualiza uma consulta existente."""

    @abstractmethod
    def find_by_id(self, consultation_id: int) -> Optional[Consultation]:
        """Busca consulta por ID."""

    @abstractmethod
    def list_all(
        self,
        animal_id: int | None = None,
        veterinarian_id: int | None = None,
        status: ConsultationStatus | None = None,
    ) -> list[Consultation]:
        """Lista consultas com filtros opcionais."""

    @abstractmethod
    def exists(self, consultation_id: int) -> bool:
        """Verifica se a consulta existe."""
