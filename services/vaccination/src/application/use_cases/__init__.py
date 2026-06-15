"""Casos de uso - Vacinação."""

from src.application.use_cases.vaccine_use_cases import (
    CheckUpcomingVaccinesUseCase,
    GetVaccineHistoryUseCase,
    GetVaccineUseCase,
    ListVaccinesUseCase,
    RegisterVaccineUseCase,
    VaccineNotFoundError,
    VaccineRegistrationError,
)

__all__ = [
    "RegisterVaccineUseCase",
    "ListVaccinesUseCase",
    "GetVaccineUseCase",
    "GetVaccineHistoryUseCase",
    "CheckUpcomingVaccinesUseCase",
    "VaccineNotFoundError",
    "VaccineRegistrationError",
]
