from django.urls import path

from src.presentation.api.views.medicine_views import (
    LowStockView,
    MedicineDetailView,
    MedicineListCreateView,
    MovementsListView,
    StockEntryView,
    StockExitView,
)

urlpatterns = [
    path("medicamentos/", MedicineListCreateView.as_view(), name="medicines-list-create"),
    path("medicamentos/baixo-estoque/", LowStockView.as_view(), name="medicines-low-stock"),
    path("medicamentos/movimentacoes/", MovementsListView.as_view(), name="movements-list"),
    path("medicamentos/<int:pk>/", MedicineDetailView.as_view(), name="medicine-detail"),
    path("medicamentos/<int:pk>/entrada/", StockEntryView.as_view(), name="stock-entry"),
    path("medicamentos/<int:pk>/saida/", StockExitView.as_view(), name="stock-exit"),
]
