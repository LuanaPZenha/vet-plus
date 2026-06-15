"""Entidades de domínio - Veterinários."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Veterinarian:
    """Entidade de veterinário vinculado a um usuário do sistema."""

    id: int | None
    user_id: int
    full_name: str
    crmv: str
    specialty: str
    created_at: datetime | None = None

    def is_valid(self) -> bool:
        return (
            self.user_id > 0
            and bool(self.full_name.strip())
            and bool(self.crmv.strip())
            and bool(self.specialty.strip())
        )
