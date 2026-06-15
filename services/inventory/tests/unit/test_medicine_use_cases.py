from decimal import Decimal

import pytest

from src.application.dto.medicine_dto import RegisterMedicineDTO, StockMovementDTO
from src.application.use_cases.medicine_use_cases import (
    InsufficientStockError,
    RegisterMedicineUseCase,
    StockEntryUseCase,
    StockExitUseCase,
)
from src.domain.entities.medicine import Medicine, MedicineCategory, MovementType, StockMovement
from src.domain.repositories.medicine_repository import IMedicineRepository, IStockMovementRepository


class InMemoryMedicineRepository(IMedicineRepository):
    def __init__(self):
        self._store: dict[int, Medicine] = {}
        self._next_id = 1

    def save(self, medicine: Medicine) -> Medicine:
        medicine.id = self._next_id
        self._next_id += 1
        self._store[medicine.id] = medicine
        return medicine

    def find_by_id(self, medicine_id: int) -> Medicine | None:
        return self._store.get(medicine_id)

    def find_all(self) -> list[Medicine]:
        return list(self._store.values())

    def update(self, medicine: Medicine) -> Medicine:
        self._store[medicine.id] = medicine
        return medicine

    def find_low_stock(self) -> list[Medicine]:
        return [m for m in self._store.values() if m.is_low_stock()]


class InMemoryMovementRepository(IStockMovementRepository):
    def __init__(self):
        self._store: list[StockMovement] = []
        self._next_id = 1

    def save(self, movement: StockMovement) -> StockMovement:
        movement.id = self._next_id
        self._next_id += 1
        self._store.append(movement)
        return movement

    def find_all(self, medicine_id: int | None = None) -> list[StockMovement]:
        if medicine_id:
            return [m for m in self._store if m.medicine_id == medicine_id]
        return list(self._store)


@pytest.fixture
def medicine_repo():
    return InMemoryMedicineRepository()


@pytest.fixture
def movement_repo():
    return InMemoryMovementRepository()


class TestRegisterMedicine:
    def test_register_medicine_success(self, medicine_repo):
        use_case = RegisterMedicineUseCase(medicine_repo)
        dto = RegisterMedicineDTO(
            name="Amoxicilina 500mg",
            generic_name="Amoxicilina",
            category="antibiotico",
            unit="comp",
            quantity=Decimal("100"),
            min_stock=Decimal("20"),
        )
        result = use_case.execute(dto)
        assert result.name == "Amoxicilina 500mg"
        assert result.quantity == Decimal("100")


class TestStockMovement:
    def test_stock_entry_increases_quantity(self, medicine_repo, movement_repo):
        med = medicine_repo.save(Medicine(
            id=None, name="Dipirona", generic_name="Dipirona", category=MedicineCategory.ANALGESIC,
            unit="ml", quantity=Decimal("50"), min_stock=Decimal("10"),
            batch_number=None, expiration_date=None, supplier=None, unit_price=None,
        ))
        use_case = StockEntryUseCase(medicine_repo, movement_repo)
        result = use_case.execute(med.id, StockMovementDTO(
            quantity=Decimal("30"), reason="Compra fornecedor", performed_by=1,
        ))
        assert result.movement_type == "entrada"
        updated = medicine_repo.find_by_id(med.id)
        assert updated.quantity == Decimal("80")

    def test_stock_exit_decreases_quantity(self, medicine_repo, movement_repo):
        med = medicine_repo.save(Medicine(
            id=None, name="Dipirona", generic_name="Dipirona", category=MedicineCategory.ANALGESIC,
            unit="ml", quantity=Decimal("50"), min_stock=Decimal("10"),
            batch_number=None, expiration_date=None, supplier=None, unit_price=None,
        ))
        use_case = StockExitUseCase(medicine_repo, movement_repo)
        result = use_case.execute(med.id, StockMovementDTO(
            quantity=Decimal("10"), reason="Consulta animal #1", performed_by=1,
        ))
        assert result.movement_type == "saida"
        updated = medicine_repo.find_by_id(med.id)
        assert updated.quantity == Decimal("40")

    def test_stock_exit_insufficient_raises(self, medicine_repo, movement_repo):
        med = medicine_repo.save(Medicine(
            id=None, name="Dipirona", generic_name="Dipirona", category=MedicineCategory.ANALGESIC,
            unit="ml", quantity=Decimal("5"), min_stock=Decimal("10"),
            batch_number=None, expiration_date=None, supplier=None, unit_price=None,
        ))
        use_case = StockExitUseCase(medicine_repo, movement_repo)
        with pytest.raises(InsufficientStockError):
            use_case.execute(med.id, StockMovementDTO(
                quantity=Decimal("10"), reason="Consulta", performed_by=1,
            ))
