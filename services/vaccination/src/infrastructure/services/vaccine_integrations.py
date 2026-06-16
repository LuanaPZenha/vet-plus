"""Integração do microsserviço de vacinação com animais."""

from animal_client import HttpAnimalService, HttpMedicalHistoryService


def get_animal_service(auth_token: str | None = None) -> HttpAnimalService:
    return HttpAnimalService(auth_token=auth_token)


def get_medical_history_service(auth_token: str | None = None) -> HttpMedicalHistoryService:
    return HttpMedicalHistoryService(auth_token=auth_token)
