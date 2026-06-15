"""URLs da API de Vacinação."""

from django.urls import path

from src.presentation.api.views.vaccine_views import (
    UpcomingVaccinesView,
    VaccineByAnimalView,
    VaccineDetailView,
    VaccineListCreateView,
)

urlpatterns = [
    path("vacinas/", VaccineListCreateView.as_view(), name="vaccines-list-create"),
    path("vacinas/proximas/", UpcomingVaccinesView.as_view(), name="vaccines-upcoming"),
    path(
        "vacinas/animal/<int:animal_id>/",
        VaccineByAnimalView.as_view(),
        name="vaccines-by-animal",
    ),
    path("vacinas/<int:pk>/", VaccineDetailView.as_view(), name="vaccine-detail"),
]
