"""Views REST - Vacinação."""

from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.application.dto.vaccine_dto import RegisterVaccineDTO
from src.application.use_cases.vaccine_use_cases import (
    CheckUpcomingVaccinesUseCase,
    GetVaccineHistoryUseCase,
    GetVaccineUseCase,
    ListVaccinesUseCase,
    RegisterVaccineUseCase,
    VaccineNotFoundError,
    VaccineRegistrationError,
)
from src.domain.services.vaccine_reminder_observer import VaccineReminderObserver
from src.infrastructure.repositories.django_vaccine_reminder_repository import (
    DjangoVaccineReminderRepository,
)
from src.infrastructure.repositories.django_vaccine_repository import DjangoVaccineRepository
from src.infrastructure.services.console_notification_service import ConsoleNotificationService
from src.presentation.api.serializers.vaccine_serializers import (
    RegisterVaccineSerializer,
    UpcomingVaccineSerializer,
    VaccineResponseSerializer,
)


def _vaccine_repository():
    return DjangoVaccineRepository()


def _reminder_repository():
    return DjangoVaccineReminderRepository()


def _reminder_observer(within_days: int | None = None):
    days = within_days or getattr(settings, "VACCINE_REMINDER_DAYS_AHEAD", 7)
    return VaccineReminderObserver(
        _vaccine_repository(),
        _reminder_repository(),
        ConsoleNotificationService(),
        within_days=days,
    )


class VaccineListCreateView(APIView):
    """GET/POST /api/vacinas - Listar e registrar vacinas."""

    @extend_schema(
        responses={200: VaccineResponseSerializer(many=True)},
        tags=["Vacinas"],
    )
    def get(self, request):
        animal_id = request.query_params.get("animal_id")
        use_case = ListVaccinesUseCase(_vaccine_repository())
        results = use_case.execute(
            animal_id=int(animal_id) if animal_id else None,
        )
        return Response(
            VaccineResponseSerializer([r.__dict__ for r in results], many=True).data,
        )

    @extend_schema(
        request=RegisterVaccineSerializer,
        responses={201: VaccineResponseSerializer},
        tags=["Vacinas"],
    )
    def post(self, request):
        serializer = RegisterVaccineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated = dict(serializer.validated_data)
        validated.setdefault("next_dose_date", None)
        validated.setdefault("batch_number", None)
        validated.setdefault("notes", None)
        if validated.get("batch_number") == "":
            validated["batch_number"] = None
        if validated.get("notes") == "":
            validated["notes"] = None

        dto = RegisterVaccineDTO(**validated)
        use_case = RegisterVaccineUseCase(
            _vaccine_repository(),
            _reminder_repository(),
        )

        try:
            result = use_case.execute(dto)
        except VaccineRegistrationError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            VaccineResponseSerializer(result.__dict__).data,
            status=status.HTTP_201_CREATED,
        )


class VaccineDetailView(APIView):
    """GET /api/vacinas/{id} - Detalhes de uma vacina."""

    @extend_schema(
        responses={200: VaccineResponseSerializer},
        tags=["Vacinas"],
    )
    def get(self, request, pk: int):
        use_case = GetVaccineUseCase(_vaccine_repository())

        try:
            result = use_case.execute(pk)
        except VaccineNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(VaccineResponseSerializer(result.__dict__).data)


class VaccineByAnimalView(APIView):
    """GET /api/vacinas/animal/{animal_id} - Histórico de vacinação do animal."""

    @extend_schema(
        responses={200: VaccineResponseSerializer(many=True)},
        tags=["Vacinas"],
    )
    def get(self, request, animal_id: int):
        use_case = GetVaccineHistoryUseCase(_vaccine_repository())
        results = use_case.execute(animal_id)
        return Response(
            VaccineResponseSerializer([r.__dict__ for r in results], many=True).data,
        )


class UpcomingVaccinesView(APIView):
    """GET /api/vacinas/proximas - Vacinas com próxima dose se aproximando."""

    @extend_schema(
        responses={200: UpcomingVaccineSerializer(many=True)},
        tags=["Vacinas"],
    )
    def get(self, request):
        within_days = int(request.query_params.get("days", settings.VACCINE_REMINDER_DAYS_AHEAD))
        use_case = CheckUpcomingVaccinesUseCase(
            _reminder_observer(within_days),
            _vaccine_repository(),
            within_days=within_days,
        )
        results = use_case.execute()
        return Response(
            UpcomingVaccineSerializer([r.__dict__ for r in results], many=True).data,
        )
