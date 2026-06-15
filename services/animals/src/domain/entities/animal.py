"""Entidades de domínio - Animais."""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Animal:
    """Entidade de animal do domínio."""

    id: int | None
    name: str
    species: str
    breed: str
    birth_date: date | None
    weight: float | None
    client_id: int
    created_at: datetime | None = None

    def is_valid(self) -> bool:
        return bool(self.name.strip()) and bool(self.species.strip()) and self.client_id > 0
