"""Casos de uso - Clientes."""


class ClientError(Exception):
    """Erro genérico de operações com clientes."""


class ClientNotFoundError(ClientError):
    """Cliente não encontrado."""


class CreateClientUseCase:
    """Cadastra novo cliente (tutor) no sistema."""

    def __init__(self, client_repository):
        self._client_repository = client_repository

    def execute(self, dto) -> "ClientResponseDTO":
        from src.application.dto.client_dto import ClientResponseDTO
        from src.domain.entities.client import Client

        if self._client_repository.email_exists(dto.email):
            raise ClientError("E-mail já cadastrado.")

        if self._client_repository.cpf_exists(dto.cpf):
            raise ClientError("CPF já cadastrado.")

        client = Client(
            id=None,
            full_name=dto.full_name,
            email=dto.email,
            phone=dto.phone,
            cpf=dto.cpf,
            address=dto.address,
        )
        saved = self._client_repository.save(client)

        return ClientResponseDTO(
            id=saved.id,
            full_name=saved.full_name,
            email=saved.email,
            phone=saved.phone,
            cpf=saved.cpf,
            address=saved.address,
            created_at=saved.created_at,
        )


class ListClientsUseCase:
    """Lista todos os clientes cadastrados."""

    def __init__(self, client_repository):
        self._client_repository = client_repository

    def execute(self) -> list["ClientResponseDTO"]:
        from src.application.dto.client_dto import ClientResponseDTO

        clients = self._client_repository.find_all()
        return [
            ClientResponseDTO(
                id=client.id,
                full_name=client.full_name,
                email=client.email,
                phone=client.phone,
                cpf=client.cpf,
                address=client.address,
                created_at=client.created_at,
            )
            for client in clients
        ]


class GetClientUseCase:
    """Obtém cliente por identificador."""

    def __init__(self, client_repository):
        self._client_repository = client_repository

    def execute(self, client_id: int) -> "ClientResponseDTO":
        from src.application.dto.client_dto import ClientResponseDTO

        client = self._client_repository.find_by_id(client_id)
        if client is None:
            raise ClientNotFoundError("Cliente não encontrado.")

        return ClientResponseDTO(
            id=client.id,
            full_name=client.full_name,
            email=client.email,
            phone=client.phone,
            cpf=client.cpf,
            address=client.address,
            created_at=client.created_at,
        )
