"""Interface de repositório - Lembretes de vacina."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.vaccine_reminder import VaccineReminder


class IVaccineReminderRepository(ABC):
    """Contrato para persistência de lembretes de vacina."""

    @abstractmethod
    def save(self, reminder: VaccineReminder) -> VaccineReminder:
        pass

    @abstractmethod
    def find_by_vaccine_id(self, vaccine_id: int) -> Optional[VaccineReminder]:
        pass

    @abstractmethod
    def find_pending(self) -> list[VaccineReminder]:
        pass

    @abstractmethod
    def mark_sent(self, reminder_id: int) -> None:
        pass
