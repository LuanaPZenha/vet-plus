"""Entidades de domínio - Clientes."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Client:
    """Entidade de cliente (tutor) do domínio."""

    id: int | None
    full_name: str
    email: str
    phone: str
    cpf: str
    address: str
    created_at: datetime | None = None

    def has_contact_info(self) -> bool:
        return bool(self.email or self.phone)
