"""Serializers REST - Animais."""

from rest_framework import serializers


class CreateAnimalSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    species = serializers.CharField(max_length=100)
    breed = serializers.CharField(max_length=100)
    birth_date = serializers.DateField(required=False, allow_null=True)
    weight = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=False,
        allow_null=True,
    )
    client_id = serializers.IntegerField(min_value=1)


class AnimalResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    species = serializers.CharField()
    breed = serializers.CharField()
    birth_date = serializers.DateField(allow_null=True)
    weight = serializers.DecimalField(max_digits=6, decimal_places=2, allow_null=True)
    client_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class AddMedicalHistorySerializer(serializers.Serializer):
    description = serializers.CharField()
    record_type = serializers.ChoiceField(
        choices=[
            "consultation",
            "vaccination",
            "surgery",
            "exam",
            "medication",
            "note",
        ],
    )


class MedicalHistoryResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    animal_id = serializers.IntegerField()
    description = serializers.CharField()
    record_type = serializers.CharField()
    created_at = serializers.DateTimeField()
