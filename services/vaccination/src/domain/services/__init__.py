"""Serviços de domínio - Vacinação."""

from src.domain.services.notification_service import INotificationService
from src.domain.services.vaccine_reminder_observer import IVaccineObserver, VaccineReminderObserver

__all__ = ["INotificationService", "IVaccineObserver", "VaccineReminderObserver"]
