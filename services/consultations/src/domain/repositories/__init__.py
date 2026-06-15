"""Contratos de repositório."""

from src.domain.repositories.consultation_repository import IConsultationRepository
from src.domain.repositories.veterinarian_repository import IVeterinarianRepository

__all__ = ["IConsultationRepository", "IVeterinarianRepository"]
