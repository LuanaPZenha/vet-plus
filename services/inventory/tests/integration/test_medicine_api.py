import pytest
from decimal import Decimal
from rest_framework.test import APIClient

from src.domain.entities.medicine import Medicine, MedicineCategory
from src.infrastructure.repositories.django_medicine_repository import DjangoMedicineRepository


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_headers():
    import jwt
    from django.conf import settings
    token = jwt.encode(
        {"user_id": 1, "email": "vet@test.com", "role": "veterinarian"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.mark.django_db
class TestMedicineAPI:
    def test_list_medicines_empty(self, api_client, auth_headers):
        response = api_client.get("/api/medicamentos/", **auth_headers)
        assert response.status_code == 200
        assert response.data == []

    def test_create_medicine(self, api_client, auth_headers):
        response = api_client.post(
            "/api/medicamentos/",
            {
                "name": "Amoxicilina 500mg",
                "generic_name": "Amoxicilina",
                "category": "antibiotico",
                "unit": "comp",
                "quantity": "100.00",
                "min_stock": "20.00",
            },
            format="json",
            **auth_headers,
        )
        assert response.status_code == 201
        assert response.data["name"] == "Amoxicilina 500mg"

    def test_stock_entry(self, api_client, auth_headers):
        repo = DjangoMedicineRepository()
        med = repo.save(Medicine(
            id=None, name="Dipirona", generic_name="Dipirona",
            category=MedicineCategory.ANALGESIC, unit="ml",
            quantity=Decimal("50"), min_stock=Decimal("10"),
            batch_number=None, expiration_date=None, supplier=None, unit_price=None,
        ))
        response = api_client.post(
            f"/api/medicamentos/{med.id}/entrada/",
            {"quantity": "20.00", "reason": "Reposição"},
            format="json",
            **auth_headers,
        )
        assert response.status_code == 201
        assert response.data["movement_type"] == "entrada"
