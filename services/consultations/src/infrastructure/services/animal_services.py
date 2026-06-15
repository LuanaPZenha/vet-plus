"""Serviços de infraestrutura para integração com microsserviço de Animais."""

import logging
from typing import Optional

import requests
from django.conf import settings

from src.domain.services.animal_service import AnimalReference, IAnimalService, IMedicalHistoryService

logger = logging.getLogger(__name__)


class HttpAnimalService(IAnimalService):
    """Busca animais via API REST do microsserviço de Animais."""

    def __init__(self, base_url: str | None = None, auth_token: str | None = None):
        self._base_url = (base_url or settings.ANIMALS_SERVICE_URL).rstrip("/")
        self._auth_token = auth_token

    def get_animal(self, animal_id: int) -> Optional[AnimalReference]:
        headers = {}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"

        try:
            response = requests.get(
                f"{self._base_url}/api/animais/{animal_id}/",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            return AnimalReference(
                id=data["id"],
                name=data["name"],
                species=data["species"],
                client_id=data["client_id"],
            )
        except requests.RequestException as exc:
            logger.warning("Falha ao buscar animal %s: %s", animal_id, exc)
            return None


class HttpMedicalHistoryService(IMedicalHistoryService):
    """Atualiza histórico médico via API REST do microsserviço de Animais."""

    def __init__(self, base_url: str | None = None, auth_token: str | None = None):
        self._base_url = (base_url or settings.ANIMALS_SERVICE_URL).rstrip("/")
        self._auth_token = auth_token

    def add_record(self, animal_id: int, description: str, record_type: str) -> dict:
        headers = {"Content-Type": "application/json"}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"

        try:
            response = requests.post(
                f"{self._base_url}/api/animais/{animal_id}/historico/",
                json={"description": description, "record_type": record_type},
                headers=headers,
                timeout=5,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            logger.warning("Falha ao registrar histórico para animal %s: %s", animal_id, exc)
            return {
                "animal_id": animal_id,
                "description": description,
                "record_type": record_type,
                "source": "local_fallback",
            }


class InMemoryAnimalService(IAnimalService):
    """
    Implementação em memória para testes e desenvolvimento local.

    Aceita qualquer animal_id > 0 sem validação externa.
    """

    def __init__(self, animals: dict[int, AnimalReference] | None = None):
        self._animals = animals or {}

    def register_animal(self, animal: AnimalReference) -> None:
        self._animals[animal.id] = animal

    def get_animal(self, animal_id: int) -> Optional[AnimalReference]:
        if animal_id in self._animals:
            return self._animals[animal_id]
        if animal_id > 0:
            return AnimalReference(
                id=animal_id,
                name=f"Animal #{animal_id}",
                species="Não informado",
                client_id=1,
            )
        return None


class InMemoryMedicalHistoryService(IMedicalHistoryService):
    """Implementação em memória para testes - armazena registros localmente."""

    def __init__(self):
        self.records: list[dict] = []

    def add_record(self, animal_id: int, description: str, record_type: str) -> dict:
        entry = {
            "id": len(self.records) + 1,
            "animal_id": animal_id,
            "description": description,
            "record_type": record_type,
        }
        self.records.append(entry)
        return entry
