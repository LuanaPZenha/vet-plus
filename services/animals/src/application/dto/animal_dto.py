"""DTOs - Animais."""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class CreateAnimalDTO:
    name: str
    species: str
    breed: str
    birth_date: date | None
    weight: float | None
    client_id: int


@dataclass
class AnimalResponseDTO:
    id: int
    name: str
    species: str
    breed: str
    birth_date: date | None
    weight: float | None
    client_id: int
    created_at: datetime


@dataclass
class AddMedicalHistoryDTO:
    animal_id: int
    description: str
    record_type: str


@dataclass
class MedicalHistoryResponseDTO:
    id: int
    animal_id: int
    description: str
    record_type: str
    created_at: datetime
