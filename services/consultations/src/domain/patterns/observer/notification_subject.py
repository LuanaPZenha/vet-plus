"""
Observer Pattern - Notificações de agendamento.

O padrão Observer define uma dependência um-para-muitos entre objetos:
quando o estado do Subject muda (consulta agendada), todos os Observers
registrados são notificados automaticamente.

Estrutura:
  - NotificationObserver (observer abstrato): interface update()
  - ConsultationScheduledObserver, EmailNotificationObserver (observers concretos)
  - NotificationSubject (subject): mantém lista de observers e os notifica

Benefício: adicionar novos canais de notificação (SMS, push, e-mail) sem
alterar o código que agenda consultas — basta registrar um novo Observer.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from src.domain.entities.consultation import Consultation


@dataclass
class NotificationEvent:
    """Payload enviado aos observers quando um evento ocorre."""

    event_type: str
    consultation_id: int
    animal_id: int
    veterinarian_id: int
    scheduled_at: datetime
    message: str


class NotificationObserver(ABC):
    """Observer abstrato - interface para receber notificações."""

    @abstractmethod
    def update(self, event: NotificationEvent) -> None:
        """Reage à notificação do subject."""


class ConsultationScheduledObserver(NotificationObserver):
    """
    Observer concreto - registra notificação de consulta agendada.

    Em produção, este observer poderia enviar push notification ou
    registrar em fila de mensageria.
    """

    def __init__(self):
        self.notifications: list[NotificationEvent] = []

    def update(self, event: NotificationEvent) -> None:
        self.notifications.append(event)


class EmailNotificationObserver(NotificationObserver):
    """Observer concreto - simula envio de e-mail ao tutor."""

    def __init__(self):
        self.sent_emails: list[dict] = []

    def update(self, event: NotificationEvent) -> None:
        self.sent_emails.append(
            {
                "to": f"tutor-animal-{event.animal_id}@vetplus.com",
                "subject": "Consulta agendada - Vet Plus+",
                "body": event.message,
            }
        )


class AppointmentReminderObserver(NotificationObserver):
    """Observer concreto - registra lembrete de consulta futura."""

    def __init__(self):
        self.reminders: list[dict] = []

    def update(self, event: NotificationEvent) -> None:
        self.reminders.append(
            {
                "consultation_id": event.consultation_id,
                "scheduled_at": event.scheduled_at.isoformat(),
                "reminder_message": f"Lembrete: {event.message}",
            }
        )


class NotificationSubject:
    """
    Subject do Observer Pattern.

    Mantém lista de observers e os notifica quando uma consulta é agendada.
    Observers podem ser adicionados/removidos dinamicamente.
    """

    def __init__(self):
        self._observers: list[NotificationObserver] = []

    def attach(self, observer: NotificationObserver) -> None:
        """Registra um observer para receber notificações."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: NotificationObserver) -> None:
        """Remove um observer da lista."""
        self._observers.remove(observer)

    def notify_consultation_scheduled(self, consultation: Consultation) -> list[NotificationEvent]:
        """Notifica todos os observers sobre consulta agendada."""
        event = NotificationEvent(
            event_type="consultation_scheduled",
            consultation_id=consultation.id or 0,
            animal_id=consultation.animal_id,
            veterinarian_id=consultation.veterinarian_id,
            scheduled_at=consultation.scheduled_at,
            message=(
                f"Consulta {consultation.type.value} agendada para "
                f"{consultation.scheduled_at.strftime('%d/%m/%Y %H:%M')} "
                f"(animal #{consultation.animal_id})"
            ),
        )
        for observer in self._observers:
            observer.update(event)
        return [event]
