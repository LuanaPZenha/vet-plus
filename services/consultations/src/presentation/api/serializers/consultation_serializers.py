"""Serializers REST - Consultas."""

from rest_framework import serializers


class ScheduleConsultationSerializer(serializers.Serializer):
    animal_id = serializers.IntegerField(min_value=1)
    veterinarian_id = serializers.IntegerField(min_value=1)
    scheduled_at = serializers.DateTimeField()
    type = serializers.ChoiceField(choices=["regular", "emergency", "surgery"])
    notes = serializers.CharField(required=False, allow_blank=True, default="")


class CompleteConsultationSerializer(serializers.Serializer):
    diagnosis = serializers.CharField()
    prescription_notes = serializers.CharField(required=False, allow_blank=True, default="")
    procedure = serializers.CharField(required=False, allow_blank=True, default="")


class ConsultationResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    animal_id = serializers.IntegerField()
    veterinarian_id = serializers.IntegerField()
    scheduled_at = serializers.DateTimeField()
    status = serializers.CharField()
    type = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    notes = serializers.CharField()
    diagnosis = serializers.CharField()
    prescription = serializers.CharField()
    created_at = serializers.DateTimeField()


class CreateVeterinarianSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    full_name = serializers.CharField(max_length=200)
    crmv = serializers.CharField(max_length=20)
    specialty = serializers.CharField(max_length=100)


class VeterinarianResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    full_name = serializers.CharField()
    crmv = serializers.CharField()
    specialty = serializers.CharField()
    created_at = serializers.DateTimeField()
