"""Implementação concreta do repositório de lembretes."""

from typing import Optional

from src.domain.entities.vaccine_reminder import VaccineReminder
from src.domain.repositories.vaccine_reminder_repository import IVaccineReminderRepository
from src.infrastructure.database.models import VaccineReminderModel


class DjangoVaccineReminderRepository(IVaccineReminderRepository):
    """Adaptador Django ORM para IVaccineReminderRepository."""

    def _to_entity(self, model: VaccineReminderModel) -> VaccineReminder:
        return VaccineReminder(
            id=model.id,
            vaccine_id=model.vaccine_id,
            animal_id=model.animal_id,
            reminder_date=model.reminder_date,
            sent=model.sent,
        )

    def save(self, reminder: VaccineReminder) -> VaccineReminder:
        if reminder.id:
            model = VaccineReminderModel.objects.get(id=reminder.id)
            model.sent = reminder.sent
            model.reminder_date = reminder.reminder_date
            model.save()
        else:
            model = VaccineReminderModel.objects.create(
                vaccine_id=reminder.vaccine_id,
                animal_id=reminder.animal_id,
                reminder_date=reminder.reminder_date,
                sent=reminder.sent,
            )
        return self._to_entity(model)

    def find_by_vaccine_id(self, vaccine_id: int) -> Optional[VaccineReminder]:
        try:
            model = VaccineReminderModel.objects.get(vaccine_id=vaccine_id)
            return self._to_entity(model)
        except VaccineReminderModel.DoesNotExist:
            return None

    def find_pending(self) -> list[VaccineReminder]:
        queryset = VaccineReminderModel.objects.filter(sent=False)
        return [self._to_entity(model) for model in queryset]

    def mark_sent(self, reminder_id: int) -> None:
        VaccineReminderModel.objects.filter(id=reminder_id).update(sent=True)
