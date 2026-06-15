"""Implementação concreta do serviço de notificação."""

import logging

from src.domain.entities.vaccine import Vaccine
from src.domain.entities.vaccine_reminder import VaccineReminder
from src.domain.services.notification_service import INotificationService

logger = logging.getLogger(__name__)


class ConsoleNotificationService(INotificationService):
    """Envia notificações registrando no log (adaptador de infraestrutura)."""

    def notify_vaccine_due(self, vaccine: Vaccine, reminder: VaccineReminder) -> None:
        message = (
            f"Vacina '{vaccine.vaccine_name}' do animal #{vaccine.animal_id} "
            f"vence em {vaccine.next_dose_date}. Lembrete #{reminder.id}."
        )
        logger.info("NOTIFICAÇÃO: %s", message)
