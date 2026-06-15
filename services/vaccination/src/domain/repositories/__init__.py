"""Repositórios de domínio - Vacinação."""

from src.domain.repositories.vaccine_reminder_repository import IVaccineReminderRepository
from src.domain.repositories.vaccine_repository import IVaccineRepository

__all__ = ["IVaccineRepository", "IVaccineReminderRepository"]
