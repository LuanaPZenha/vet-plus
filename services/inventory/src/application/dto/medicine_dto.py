"""DTOs - Estoque."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class RegisterMedicineDTO:
    name: str
    generic_name: str
    category: str
    unit: str
    quantity: Decimal
    min_stock: Decimal
    batch_number: str | None = None
    expiration_date: date | None = None
    supplier: str | None = None
    unit_price: Decimal | None = None


@dataclass
class UpdateMedicineDTO:
    name: str | None = None
    generic_name: str | None = None
    category: str | None = None
    unit: str | None = None
    min_stock: Decimal | None = None
    batch_number: str | None = None
    expiration_date: date | None = None
    supplier: str | None = None
    unit_price: Decimal | None = None


@dataclass
class StockMovementDTO:
    quantity: Decimal
    reason: str
    performed_by: int


@dataclass
class MedicineResponseDTO:
    id: int
    name: str
    generic_name: str
    category: str
    unit: str
    quantity: Decimal
    min_stock: Decimal
    batch_number: str | None
    expiration_date: date | None
    supplier: str | None
    unit_price: Decimal | None
    is_low_stock: bool
    is_expired: bool
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class MovementResponseDTO:
    id: int
    medicine_id: int
    movement_type: str
    quantity: Decimal
    reason: str
    performed_by: int
    stock_after: Decimal
    created_at: datetime | None
