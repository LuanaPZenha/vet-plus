from rest_framework import serializers


class RegisterMedicineSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    generic_name = serializers.CharField(max_length=200, required=False, allow_blank=True, default="")
    category = serializers.ChoiceField(
        choices=["antibiotico", "analgesico", "anti_inflamatorio", "vacina", "anestesico", "suplemento", "outro"],
    )
    unit = serializers.CharField(max_length=20, default="un")
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    min_stock = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, default=0)
    batch_number = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    expiration_date = serializers.DateField(required=False, allow_null=True)
    supplier = serializers.CharField(max_length=200, required=False, allow_null=True, allow_blank=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True, min_value=0)


class UpdateMedicineSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)
    generic_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    category = serializers.ChoiceField(
        choices=["antibiotico", "analgesico", "anti_inflamatorio", "vacina", "anestesico", "suplemento", "outro"],
        required=False,
    )
    unit = serializers.CharField(max_length=20, required=False)
    min_stock = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, min_value=0)
    batch_number = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    expiration_date = serializers.DateField(required=False, allow_null=True)
    supplier = serializers.CharField(max_length=200, required=False, allow_null=True, allow_blank=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)


class StockMovementSerializer(serializers.Serializer):
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    reason = serializers.CharField()


class MedicineResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    generic_name = serializers.CharField()
    category = serializers.CharField()
    unit = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_stock = serializers.DecimalField(max_digits=10, decimal_places=2)
    batch_number = serializers.CharField(allow_null=True)
    expiration_date = serializers.DateField(allow_null=True)
    supplier = serializers.CharField(allow_null=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    is_low_stock = serializers.BooleanField()
    is_expired = serializers.BooleanField()
    created_at = serializers.DateTimeField(allow_null=True)
    updated_at = serializers.DateTimeField(allow_null=True)


class MovementResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    medicine_id = serializers.IntegerField()
    movement_type = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    reason = serializers.CharField()
    performed_by = serializers.IntegerField()
    stock_after = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(allow_null=True)
