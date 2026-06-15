"""Entidades de domínio - Estoque de Medicamentos."""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum


class MedicineCategory(str, Enum):
    ANTIBIOTIC = "antibiotico"
    ANALGESIC = "analgesico"
    ANTI_INFLAMMATORY = "anti_inflamatorio"
    VACCINE = "vacina"
    ANESTHETIC = "anestesico"
    SUPPLEMENT = "suplemento"
    OTHER = "outro"


class MovementType(str, Enum):
    ENTRY = "entrada"
    EXIT = "saida"


@dataclass
class Medicine:
    """Entidade de medicamento no estoque."""

    id: int | None
    name: str
    generic_name: str
    category: MedicineCategory
    unit: str
    quantity: Decimal
    min_stock: Decimal
    batch_number: str | None
    expiration_date: date | None
    supplier: str | None
    unit_price: Decimal | None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def is_valid(self) -> bool:
        return bool(self.name.strip()) and self.quantity >= 0 and self.min_stock >= 0

    def is_low_stock(self) -> bool:
        return self.quantity <= self.min_stock

    def is_expired(self, reference: date | None = None) -> bool:
        if self.expiration_date is None:
            return False
        return self.expiration_date < (reference or date.today())

    def can_withdraw(self, amount: Decimal) -> bool:
        return amount > 0 and self.quantity >= amount


@dataclass
class StockMovement:
    """Registro de movimentação de estoque."""

    id: int | None
    medicine_id: int
    movement_type: MovementType
    quantity: Decimal
    reason: str
    performed_by: int
    stock_after: Decimal
    created_at: datetime | None = None

    def is_valid(self) -> bool:
        return self.quantity > 0 and bool(self.reason.strip())
