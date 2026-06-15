"""Observer Pattern - notificações."""

from src.domain.patterns.observer.notification_subject import (
    AppointmentReminderObserver,
    ConsultationScheduledObserver,
    EmailNotificationObserver,
    NotificationEvent,
    NotificationObserver,
    NotificationSubject,
)

__all__ = [
    "AppointmentReminderObserver",
    "ConsultationScheduledObserver",
    "EmailNotificationObserver",
    "NotificationEvent",
    "NotificationObserver",
    "NotificationSubject",
]
