"""DTOs - Consultas."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScheduleConsultationDTO:
    animal_id: int
    veterinarian_id: int
    scheduled_at: datetime
    type: str
    notes: str = ""


@dataclass
class CompleteConsultationDTO:
    consultation_id: int
    diagnosis: str
    prescription_notes: str = ""
    procedure: str = ""


@dataclass
class ConsultationResponseDTO:
    id: int
    animal_id: int
    veterinarian_id: int
    scheduled_at: datetime
    status: str
    type: str
    price: float | None
    notes: str
    diagnosis: str
    prescription: str
    created_at: datetime


@dataclass
class CreateVeterinarianDTO:
    user_id: int
    full_name: str
    crmv: str
    specialty: str


@dataclass
class VeterinarianResponseDTO:
    id: int
    user_id: int
    full_name: str
    crmv: str
    specialty: str
    created_at: datetime
