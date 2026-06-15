"""Serializers REST - Vacinação."""

from rest_framework import serializers


class RegisterVaccineSerializer(serializers.Serializer):
    animal_id = serializers.IntegerField(min_value=1)
    vaccine_name = serializers.CharField(max_length=200)
    application_date = serializers.DateField()
    next_dose_date = serializers.DateField(required=False, allow_null=True)
    veterinarian_id = serializers.IntegerField(min_value=1)
    batch_number = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class VaccineResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    animal_id = serializers.IntegerField()
    vaccine_name = serializers.CharField()
    application_date = serializers.DateField()
    next_dose_date = serializers.DateField(allow_null=True)
    veterinarian_id = serializers.IntegerField()
    batch_number = serializers.CharField(allow_null=True)
    notes = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()


class UpcomingVaccineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    animal_id = serializers.IntegerField()
    vaccine_name = serializers.CharField()
    next_dose_date = serializers.DateField()
    days_until_due = serializers.IntegerField()
