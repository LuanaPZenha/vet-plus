"""Modelos de persistência Django."""

from django.db import models


class AnimalModel(models.Model):
    """Modelo ORM - mapeamento para entidade Animal."""

    name = models.CharField(max_length=200)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    client_id = models.IntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "api"
        db_table = "animals"
        verbose_name = "Animal"
        verbose_name_plural = "Animais"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.species})"


class MedicalHistoryModel(models.Model):
    """Modelo ORM - mapeamento para entidade MedicalHistoryEntry."""

    class RecordType(models.TextChoices):
        CONSULTATION = "consultation", "Consulta"
        VACCINATION = "vaccination", "Vacinação"
        SURGERY = "surgery", "Cirurgia"
        EXAM = "exam", "Exame"
        MEDICATION = "medication", "Medicação"
        NOTE = "note", "Observação"

    animal = models.ForeignKey(
        AnimalModel,
        on_delete=models.CASCADE,
        related_name="medical_history",
    )
    description = models.TextField()
    record_type = models.CharField(max_length=20, choices=RecordType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "api"
        db_table = "medical_history"
        verbose_name = "Histórico Médico"
        verbose_name_plural = "Históricos Médicos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.record_type} - Animal #{self.animal_id}"
