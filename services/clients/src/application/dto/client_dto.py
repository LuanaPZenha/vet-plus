"""DTOs - Clientes."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateClientDTO:
    full_name: str
    email: str
    phone: str
    cpf: str
    address: str


@dataclass
class ClientResponseDTO:
    id: int
    full_name: str
    email: str
    phone: str
    cpf: str
    address: str
    created_at: datetime
