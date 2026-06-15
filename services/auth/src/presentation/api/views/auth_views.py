"""Views REST - Autenticação."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.application.dto.auth_dto import LoginDTO, RegisterUserDTO
from src.application.use_cases.auth_use_cases import (
    AuthenticationError,
    LoginUserUseCase,
    RegisterUserUseCase,
    RegistrationError,
)
from src.domain.services.token_service import TokenService
from src.infrastructure.repositories.django_user_repository import DjangoUserRepository
from src.presentation.api.serializers.auth_serializers import (
    AuthResponseSerializer,
    LoginSerializer,
    RegisterSerializer,
)


class RegisterView(APIView):
    """POST /api/register - Registro de usuário."""

    @extend_schema(
        request=RegisterSerializer,
        responses={201: AuthResponseSerializer},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = RegisterUserUseCase(DjangoUserRepository(), TokenService())
        dto = RegisterUserDTO(**serializer.validated_data)

        try:
            result = use_case.execute(dto)
        except RegistrationError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            AuthResponseSerializer(result.__dict__).data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/login - Autenticação JWT."""

    @extend_schema(
        request=LoginSerializer,
        responses={200: AuthResponseSerializer},
        tags=["Auth"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = LoginUserUseCase(DjangoUserRepository(), TokenService())
        dto = LoginDTO(**serializer.validated_data)

        try:
            result = use_case.execute(dto)
        except AuthenticationError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(AuthResponseSerializer(result.__dict__).data)
