"""Facade Pattern - orquestração veterinária."""

from src.domain.patterns.facade.veterinary_service_facade import (
    AnimalNotFoundError,
    ConsultationCompletionError,
    ConsultationCompletionResult,
    VeterinaryServiceFacade,
)

__all__ = [
    "AnimalNotFoundError",
    "ConsultationCompletionError",
    "ConsultationCompletionResult",
    "VeterinaryServiceFacade",
]
