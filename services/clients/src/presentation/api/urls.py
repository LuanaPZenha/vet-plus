"""URLs da API de Clientes."""

from django.urls import path

from src.presentation.api.views.client_views import ClientDetailView, ClientListCreateView

urlpatterns = [
    path("clientes/", ClientListCreateView.as_view(), name="client-list-create"),
    path("clientes/<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
]
