"""Modelos de persistência Django."""

from django.db import models


class VeterinarianModel(models.Model):
    """Modelo ORM - mapeamento para entidade Veterinarian."""

    user_id = models.IntegerField(unique=True, db_index=True)
    full_name = models.CharField(max_length=200)
    crmv = models.CharField(max_length=20, unique=True)
    specialty = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "api"
        db_table = "veterinarians"
        verbose_name = "Veterinário"
        verbose_name_plural = "Veterinários"
        ordering = ["full_name"]

    def __str__(self) -> str:
        return f"{self.full_name} (CRMV {self.crmv})"


class ConsultationModel(models.Model):
    """Modelo ORM - mapeamento para entidade Consultation."""

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Agendada"
        COMPLETED = "completed", "Concluída"
        CANCELLED = "cancelled", "Cancelada"

    class Type(models.TextChoices):
        REGULAR = "regular", "Rotina"
        EMERGENCY = "emergency", "Emergência"
        SURGERY = "surgery", "Cirurgia"

    animal_id = models.IntegerField(db_index=True)
    veterinarian = models.ForeignKey(
        VeterinarianModel,
        on_delete=models.PROTECT,
        related_name="consultations",
    )
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )
    type = models.CharField(max_length=20, choices=Type.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    diagnosis = models.TextField(blank=True, default="")
    prescription = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "api"
        db_table = "consultations"
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ["-scheduled_at"]

    def __str__(self) -> str:
        return f"Consulta #{self.id} - Animal {self.animal_id}"
