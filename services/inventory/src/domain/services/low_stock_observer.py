"""
Observer Pattern - Alertas de estoque baixo.

Notifica quando a quantidade de um medicamento atinge ou fica abaixo
do estoque mínimo configurado.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.medicine import Medicine


@dataclass
class LowStockEvent:
    medicine_id: int
    medicine_name: str
    current_quantity: str
    min_stock: str
    message: str


class StockAlertObserver(ABC):
    @abstractmethod
    def update(self, event: LowStockEvent) -> None:
        pass


class ConsoleStockAlertObserver(StockAlertObserver):
    """Observer concreto - registra alerta no console/log."""

    def __init__(self):
        self.alerts: list[LowStockEvent] = []

    def update(self, event: LowStockEvent) -> None:
        self.alerts.append(event)


class LowStockSubject:
    """Subject do Observer - dispara alertas de estoque baixo."""

    def __init__(self):
        self._observers: list[StockAlertObserver] = []

    def attach(self, observer: StockAlertObserver) -> None:
        self._observers.append(observer)

    def notify_low_stock(self, medicine: Medicine) -> None:
        if not medicine.is_low_stock():
            return
        event = LowStockEvent(
            medicine_id=medicine.id,
            medicine_name=medicine.name,
            current_quantity=str(medicine.quantity),
            min_stock=str(medicine.min_stock),
            message=f"Estoque baixo: {medicine.name} ({medicine.quantity} {medicine.unit})",
        )
        for observer in self._observers:
            observer.update(event)
