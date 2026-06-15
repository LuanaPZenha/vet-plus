"""Testes unitários - DjangoClientRepository."""

import pytest

from src.domain.entities.client import Client
from src.infrastructure.repositories.django_client_repository import DjangoClientRepository


@pytest.mark.django_db
class TestDjangoClientRepository:
    """TDD: Persistência de clientes via Django ORM."""

    def test_save_and_find_by_id(self):
        repository = DjangoClientRepository()
        client = Client(
            id=None,
            full_name="João Tutor",
            email="joao@test.com",
            phone="11988887777",
            cpf="987.654.321-00",
            address="Av. Principal, 50",
        )

        saved = repository.save(client)
        found = repository.find_by_id(saved.id)

        assert found is not None
        assert found.full_name == "João Tutor"
        assert found.email == "joao@test.com"

    def test_find_all_returns_clients(self):
        repository = DjangoClientRepository()
        client = Client(
            id=None,
            full_name="Ana Costa",
            email="ana@test.com",
            phone="11977776666",
            cpf="111.222.333-44",
            address="Rua B, 20",
        )
        repository.save(client)

        results = repository.find_all()
        assert len(results) >= 1
        assert any(c.email == "ana@test.com" for c in results)

    def test_email_exists(self):
        repository = DjangoClientRepository()
        client = Client(
            id=None,
            full_name="Pedro Lima",
            email="pedro@test.com",
            phone="11966665555",
            cpf="555.666.777-88",
            address="Rua C, 30",
        )
        repository.save(client)

        assert repository.email_exists("pedro@test.com") is True
        assert repository.email_exists("naoexiste@test.com") is False

    def test_cpf_exists(self):
        repository = DjangoClientRepository()
        client = Client(
            id=None,
            full_name="Carla Souza",
            email="carla@test.com",
            phone="11955554444",
            cpf="999.888.777-66",
            address="Rua D, 40",
        )
        repository.save(client)

        assert repository.cpf_exists("999.888.777-66") is True
        assert repository.cpf_exists("000.000.000-00") is False
