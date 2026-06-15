"""DTOs - Vacinação."""

from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class RegisterVaccineDTO:
    animal_id: int
    vaccine_name: str
    application_date: date
    next_dose_date: date | None
    veterinarian_id: int
    batch_number: str | None
    notes: str | None


@dataclass
class VaccineResponseDTO:
    id: int
    animal_id: int
    vaccine_name: str
    application_date: date
    next_dose_date: date | None
    veterinarian_id: int
    batch_number: str | None
    notes: str | None
    created_at: datetime


@dataclass
class UpcomingVaccineDTO:
    id: int
    animal_id: int
    vaccine_name: str
    next_dose_date: date
    days_until_due: int
