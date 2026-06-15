"""Entidade de lembrete de vacina."""

from dataclasses import dataclass
from datetime import date


@dataclass
class VaccineReminder:
    """Lembrete de vacina pendente ou enviado."""

    id: int | None
    vaccine_id: int
    animal_id: int
    reminder_date: date
    sent: bool = False

    def is_valid(self) -> bool:
        return self.vaccine_id > 0 and self.animal_id > 0 and self.reminder_date is not None

    def mark_sent(self) -> None:
        self.sent = True
