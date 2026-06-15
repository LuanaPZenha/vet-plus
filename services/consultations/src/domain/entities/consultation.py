"""Entidades de domínio - Consultas."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ConsultationStatus(str, Enum):
    """Status possíveis de uma consulta."""

    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ConsultationType(str, Enum):
    """Tipos de consulta que determinam estratégia de preço e registro médico."""

    REGULAR = "regular"
    EMERGENCY = "emergency"
    SURGERY = "surgery"


@dataclass
class Consultation:
    """Entidade de consulta veterinária."""

    id: int | None
    animal_id: int
    veterinarian_id: int
    scheduled_at: datetime
    status: ConsultationStatus
    type: ConsultationType
    price: float | None = None
    notes: str = ""
    diagnosis: str = ""
    prescription: str = ""
    created_at: datetime | None = None

    def is_valid(self) -> bool:
        return self.animal_id > 0 and self.veterinarian_id > 0

    def can_complete(self) -> bool:
        return self.status == ConsultationStatus.SCHEDULED
