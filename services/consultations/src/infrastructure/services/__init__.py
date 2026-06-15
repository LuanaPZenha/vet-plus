"""Serviços de integração."""

from src.infrastructure.services.animal_services import (
    HttpAnimalService,
    HttpMedicalHistoryService,
    InMemoryAnimalService,
    InMemoryMedicalHistoryService,
)

__all__ = [
    "HttpAnimalService",
    "HttpMedicalHistoryService",
    "InMemoryAnimalService",
    "InMemoryMedicalHistoryService",
]
