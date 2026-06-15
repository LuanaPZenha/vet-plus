"""Interfaces de repositório - Clientes (Dependency Inversion)."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.client import Client


class IClientRepository(ABC):
    """Contrato para persistência de clientes."""

    @abstractmethod
    def save(self, client: Client) -> Client:
        pass

    @abstractmethod
    def find_by_id(self, client_id: int) -> Optional[Client]:
        pass

    @abstractmethod
    def find_all(self) -> list[Client]:
        pass

    @abstractmethod
    def email_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def cpf_exists(self, cpf: str) -> bool:
        pass
