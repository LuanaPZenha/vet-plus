"""Testes de integração - Consultations API."""

import pytest
from rest_framework.test import APIClient

from tests.conftest import make_jwt_token


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def veterinarian_headers():
    token = make_jwt_token(user_id=1, email="vet@test.com", role="veterinarian")
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture
def tutor_headers():
    token = make_jwt_token(user_id=10, email="tutor@test.com", role="tutor")
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture
def veterinarian_id(api_client, veterinarian_headers):
    response = api_client.post(
        "/api/veterinarios/",
        {
            "user_id": 1,
            "full_name": "Dr. João Silva",
            "crmv": "SP-12345",
            "specialty": "Clínica Geral",
        },
        format="json",
        **veterinarian_headers,
    )
    assert response.status_code == 201
    return response.data["id"]


@pytest.mark.django_db
class TestConsultationsAPI:
    """Testes de integração para API de consultas."""

    def test_create_veterinarian_requires_auth(self, api_client):
        response = api_client.post(
            "/api/veterinarios/",
            {
                "user_id": 1,
                "full_name": "Dr. Test",
                "crmv": "SP-99999",
                "specialty": "Geral",
            },
            format="json",
        )
        assert response.status_code == 403

    def test_create_veterinarian_success(self, api_client, veterinarian_headers):
        response = api_client.post(
            "/api/veterinarios/",
            {
                "user_id": 2,
                "full_name": "Dra. Maria",
                "crmv": "SP-54321",
                "specialty": "Cirurgia",
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 201
        assert response.data["full_name"] == "Dra. Maria"

    def test_list_veterinarians(self, api_client, veterinarian_headers, veterinarian_id):
        response = api_client.get("/api/veterinarios/", **veterinarian_headers)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_schedule_consultation_requires_auth(self, api_client):
        response = api_client.post(
            "/api/consultas/",
            {
                "animal_id": 1,
                "veterinarian_id": 1,
                "scheduled_at": "2026-06-20T10:00:00Z",
                "type": "regular",
            },
            format="json",
        )
        assert response.status_code == 403

    def test_schedule_consultation_success(self, api_client, veterinarian_headers, veterinarian_id):
        response = api_client.post(
            "/api/consultas/",
            {
                "animal_id": 1,
                "veterinarian_id": veterinarian_id,
                "scheduled_at": "2026-06-20T10:00:00Z",
                "type": "regular",
                "notes": "Check-up anual",
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 201
        assert response.data["status"] == "scheduled"
        assert response.data["type"] == "regular"
        assert response.data["animal_id"] == 1

    def test_list_consultations(self, api_client, veterinarian_headers, veterinarian_id):
        api_client.post(
            "/api/consultas/",
            {
                "animal_id": 2,
                "veterinarian_id": veterinarian_id,
                "scheduled_at": "2026-06-21T14:00:00Z",
                "type": "emergency",
            },
            format="json",
            **veterinarian_headers,
        )
        response = api_client.get("/api/consultas/", **veterinarian_headers)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_get_consultation_by_id(self, api_client, veterinarian_headers, veterinarian_id):
        create_response = api_client.post(
            "/api/consultas/",
            {
                "animal_id": 3,
                "veterinarian_id": veterinarian_id,
                "scheduled_at": "2026-06-22T09:00:00Z",
                "type": "regular",
            },
            format="json",
            **veterinarian_headers,
        )
        consultation_id = create_response.data["id"]
        response = api_client.get(f"/api/consultas/{consultation_id}/", **veterinarian_headers)
        assert response.status_code == 200
        assert response.data["animal_id"] == 3

    def test_get_consultation_not_found(self, api_client, veterinarian_headers):
        response = api_client.get("/api/consultas/9999/", **veterinarian_headers)
        assert response.status_code == 404

    def test_complete_consultation_regular(self, api_client, veterinarian_headers, veterinarian_id):
        create_response = api_client.post(
            "/api/consultas/",
            {
                "animal_id": 4,
                "veterinarian_id": veterinarian_id,
                "scheduled_at": "2026-06-23T11:00:00Z",
                "type": "regular",
            },
            format="json",
            **veterinarian_headers,
        )
        consultation_id = create_response.data["id"]
        response = api_client.patch(
            f"/api/consultas/{consultation_id}/concluir/",
            {
                "diagnosis": "Animal saudável",
                "prescription_notes": "Continuar dieta atual",
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 200
        assert response.data["status"] == "completed"
        assert float(response.data["price"]) == 150.00
        assert response.data["diagnosis"] == "Animal saudável"
        assert "PRESCRIÇÃO" in response.data["prescription"]

    def test_complete_consultation_emergency_price(self, api_client, veterinarian_headers, veterinarian_id):
        create_response = api_client.post(
            "/api/consultas/",
            {
                "animal_id": 5,
                "veterinarian_id": veterinarian_id,
                "scheduled_at": "2026-06-24T16:00:00Z",
                "type": "emergency",
            },
            format="json",
            **veterinarian_headers,
        )
        consultation_id = create_response.data["id"]
        response = api_client.patch(
            f"/api/consultas/{consultation_id}/concluir/",
            {"diagnosis": "Febre"},
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 200
        assert float(response.data["price"]) == 300.00

    def test_complete_consultation_surgery_price(self, api_client, veterinarian_headers, veterinarian_id):
        create_response = api_client.post(
            "/api/consultas/",
            {
                "animal_id": 6,
                "veterinarian_id": veterinarian_id,
                "scheduled_at": "2026-06-25T08:00:00Z",
                "type": "surgery",
            },
            format="json",
            **veterinarian_headers,
        )
        consultation_id = create_response.data["id"]
        response = api_client.patch(
            f"/api/consultas/{consultation_id}/concluir/",
            {
                "diagnosis": "Fratura",
                "procedure": "Fixação",
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 200
        assert float(response.data["price"]) == 800.00

    def test_schedule_consultation_invalid_veterinarian(self, api_client, veterinarian_headers):
        response = api_client.post(
            "/api/consultas/",
            {
                "animal_id": 1,
                "veterinarian_id": 9999,
                "scheduled_at": "2026-06-20T10:00:00Z",
                "type": "regular",
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 400

    def test_tutor_can_schedule_consultation(self, api_client, veterinarian_id, tutor_headers):
        response = api_client.post(
            "/api/consultas/",
            {
                "animal_id": 7,
                "veterinarian_id": veterinarian_id,
                "scheduled_at": "2026-06-26T10:00:00Z",
                "type": "regular",
            },
            format="json",
            **tutor_headers,
        )
        assert response.status_code == 201

    def test_invalid_jwt_rejected(self, api_client):
        response = api_client.get(
            "/api/consultas/",
            HTTP_AUTHORIZATION="Bearer invalid-token",
        )
        assert response.status_code == 403
