"""Serviços de infraestrutura para integração com microsserviço de Animais."""

from animal_client import (
    AnimalReference,
    HttpAnimalService,
    HttpMedicalHistoryService,
    IAnimalService,
    IMedicalHistoryService,
    InMemoryAnimalService,
    InMemoryMedicalHistoryService,
)

__all__ = [
    "AnimalReference",
    "HttpAnimalService",
    "HttpMedicalHistoryService",
    "IAnimalService",
    "IMedicalHistoryService",
    "InMemoryAnimalService",
    "InMemoryMedicalHistoryService",
]
