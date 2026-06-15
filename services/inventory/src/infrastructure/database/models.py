from django.db import models


class MedicineModel(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True, default="")
    category = models.CharField(max_length=30)
    unit = models.CharField(max_length=20, default="un")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    batch_number = models.CharField(max_length=100, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    supplier = models.CharField(max_length=200, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "api"
        db_table = "medicines"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class StockMovementModel(models.Model):
    medicine = models.ForeignKey(MedicineModel, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    performed_by = models.IntegerField()
    stock_after = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "api"
        db_table = "stock_movements"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.movement_type} - {self.quantity}"
