"""Views REST - Clientes."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.application.dto.client_dto import CreateClientDTO
from src.application.use_cases.client_use_cases import (
    ClientError,
    ClientNotFoundError,
    CreateClientUseCase,
    GetClientUseCase,
    ListClientsUseCase,
)
from src.infrastructure.repositories.django_client_repository import DjangoClientRepository
from src.presentation.api.authentication.jwt_auth import IsAnyAuthenticatedRole, IsStaffRole
from src.presentation.api.serializers.client_serializers import (
    ClientResponseSerializer,
    CreateClientSerializer,
)


class ClientListCreateView(APIView):
    """GET/POST /api/clientes - Listagem e cadastro de clientes."""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsStaffRole()]
        return [IsAnyAuthenticatedRole()]

    @extend_schema(
        responses={200: ClientResponseSerializer(many=True)},
        tags=["Clientes"],
    )
    def get(self, request):
        use_case = ListClientsUseCase(DjangoClientRepository())
        results = use_case.execute()
        data = [ClientResponseSerializer.from_dto(dto) for dto in results]
        return Response(data)

    @extend_schema(
        request=CreateClientSerializer,
        responses={201: ClientResponseSerializer},
        tags=["Clientes"],
    )
    def post(self, request):
        serializer = CreateClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = serializer.validated_data
        dto = CreateClientDTO(
            full_name=validated["nome_completo"],
            email=validated["email"],
            phone=validated["telefone"],
            cpf=validated["cpf"],
            address=validated["endereco"],
        )

        use_case = CreateClientUseCase(DjangoClientRepository())
        try:
            result = use_case.execute(dto)
        except ClientError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            ClientResponseSerializer.from_dto(result),
            status=status.HTTP_201_CREATED,
        )


class ClientDetailView(APIView):
    """GET /api/clientes/{id} - Detalhe de cliente."""

    permission_classes = [IsAnyAuthenticatedRole]

    @extend_schema(
        responses={200: ClientResponseSerializer},
        tags=["Clientes"],
    )
    def get(self, request, pk: int):
        use_case = GetClientUseCase(DjangoClientRepository())
        try:
            result = use_case.execute(pk)
        except ClientNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(ClientResponseSerializer.from_dto(result))
