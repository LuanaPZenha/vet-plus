"""Implementação concreta do repositório de clientes (Repository Pattern)."""

from typing import Optional

from src.domain.entities.client import Client
from src.domain.repositories.client_repository import IClientRepository
from src.infrastructure.database.models import ClientModel


class DjangoClientRepository(IClientRepository):
    """Adaptador Django ORM para IClientRepository."""

    def _to_entity(self, model: ClientModel) -> Client:
        return Client(
            id=model.id,
            full_name=model.full_name,
            email=model.email,
            phone=model.phone,
            cpf=model.cpf,
            address=model.address,
            created_at=model.created_at,
        )

    def save(self, client: Client) -> Client:
        model = ClientModel.objects.create(
            full_name=client.full_name,
            email=client.email,
            phone=client.phone,
            cpf=client.cpf,
            address=client.address,
        )
        return self._to_entity(model)

    def find_by_id(self, client_id: int) -> Optional[Client]:
        try:
            model = ClientModel.objects.get(id=client_id)
            return self._to_entity(model)
        except ClientModel.DoesNotExist:
            return None

    def find_all(self) -> list[Client]:
        return [self._to_entity(model) for model in ClientModel.objects.all()]

    def email_exists(self, email: str) -> bool:
        return ClientModel.objects.filter(email=email).exists()

    def cpf_exists(self, cpf: str) -> bool:
        return ClientModel.objects.filter(cpf=cpf).exists()
