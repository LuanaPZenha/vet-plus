"""Modelos de persistência Django."""

from django.db import models


class VaccineModel(models.Model):
    """Modelo ORM - mapeamento para entidade Vaccine."""

    animal_id = models.IntegerField(db_index=True)
    vaccine_name = models.CharField(max_length=200)
    application_date = models.DateField()
    next_dose_date = models.DateField(null=True, blank=True, db_index=True)
    veterinarian_id = models.IntegerField()
    batch_number = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "api"
        db_table = "vaccines"
        verbose_name = "Vacina"
        verbose_name_plural = "Vacinas"
        ordering = ["-application_date"]

    def __str__(self) -> str:
        return f"{self.vaccine_name} - Animal #{self.animal_id}"


class VaccineReminderModel(models.Model):
    """Modelo ORM - mapeamento para entidade VaccineReminder."""

    vaccine = models.ForeignKey(
        VaccineModel,
        on_delete=models.CASCADE,
        related_name="reminders",
    )
    animal_id = models.IntegerField(db_index=True)
    reminder_date = models.DateField()
    sent = models.BooleanField(default=False)

    class Meta:
        app_label = "api"
        db_table = "vaccine_reminders"
        verbose_name = "Lembrete de Vacina"
        verbose_name_plural = "Lembretes de Vacina"
        ordering = ["reminder_date"]

    def __str__(self) -> str:
        status = "enviado" if self.sent else "pendente"
        return f"Lembrete #{self.id} - {status}"
