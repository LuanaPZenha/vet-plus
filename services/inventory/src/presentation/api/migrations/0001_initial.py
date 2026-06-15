from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MedicineModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("generic_name", models.CharField(blank=True, default="", max_length=200)),
                ("category", models.CharField(max_length=30)),
                ("unit", models.CharField(default="un", max_length=20)),
                ("quantity", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("min_stock", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("batch_number", models.CharField(blank=True, max_length=100, null=True)),
                ("expiration_date", models.DateField(blank=True, null=True)),
                ("supplier", models.CharField(blank=True, max_length=200, null=True)),
                ("unit_price", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "medicines",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="StockMovementModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("movement_type", models.CharField(max_length=10)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                ("reason", models.TextField()),
                ("performed_by", models.IntegerField()),
                ("stock_after", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("medicine", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="movements", to="api.medicinemodel")),
            ],
            options={
                "db_table": "stock_movements",
                "ordering": ["-created_at"],
            },
        ),
    ]
