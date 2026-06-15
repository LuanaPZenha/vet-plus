"""Testes unitários - Casos de uso de clientes."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from src.application.dto.client_dto import CreateClientDTO
from src.application.use_cases.client_use_cases import (
    ClientError,
    ClientNotFoundError,
    CreateClientUseCase,
    GetClientUseCase,
    ListClientsUseCase,
)
from src.domain.entities.client import Client


@pytest.fixture
def sample_client():
    return Client(
        id=1,
        full_name="Maria Silva",
        email="maria@test.com",
        phone="11999998888",
        cpf="123.456.789-00",
        address="Rua das Flores, 100",
        created_at=datetime(2024, 1, 15, 10, 0, tzinfo=timezone.utc),
    )


@pytest.fixture
def create_dto():
    return CreateClientDTO(
        full_name="Maria Silva",
        email="maria@test.com",
        phone="11999998888",
        cpf="123.456.789-00",
        address="Rua das Flores, 100",
    )


class TestCreateClientUseCase:
    """TDD: Casos de uso para cadastro de clientes."""

    def test_create_client_success(self, create_dto, sample_client):
        repository = MagicMock()
        repository.email_exists.return_value = False
        repository.cpf_exists.return_value = False
        repository.save.return_value = sample_client

        use_case = CreateClientUseCase(repository)
        result = use_case.execute(create_dto)

        assert result.id == 1
        assert result.full_name == "Maria Silva"
        assert result.email == "maria@test.com"
        repository.save.assert_called_once()

    def test_create_client_duplicate_email(self, create_dto):
        repository = MagicMock()
        repository.email_exists.return_value = True

        use_case = CreateClientUseCase(repository)

        with pytest.raises(ClientError, match="E-mail já cadastrado"):
            use_case.execute(create_dto)

    def test_create_client_duplicate_cpf(self, create_dto):
        repository = MagicMock()
        repository.email_exists.return_value = False
        repository.cpf_exists.return_value = True

        use_case = CreateClientUseCase(repository)

        with pytest.raises(ClientError, match="CPF já cadastrado"):
            use_case.execute(create_dto)


class TestListClientsUseCase:
    """TDD: Listagem de clientes."""

    def test_list_clients_returns_all(self, sample_client):
        repository = MagicMock()
        repository.find_all.return_value = [sample_client]

        use_case = ListClientsUseCase(repository)
        results = use_case.execute()

        assert len(results) == 1
        assert results[0].full_name == "Maria Silva"


class TestGetClientUseCase:
    """TDD: Obtenção de cliente por ID."""

    def test_get_client_success(self, sample_client):
        repository = MagicMock()
        repository.find_by_id.return_value = sample_client

        use_case = GetClientUseCase(repository)
        result = use_case.execute(1)

        assert result.id == 1
        assert result.cpf == "123.456.789-00"

    def test_get_client_not_found(self):
        repository = MagicMock()
        repository.find_by_id.return_value = None

        use_case = GetClientUseCase(repository)

        with pytest.raises(ClientNotFoundError, match="Cliente não encontrado"):
            use_case.execute(999)
