"""Views REST - Consultas."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.application.dto.consultation_dto import (
    CompleteConsultationDTO,
    CreateVeterinarianDTO,
    ScheduleConsultationDTO,
)
from src.application.use_cases.consultation_use_cases import (
    CompleteConsultationUseCase,
    ConsultationNotFoundError,
    ConsultationSchedulingError,
    CreateVeterinarianUseCase,
    GetConsultationUseCase,
    ListConsultationsUseCase,
    ListVeterinariansUseCase,
    ScheduleConsultationUseCase,
    VeterinarianCreationError,
)
from src.domain.patterns.facade.veterinary_service_facade import VeterinaryServiceFacade
from src.infrastructure.repositories.django_consultation_repository import DjangoConsultationRepository
from src.infrastructure.repositories.django_veterinarian_repository import DjangoVeterinarianRepository
from src.infrastructure.services.animal_services import (
    InMemoryAnimalService,
    InMemoryMedicalHistoryService,
)
from src.presentation.api.serializers.consultation_serializers import (
    CompleteConsultationSerializer,
    ConsultationResponseSerializer,
    CreateVeterinarianSerializer,
    ScheduleConsultationSerializer,
    VeterinarianResponseSerializer,
)


def _get_consultation_repository():
    return DjangoConsultationRepository()


def _get_veterinarian_repository():
    return DjangoVeterinarianRepository()


def _get_facade(auth_token: str | None = None) -> VeterinaryServiceFacade:
    """Monta o Facade com serviços de animal (in-memory para operação local)."""
    return VeterinaryServiceFacade(
        animal_service=InMemoryAnimalService(),
        medical_history_service=InMemoryMedicalHistoryService(),
        consultation_repository=_get_consultation_repository(),
    )


class ConsultationListCreateView(APIView):
    """GET/POST /api/consultas - Listar e agendar consultas."""

    @extend_schema(
        responses={200: ConsultationResponseSerializer(many=True)},
        tags=["Consultas"],
    )
    def get(self, request):
        use_case = ListConsultationsUseCase(_get_consultation_repository())

        animal_id = request.query_params.get("animal_id")
        veterinarian_id = request.query_params.get("veterinarian_id")
        status_filter = request.query_params.get("status")

        results = use_case.execute(
            animal_id=int(animal_id) if animal_id else None,
            veterinarian_id=int(veterinarian_id) if veterinarian_id else None,
            status=status_filter,
        )
        return Response(
            ConsultationResponseSerializer([r.__dict__ for r in results], many=True).data,
        )

    @extend_schema(
        request=ScheduleConsultationSerializer,
        responses={201: ConsultationResponseSerializer},
        tags=["Consultas"],
    )
    def post(self, request):
        serializer = ScheduleConsultationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = ScheduleConsultationUseCase(
            _get_consultation_repository(),
            _get_veterinarian_repository(),
        )
        dto = ScheduleConsultationDTO(**serializer.validated_data)

        try:
            result = use_case.execute(dto)
        except ConsultationSchedulingError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            ConsultationResponseSerializer(result.__dict__).data,
            status=status.HTTP_201_CREATED,
        )


class ConsultationDetailView(APIView):
    """GET /api/consultas/{id} - Detalhes de uma consulta."""

    @extend_schema(
        responses={200: ConsultationResponseSerializer},
        tags=["Consultas"],
    )
    def get(self, request, pk: int):
        use_case = GetConsultationUseCase(_get_consultation_repository())

        try:
            result = use_case.execute(pk)
        except ConsultationNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(ConsultationResponseSerializer(result.__dict__).data)


class ConsultationCompleteView(APIView):
    """PATCH /api/consultas/{id}/concluir - Concluir consulta via Facade."""

    @extend_schema(
        request=CompleteConsultationSerializer,
        responses={200: ConsultationResponseSerializer},
        tags=["Consultas"],
    )
    def patch(self, request, pk: int):
        serializer = CompleteConsultationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_token = None
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            auth_token = auth_header.split(" ", 1)[1]

        use_case = CompleteConsultationUseCase(
            _get_consultation_repository(),
            _get_facade(auth_token=auth_token),
        )
        dto = CompleteConsultationDTO(consultation_id=pk, **serializer.validated_data)

        try:
            result = use_case.execute(dto)
        except ConsultationNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except ConsultationSchedulingError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ConsultationResponseSerializer(result.__dict__).data)


class VeterinarianListCreateView(APIView):
    """GET/POST /api/veterinarios - Listar e cadastrar veterinários."""

    @extend_schema(
        responses={200: VeterinarianResponseSerializer(many=True)},
        tags=["Veterinários"],
    )
    def get(self, request):
        use_case = ListVeterinariansUseCase(_get_veterinarian_repository())
        results = use_case.execute()
        return Response(
            VeterinarianResponseSerializer([r.__dict__ for r in results], many=True).data,
        )

    @extend_schema(
        request=CreateVeterinarianSerializer,
        responses={201: VeterinarianResponseSerializer},
        tags=["Veterinários"],
    )
    def post(self, request):
        serializer = CreateVeterinarianSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateVeterinarianUseCase(_get_veterinarian_repository())
        dto = CreateVeterinarianDTO(**serializer.validated_data)

        try:
            result = use_case.execute(dto)
        except VeterinarianCreationError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            VeterinarianResponseSerializer(result.__dict__).data,
            status=status.HTTP_201_CREATED,
        )
