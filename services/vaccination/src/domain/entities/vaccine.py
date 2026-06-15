"""Entidades de domínio - Vacinação."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass
class Vaccine:
    """Entidade de vacina do domínio."""

    id: int | None
    animal_id: int
    vaccine_name: str
    application_date: date
    next_dose_date: date | None
    veterinarian_id: int
    batch_number: str | None
    notes: str | None
    created_at: datetime | None = None

    def is_valid(self) -> bool:
        return (
            bool(self.vaccine_name.strip())
            and self.animal_id > 0
            and self.veterinarian_id > 0
            and self.application_date is not None
        )

    def is_upcoming(self, within_days: int = 7, reference_date: date | None = None) -> bool:
        """Verifica se a próxima dose está dentro do período informado."""
        if self.next_dose_date is None:
            return False
        today = reference_date or date.today()
        deadline = today + timedelta(days=within_days)
        return today <= self.next_dose_date <= deadline
