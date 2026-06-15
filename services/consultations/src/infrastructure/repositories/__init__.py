"""Repositórios Django."""

from src.infrastructure.repositories.django_consultation_repository import DjangoConsultationRepository
from src.infrastructure.repositories.django_veterinarian_repository import DjangoVeterinarianRepository

__all__ = ["DjangoConsultationRepository", "DjangoVeterinarianRepository"]
