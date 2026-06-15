"""Entidades de domínio."""

from src.domain.entities.consultation import Consultation, ConsultationStatus, ConsultationType
from src.domain.entities.veterinarian import Veterinarian

__all__ = [
    "Consultation",
    "ConsultationStatus",
    "ConsultationType",
    "Veterinarian",
]
