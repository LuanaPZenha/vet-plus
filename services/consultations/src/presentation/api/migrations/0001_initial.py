# Generated manually for Consultations microservice

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VeterinarianModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_id", models.IntegerField(db_index=True, unique=True)),
                ("full_name", models.CharField(max_length=200)),
                ("crmv", models.CharField(max_length=20, unique=True)),
                ("specialty", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Veterinário",
                "verbose_name_plural": "Veterinários",
                "db_table": "veterinarians",
                "ordering": ["full_name"],
            },
        ),
        migrations.CreateModel(
            name="ConsultationModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("animal_id", models.IntegerField(db_index=True)),
                ("scheduled_at", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("scheduled", "Agendada"),
                            ("completed", "Concluída"),
                            ("cancelled", "Cancelada"),
                        ],
                        default="scheduled",
                        max_length=20,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("regular", "Rotina"),
                            ("emergency", "Emergência"),
                            ("surgery", "Cirurgia"),
                        ],
                        max_length=20,
                    ),
                ),
                ("price", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("notes", models.TextField(blank=True, default="")),
                ("diagnosis", models.TextField(blank=True, default="")),
                ("prescription", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "veterinarian",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="consultations",
                        to="api.veterinarianmodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Consulta",
                "verbose_name_plural": "Consultas",
                "db_table": "consultations",
                "ordering": ["-scheduled_at"],
            },
        ),
    ]
