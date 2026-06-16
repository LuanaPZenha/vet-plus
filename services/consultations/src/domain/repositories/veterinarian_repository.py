"""Contratos de repositório - Veterinários (Repository Pattern)."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.veterinarian import Veterinarian


class IVeterinarianRepository(ABC):
    """
    Interface do repositório de veterinários.

    Repository Pattern: desacopla a camada de domínio da infraestrutura
    de persistência, facilitando testes com repositórios em memória.
    """

    @abstractmethod
    def save(self, veterinarian: Veterinarian) -> Veterinarian:
        """Persiste um novo veterinário."""

    @abstractmethod
    def find_by_id(self, veterinarian_id: int) -> Optional[Veterinarian]:
        """Busca veterinário por ID."""

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Veterinarian]:
        """Busca veterinário pelo ID do usuário autenticado."""

    @abstractmethod
    def crmv_exists(self, crmv: str) -> bool:
        """Verifica se o CRMV já está cadastrado."""

    @abstractmethod
    def list_all(self) -> list[Veterinarian]:
        """Lista todos os veterinários."""

    @abstractmethod
    def exists(self, veterinarian_id: int) -> bool:
        """Verifica se o veterinário existe."""
