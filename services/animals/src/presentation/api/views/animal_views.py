"""Views REST - Animais."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.application.dto.animal_dto import AddMedicalHistoryDTO, CreateAnimalDTO
from src.application.use_cases.animal_use_cases import (
    AddMedicalHistoryUseCase,
    AnimalCreationError,
    AnimalNotFoundError,
    CreateAnimalUseCase,
    GetAnimalUseCase,
    GetMedicalHistoryUseCase,
    ListAnimalsUseCase,
    MedicalHistoryError,
)
from src.infrastructure.repositories.django_animal_repository import DjangoAnimalRepository
from src.infrastructure.repositories.django_medical_history_repository import (
    DjangoMedicalHistoryRepository,
)
from src.presentation.api.serializers.animal_serializers import (
    AddMedicalHistorySerializer,
    AnimalResponseSerializer,
    CreateAnimalSerializer,
    MedicalHistoryResponseSerializer,
)


def _get_client_filter(request) -> int | None:
    """Tutores veem apenas animais do próprio client_id (user_id)."""
    role = getattr(request.user, "role", None)
    if role == "tutor":
        return getattr(request.user, "user_id", None)
    client_id = request.query_params.get("client_id")
    if client_id is not None:
        return int(client_id)
    return None


class AnimalListCreateView(APIView):
    """GET/POST /api/animais - Listar e criar animais."""

    @extend_schema(
        responses={200: AnimalResponseSerializer(many=True)},
        tags=["Animais"],
    )
    def get(self, request):
        use_case = ListAnimalsUseCase(DjangoAnimalRepository())
        client_id = _get_client_filter(request)
        results = use_case.execute(client_id=client_id)
        return Response(AnimalResponseSerializer([r.__dict__ for r in results], many=True).data)

    @extend_schema(
        request=CreateAnimalSerializer,
        responses={201: AnimalResponseSerializer},
        tags=["Animais"],
    )
    def post(self, request):
        serializer = CreateAnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateAnimalUseCase(DjangoAnimalRepository())
        validated = dict(serializer.validated_data)
        validated.setdefault("birth_date", None)
        validated.setdefault("weight", None)
        if validated.get("weight") is not None:
            validated["weight"] = float(validated["weight"])
        dto = CreateAnimalDTO(**validated)

        try:
            result = use_case.execute(dto)
        except AnimalCreationError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            AnimalResponseSerializer(result.__dict__).data,
            status=status.HTTP_201_CREATED,
        )


class AnimalDetailView(APIView):
    """GET /api/animais/{id} - Detalhes de um animal."""

    @extend_schema(
        responses={200: AnimalResponseSerializer},
        tags=["Animais"],
    )
    def get(self, request, pk: int):
        use_case = GetAnimalUseCase(DjangoAnimalRepository())

        try:
            result = use_case.execute(pk)
        except AnimalNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        role = getattr(request.user, "role", None)
        if role == "tutor" and result.client_id != request.user.user_id:
            return Response(
                {"error": "Acesso negado a este animal."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(AnimalResponseSerializer(result.__dict__).data)


class MedicalHistoryView(APIView):
    """GET/POST /api/animais/{id}/historico - Histórico médico."""

    def _check_animal_access(self, request, animal_id: int) -> Response | None:
        animal_repo = DjangoAnimalRepository()
        animal = animal_repo.find_by_id(animal_id)
        if animal is None:
            return Response(
                {"error": f"Animal {animal_id} não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        role = getattr(request.user, "role", None)
        if role == "tutor" and animal.client_id != request.user.user_id:
            return Response(
                {"error": "Acesso negado a este animal."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return None

    @extend_schema(
        responses={200: MedicalHistoryResponseSerializer(many=True)},
        tags=["Histórico Médico"],
    )
    def get(self, request, pk: int):
        access_error = self._check_animal_access(request, pk)
        if access_error:
            return access_error

        use_case = GetMedicalHistoryUseCase(
            DjangoAnimalRepository(),
            DjangoMedicalHistoryRepository(),
        )

        try:
            results = use_case.execute(pk)
        except AnimalNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            MedicalHistoryResponseSerializer([r.__dict__ for r in results], many=True).data,
        )

    @extend_schema(
        request=AddMedicalHistorySerializer,
        responses={201: MedicalHistoryResponseSerializer},
        tags=["Histórico Médico"],
    )
    def post(self, request, pk: int):
        access_error = self._check_animal_access(request, pk)
        if access_error:
            return access_error

        serializer = AddMedicalHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = AddMedicalHistoryUseCase(
            DjangoAnimalRepository(),
            DjangoMedicalHistoryRepository(),
        )
        dto = AddMedicalHistoryDTO(animal_id=pk, **serializer.validated_data)

        try:
            result = use_case.execute(dto)
        except AnimalNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except MedicalHistoryError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            MedicalHistoryResponseSerializer(result.__dict__).data,
            status=status.HTTP_201_CREATED,
        )
