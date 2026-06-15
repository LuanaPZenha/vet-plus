"""Entidades de domínio - Histórico Médico."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MedicalRecordType(str, Enum):
    """Tipos de registro no histórico médico."""

    CONSULTATION = "consultation"
    VACCINATION = "vaccination"
    SURGERY = "surgery"
    EXAM = "exam"
    MEDICATION = "medication"
    NOTE = "note"


@dataclass
class MedicalHistoryEntry:
    """Entidade de entrada no histórico médico."""

    id: int | None
    animal_id: int
    description: str
    record_type: MedicalRecordType
    created_at: datetime | None = None

    def is_valid(self) -> bool:
        return bool(self.description.strip()) and self.animal_id > 0
