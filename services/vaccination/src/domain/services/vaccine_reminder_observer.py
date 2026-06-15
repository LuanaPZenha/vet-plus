"""Observer Pattern - lembretes de vacinação."""

import logging
from abc import ABC, abstractmethod

from src.domain.entities.vaccine import Vaccine
from src.domain.entities.vaccine_reminder import VaccineReminder
from src.domain.repositories.vaccine_reminder_repository import IVaccineReminderRepository
from src.domain.repositories.vaccine_repository import IVaccineRepository
from src.domain.services.notification_service import INotificationService

logger = logging.getLogger(__name__)


class IVaccineObserver(ABC):
    """Contrato para observadores de vacinas."""

    @abstractmethod
    def update(self, vaccines: list[Vaccine]) -> None:
        pass


class VaccineReminderObserver(IVaccineObserver):
    """
    Observer que verifica vacinas com next_dose_date se aproximando
    e dispara notificações via NotificationService.
    """

    def __init__(
        self,
        vaccine_repository: IVaccineRepository,
        reminder_repository: IVaccineReminderRepository,
        notification_service: INotificationService,
        within_days: int = 7,
    ):
        self._vaccine_repository = vaccine_repository
        self._reminder_repository = reminder_repository
        self._notification_service = notification_service
        self._within_days = within_days

    def check_upcoming(self) -> list[VaccineReminder]:
        """Verifica vacinas próximas e processa lembretes pendentes."""
        upcoming = self._vaccine_repository.find_upcoming(self._within_days)
        self.update(upcoming)
        return self._reminder_repository.find_pending()

    def update(self, vaccines: list[Vaccine]) -> None:
        for vaccine in vaccines:
            if vaccine.id is None or vaccine.next_dose_date is None:
                continue

            existing = self._reminder_repository.find_by_vaccine_id(vaccine.id)
            if existing is not None and existing.sent:
                continue

            if existing is None:
                reminder = VaccineReminder(
                    id=None,
                    vaccine_id=vaccine.id,
                    animal_id=vaccine.animal_id,
                    reminder_date=vaccine.next_dose_date,
                    sent=False,
                )
                saved = self._reminder_repository.save(reminder)
            else:
                saved = existing

            if not saved.sent:
                self._notification_service.notify_vaccine_due(vaccine, saved)
                self._reminder_repository.mark_sent(saved.id)
                logger.info(
                    "Lembrete enviado: vacina %s (animal %s) vence em %s",
                    vaccine.vaccine_name,
                    vaccine.animal_id,
                    vaccine.next_dose_date,
                )
