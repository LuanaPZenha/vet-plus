"""URLs da API de Consultas."""

from django.urls import path

from src.presentation.api.views.consultation_views import (
    ConsultationCompleteView,
    ConsultationDetailView,
    ConsultationListCreateView,
    VeterinarianListCreateView,
)

urlpatterns = [
    path("consultas/", ConsultationListCreateView.as_view(), name="consultations-list-create"),
    path("consultas/<int:pk>/", ConsultationDetailView.as_view(), name="consultation-detail"),
    path("consultas/<int:pk>/concluir/", ConsultationCompleteView.as_view(), name="consultation-complete"),
    path("veterinarios/", VeterinarianListCreateView.as_view(), name="veterinarians-list-create"),
]
