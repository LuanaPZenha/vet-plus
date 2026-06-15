"""URLs da API de Animais."""

from django.urls import path

from src.presentation.api.views.animal_views import (
    AnimalDetailView,
    AnimalListCreateView,
    MedicalHistoryView,
)

urlpatterns = [
    path("animais/", AnimalListCreateView.as_view(), name="animals-list-create"),
    path("animais/<int:pk>/", AnimalDetailView.as_view(), name="animal-detail"),
    path("animais/<int:pk>/historico/", MedicalHistoryView.as_view(), name="animal-history"),
]
