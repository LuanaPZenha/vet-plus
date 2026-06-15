"""Serializers REST - Vacinação."""

from src.presentation.api.serializers.vaccine_serializers import (
    RegisterVaccineSerializer,
    UpcomingVaccineSerializer,
    VaccineResponseSerializer,
)

__all__ = ["RegisterVaccineSerializer", "VaccineResponseSerializer", "UpcomingVaccineSerializer"]
