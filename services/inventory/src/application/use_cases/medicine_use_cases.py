"""Casos de uso - Estoque de Medicamentos."""

from decimal import Decimal


class MedicineNotFoundError(Exception):
    pass


class MedicineError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


def _to_medicine_dto(medicine) -> "MedicineResponseDTO":
    from src.application.dto.medicine_dto import MedicineResponseDTO

    return MedicineResponseDTO(
        id=medicine.id,
        name=medicine.name,
        generic_name=medicine.generic_name,
        category=medicine.category.value,
        unit=medicine.unit,
        quantity=medicine.quantity,
        min_stock=medicine.min_stock,
        batch_number=medicine.batch_number,
        expiration_date=medicine.expiration_date,
        supplier=medicine.supplier,
        unit_price=medicine.unit_price,
        is_low_stock=medicine.is_low_stock(),
        is_expired=medicine.is_expired(),
        created_at=medicine.created_at,
        updated_at=medicine.updated_at,
    )


def _to_movement_dto(movement) -> "MovementResponseDTO":
    from src.application.dto.medicine_dto import MovementResponseDTO

    return MovementResponseDTO(
        id=movement.id,
        medicine_id=movement.medicine_id,
        movement_type=movement.movement_type.value,
        quantity=movement.quantity,
        reason=movement.reason,
        performed_by=movement.performed_by,
        stock_after=movement.stock_after,
        created_at=movement.created_at,
    )


class RegisterMedicineUseCase:
    def __init__(self, medicine_repository, low_stock_subject=None):
        self._repository = medicine_repository
        self._alerts = low_stock_subject

    def execute(self, dto) -> "MedicineResponseDTO":
        from src.domain.entities.medicine import Medicine, MedicineCategory

        try:
            category = MedicineCategory(dto.category)
        except ValueError as exc:
            raise MedicineError(f"Categoria inválida: {dto.category}") from exc

        medicine = Medicine(
            id=None,
            name=dto.name,
            generic_name=dto.generic_name,
            category=category,
            unit=dto.unit,
            quantity=dto.quantity,
            min_stock=dto.min_stock,
            batch_number=dto.batch_number,
            expiration_date=dto.expiration_date,
            supplier=dto.supplier,
            unit_price=dto.unit_price,
        )
        if not medicine.is_valid():
            raise MedicineError("Dados do medicamento inválidos.")

        saved = self._repository.save(medicine)
        if self._alerts:
            self._alerts.notify_low_stock(saved)
        return _to_medicine_dto(saved)


class ListMedicinesUseCase:
    def __init__(self, medicine_repository):
        self._repository = medicine_repository

    def execute(self) -> list:
        return [_to_medicine_dto(m) for m in self._repository.find_all()]


class GetMedicineUseCase:
    def __init__(self, medicine_repository):
        self._repository = medicine_repository

    def execute(self, medicine_id: int):
        medicine = self._repository.find_by_id(medicine_id)
        if medicine is None:
            raise MedicineNotFoundError(f"Medicamento {medicine_id} não encontrado.")
        return _to_medicine_dto(medicine)


class UpdateMedicineUseCase:
    def __init__(self, medicine_repository):
        self._repository = medicine_repository

    def execute(self, medicine_id: int, dto):
        from src.domain.entities.medicine import MedicineCategory

        medicine = self._repository.find_by_id(medicine_id)
        if medicine is None:
            raise MedicineNotFoundError(f"Medicamento {medicine_id} não encontrado.")

        if dto.name is not None:
            medicine.name = dto.name
        if dto.generic_name is not None:
            medicine.generic_name = dto.generic_name
        if dto.category is not None:
            medicine.category = MedicineCategory(dto.category)
        if dto.unit is not None:
            medicine.unit = dto.unit
        if dto.min_stock is not None:
            medicine.min_stock = dto.min_stock
        if dto.batch_number is not None:
            medicine.batch_number = dto.batch_number
        if dto.expiration_date is not None:
            medicine.expiration_date = dto.expiration_date
        if dto.supplier is not None:
            medicine.supplier = dto.supplier
        if dto.unit_price is not None:
            medicine.unit_price = dto.unit_price

        updated = self._repository.update(medicine)
        return _to_medicine_dto(updated)


class StockEntryUseCase:
    """Entrada de medicamentos no estoque."""

    def __init__(self, medicine_repository, movement_repository, low_stock_subject=None):
        self._medicine_repo = medicine_repository
        self._movement_repo = movement_repository
        self._alerts = low_stock_subject

    def execute(self, medicine_id: int, dto):
        from src.domain.entities.medicine import MovementType, StockMovement

        medicine = self._medicine_repo.find_by_id(medicine_id)
        if medicine is None:
            raise MedicineNotFoundError(f"Medicamento {medicine_id} não encontrado.")
        if dto.quantity <= 0:
            raise MedicineError("Quantidade de entrada deve ser maior que zero.")

        medicine.quantity += dto.quantity
        updated = self._medicine_repo.update(medicine)

        movement = StockMovement(
            id=None,
            medicine_id=medicine_id,
            movement_type=MovementType.ENTRY,
            quantity=dto.quantity,
            reason=dto.reason,
            performed_by=dto.performed_by,
            stock_after=updated.quantity,
        )
        saved_movement = self._movement_repo.save(movement)
        if self._alerts:
            self._alerts.notify_low_stock(updated)
        return _to_movement_dto(saved_movement)


class StockExitUseCase:
    """Saída de medicamentos do estoque."""

    def __init__(self, medicine_repository, movement_repository, low_stock_subject=None):
        self._medicine_repo = medicine_repository
        self._movement_repo = movement_repository
        self._alerts = low_stock_subject

    def execute(self, medicine_id: int, dto):
        from src.domain.entities.medicine import MovementType, StockMovement

        medicine = self._medicine_repo.find_by_id(medicine_id)
        if medicine is None:
            raise MedicineNotFoundError(f"Medicamento {medicine_id} não encontrado.")
        if not medicine.can_withdraw(dto.quantity):
            raise InsufficientStockError(
                f"Estoque insuficiente. Disponível: {medicine.quantity} {medicine.unit}"
            )

        medicine.quantity -= dto.quantity
        updated = self._medicine_repo.update(medicine)

        movement = StockMovement(
            id=None,
            medicine_id=medicine_id,
            movement_type=MovementType.EXIT,
            quantity=dto.quantity,
            reason=dto.reason,
            performed_by=dto.performed_by,
            stock_after=updated.quantity,
        )
        saved_movement = self._movement_repo.save(movement)
        if self._alerts:
            self._alerts.notify_low_stock(updated)
        return _to_movement_dto(saved_movement)


class ListLowStockUseCase:
    def __init__(self, medicine_repository):
        self._repository = medicine_repository

    def execute(self) -> list:
        return [_to_medicine_dto(m) for m in self._repository.find_low_stock()]


class ListMovementsUseCase:
    def __init__(self, movement_repository):
        self._repository = movement_repository

    def execute(self, medicine_id: int | None = None) -> list:
        movements = self._repository.find_all(medicine_id)
        return [_to_movement_dto(m) for m in movements]
