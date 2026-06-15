"""Repositórios de infraestrutura - Vacinação."""

from src.infrastructure.repositories.django_vaccine_reminder_repository import (
    DjangoVaccineReminderRepository,
)
from src.infrastructure.repositories.django_vaccine_repository import DjangoVaccineRepository

__all__ = ["DjangoVaccineRepository", "DjangoVaccineReminderRepository"]
