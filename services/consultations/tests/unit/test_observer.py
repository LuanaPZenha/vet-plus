"""Testes unitários - Observer Pattern."""

from datetime import datetime, timezone

from src.domain.entities.consultation import (
    Consultation,
    ConsultationStatus,
    ConsultationType,
)
from src.domain.patterns.observer.notification_subject import (
    AppointmentReminderObserver,
    ConsultationScheduledObserver,
    EmailNotificationObserver,
    NotificationSubject,
)


def _scheduled_consultation() -> Consultation:
    return Consultation(
        id=42,
        animal_id=5,
        veterinarian_id=1,
        scheduled_at=datetime(2026, 7, 1, 14, 30, tzinfo=timezone.utc),
        status=ConsultationStatus.SCHEDULED,
        type=ConsultationType.REGULAR,
    )


class TestNotificationSubject:
    """Testes do Observer Pattern para notificações de agendamento."""

    def test_notify_consultation_scheduled_observer(self):
        subject = NotificationSubject()
        scheduled_observer = ConsultationScheduledObserver()
        subject.attach(scheduled_observer)

        consultation = _scheduled_consultation()
        events = subject.notify_consultation_scheduled(consultation)

        assert len(events) == 1
        assert events[0].event_type == "consultation_scheduled"
        assert events[0].consultation_id == 42
        assert len(scheduled_observer.notifications) == 1

    def test_notify_email_observer(self):
        subject = NotificationSubject()
        email_observer = EmailNotificationObserver()
        subject.attach(email_observer)

        subject.notify_consultation_scheduled(_scheduled_consultation())

        assert len(email_observer.sent_emails) == 1
        assert "Consulta agendada" in email_observer.sent_emails[0]["subject"]

    def test_notify_reminder_observer(self):
        subject = NotificationSubject()
        reminder_observer = AppointmentReminderObserver()
        subject.attach(reminder_observer)

        subject.notify_consultation_scheduled(_scheduled_consultation())

        assert len(reminder_observer.reminders) == 1
        assert reminder_observer.reminders[0]["consultation_id"] == 42

    def test_multiple_observers_notified(self):
        subject = NotificationSubject()
        scheduled_observer = ConsultationScheduledObserver()
        email_observer = EmailNotificationObserver()
        reminder_observer = AppointmentReminderObserver()

        subject.attach(scheduled_observer)
        subject.attach(email_observer)
        subject.attach(reminder_observer)

        subject.notify_consultation_scheduled(_scheduled_consultation())

        assert len(scheduled_observer.notifications) == 1
        assert len(email_observer.sent_emails) == 1
        assert len(reminder_observer.reminders) == 1

    def test_detach_observer(self):
        subject = NotificationSubject()
        observer = ConsultationScheduledObserver()
        subject.attach(observer)
        subject.detach(observer)

        subject.notify_consultation_scheduled(_scheduled_consultation())

        assert len(observer.notifications) == 0
