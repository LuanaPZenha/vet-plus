from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from src.application.dto.medicine_dto import RegisterMedicineDTO, StockMovementDTO, UpdateMedicineDTO
from src.application.use_cases.medicine_use_cases import (
    GetMedicineUseCase,
    InsufficientStockError,
    ListLowStockUseCase,
    ListMedicinesUseCase,
    ListMovementsUseCase,
    MedicineError,
    MedicineNotFoundError,
    RegisterMedicineUseCase,
    StockEntryUseCase,
    StockExitUseCase,
    UpdateMedicineUseCase,
)
from src.domain.services.low_stock_observer import ConsoleStockAlertObserver, LowStockSubject
from src.infrastructure.repositories.django_medicine_repository import (
    DjangoMedicineRepository,
    DjangoStockMovementRepository,
)
from src.presentation.api.serializers.medicine_serializers import (
    MedicineResponseSerializer,
    MovementResponseSerializer,
    RegisterMedicineSerializer,
    StockMovementSerializer,
    UpdateMedicineSerializer,
)

_low_stock_subject = LowStockSubject()
_low_stock_subject.attach(ConsoleStockAlertObserver())


def _medicine_repo():
    return DjangoMedicineRepository()


def _movement_repo():
    return DjangoStockMovementRepository()


def _user_id(request) -> int:
    return getattr(request.user, "user_id", 0)


class MedicineListCreateView(APIView):
    @extend_schema(responses={200: MedicineResponseSerializer(many=True)}, tags=["Estoque"])
    def get(self, request):
        results = ListMedicinesUseCase(_medicine_repo()).execute()
        return Response(MedicineResponseSerializer([r.__dict__ for r in results], many=True).data)

    @extend_schema(request=RegisterMedicineSerializer, responses={201: MedicineResponseSerializer}, tags=["Estoque"])
    def post(self, request):
        serializer = RegisterMedicineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = RegisterMedicineDTO(**serializer.validated_data)
        try:
            result = RegisterMedicineUseCase(_medicine_repo(), _low_stock_subject).execute(dto)
        except MedicineError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MedicineResponseSerializer(result.__dict__).data, status=status.HTTP_201_CREATED)


class MedicineDetailView(APIView):
    @extend_schema(responses={200: MedicineResponseSerializer}, tags=["Estoque"])
    def get(self, request, pk: int):
        try:
            result = GetMedicineUseCase(_medicine_repo()).execute(pk)
        except MedicineNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        return Response(MedicineResponseSerializer(result.__dict__).data)

    @extend_schema(request=UpdateMedicineSerializer, responses={200: MedicineResponseSerializer}, tags=["Estoque"])
    def patch(self, request, pk: int):
        serializer = UpdateMedicineSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        dto = UpdateMedicineDTO(**serializer.validated_data)
        try:
            result = UpdateMedicineUseCase(_medicine_repo()).execute(pk, dto)
        except MedicineNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except MedicineError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MedicineResponseSerializer(result.__dict__).data)


class StockEntryView(APIView):
    @extend_schema(request=StockMovementSerializer, responses={201: MovementResponseSerializer}, tags=["Estoque"])
    def post(self, request, pk: int):
        serializer = StockMovementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = StockMovementDTO(performed_by=_user_id(request), **serializer.validated_data)
        try:
            result = StockEntryUseCase(_medicine_repo(), _movement_repo(), _low_stock_subject).execute(pk, dto)
        except MedicineNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except MedicineError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MovementResponseSerializer(result.__dict__).data, status=status.HTTP_201_CREATED)


class StockExitView(APIView):
    @extend_schema(request=StockMovementSerializer, responses={201: MovementResponseSerializer}, tags=["Estoque"])
    def post(self, request, pk: int):
        serializer = StockMovementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = StockMovementDTO(performed_by=_user_id(request), **serializer.validated_data)
        try:
            result = StockExitUseCase(_medicine_repo(), _movement_repo(), _low_stock_subject).execute(pk, dto)
        except MedicineNotFoundError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except InsufficientStockError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except MedicineError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MovementResponseSerializer(result.__dict__).data, status=status.HTTP_201_CREATED)


class LowStockView(APIView):
    @extend_schema(responses={200: MedicineResponseSerializer(many=True)}, tags=["Estoque"])
    def get(self, request):
        results = ListLowStockUseCase(_medicine_repo()).execute()
        return Response(MedicineResponseSerializer([r.__dict__ for r in results], many=True).data)


class MovementsListView(APIView):
    @extend_schema(responses={200: MovementResponseSerializer(many=True)}, tags=["Estoque"])
    def get(self, request):
        medicine_id = request.query_params.get("medicine_id")
        results = ListMovementsUseCase(_movement_repo()).execute(
            int(medicine_id) if medicine_id else None,
        )
        return Response(MovementResponseSerializer([r.__dict__ for r in results], many=True).data)
