"""Serviço de notificação - domínio."""

from abc import ABC, abstractmethod

from src.domain.entities.vaccine import Vaccine
from src.domain.entities.vaccine_reminder import VaccineReminder


class INotificationService(ABC):
    """Contrato para envio de notificações de vacina."""

    @abstractmethod
    def notify_vaccine_due(self, vaccine: Vaccine, reminder: VaccineReminder) -> None:
        pass
