"""Interfaces de repositório - Estoque (Dependency Inversion)."""

from abc import ABC, abstractmethod
from decimal import Decimal

from src.domain.entities.medicine import Medicine, StockMovement


class IMedicineRepository(ABC):
    @abstractmethod
    def save(self, medicine: Medicine) -> Medicine:
        pass

    @abstractmethod
    def find_by_id(self, medicine_id: int) -> Medicine | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Medicine]:
        pass

    @abstractmethod
    def update(self, medicine: Medicine) -> Medicine:
        pass

    @abstractmethod
    def find_low_stock(self) -> list[Medicine]:
        pass


class IStockMovementRepository(ABC):
    @abstractmethod
    def save(self, movement: StockMovement) -> StockMovement:
        pass

    @abstractmethod
    def find_all(self, medicine_id: int | None = None) -> list[StockMovement]:
        pass
