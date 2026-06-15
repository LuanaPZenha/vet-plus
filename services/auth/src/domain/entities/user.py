"""Entidades de domínio - Autenticação."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """Papéis de usuário no sistema."""

    ADMIN = "admin"
    VETERINARIAN = "veterinarian"
    TUTOR = "tutor"


@dataclass
class User:
    """Entidade de usuário do domínio."""

    id: int | None
    email: str
    full_name: str
    role: UserRole
    is_active: bool = True
    created_at: datetime | None = None

    def can_manage_patients(self) -> bool:
        return self.role in (UserRole.ADMIN, UserRole.VETERINARIAN)

    def can_schedule_appointments(self) -> bool:
        return self.role in (UserRole.ADMIN, UserRole.TUTOR, UserRole.VETERINARIAN)
