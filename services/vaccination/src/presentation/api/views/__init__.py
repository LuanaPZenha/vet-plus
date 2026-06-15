"""Views REST - Vacinação."""

from src.presentation.api.views.vaccine_views import (
    UpcomingVaccinesView,
    VaccineByAnimalView,
    VaccineDetailView,
    VaccineListCreateView,
)

__all__ = [
    "VaccineListCreateView",
    "VaccineDetailView",
    "VaccineByAnimalView",
    "UpcomingVaccinesView",
]
