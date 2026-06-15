"""Interfaces de repositório - Autenticação (Dependency Inversion)."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User


class IUserRepository(ABC):
    """Contrato para persistência de usuários."""

    @abstractmethod
    def save(self, user: User, password: str) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def verify_password(self, email: str, password: str) -> bool:
        pass

    @abstractmethod
    def email_exists(self, email: str) -> bool:
        pass
