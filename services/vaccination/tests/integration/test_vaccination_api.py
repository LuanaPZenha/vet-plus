"""Testes de integração - Vaccination API."""

from datetime import date, timedelta

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


@pytest.mark.django_db
class TestVaccinationAPI:
    """Testes de integração para API de vacinação."""

    def test_register_vaccine_requires_auth(self, api_client):
        response = api_client.post(
            "/api/vacinas/",
            {
                "animal_id": 1,
                "vaccine_name": "V10",
                "application_date": "2026-01-10",
                "veterinarian_id": 1,
            },
            format="json",
        )
        assert response.status_code == 403

    def test_register_vaccine_success(self, api_client, veterinarian_headers):
        response = api_client.post(
            "/api/vacinas/",
            {
                "animal_id": 1,
                "vaccine_name": "V10",
                "application_date": "2026-01-10",
                "next_dose_date": "2026-07-10",
                "veterinarian_id": 1,
                "batch_number": "LOTE123",
                "notes": "Primeira dose",
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 201
        assert response.data["vaccine_name"] == "V10"
        assert response.data["animal_id"] == 1
        assert response.data["batch_number"] == "LOTE123"

    def test_list_vaccines(self, api_client, veterinarian_headers):
        api_client.post(
            "/api/vacinas/",
            {
                "animal_id": 2,
                "vaccine_name": "Antirrábica",
                "application_date": "2026-02-15",
                "veterinarian_id": 1,
            },
            format="json",
            **veterinarian_headers,
        )
        response = api_client.get("/api/vacinas/", **veterinarian_headers)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_get_vaccine_by_id(self, api_client, veterinarian_headers):
        create_response = api_client.post(
            "/api/vacinas/",
            {
                "animal_id": 3,
                "vaccine_name": "Giardia",
                "application_date": "2026-03-01",
                "veterinarian_id": 1,
            },
            format="json",
            **veterinarian_headers,
        )
        vaccine_id = create_response.data["id"]
        response = api_client.get(f"/api/vacinas/{vaccine_id}/", **veterinarian_headers)
        assert response.status_code == 200
        assert response.data["vaccine_name"] == "Giardia"

    def test_get_vaccine_not_found(self, api_client, veterinarian_headers):
        response = api_client.get("/api/vacinas/9999/", **veterinarian_headers)
        assert response.status_code == 404

    def test_get_vaccine_history_by_animal(self, api_client, veterinarian_headers):
        animal_id = 4
        api_client.post(
            "/api/vacinas/",
            {
                "animal_id": animal_id,
                "vaccine_name": "V10",
                "application_date": "2026-01-10",
                "veterinarian_id": 1,
            },
            format="json",
            **veterinarian_headers,
        )
        api_client.post(
            "/api/vacinas/",
            {
                "animal_id": animal_id,
                "vaccine_name": "Antirrábica",
                "application_date": "2026-02-15",
                "veterinarian_id": 1,
            },
            format="json",
            **veterinarian_headers,
        )
        response = api_client.get(
            f"/api/vacinas/animal/{animal_id}/",
            **veterinarian_headers,
        )
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_upcoming_vaccines(self, api_client, veterinarian_headers):
        next_week = (date.today() + timedelta(days=5)).isoformat()
        api_client.post(
            "/api/vacinas/",
            {
                "animal_id": 5,
                "vaccine_name": "V10 Reforço",
                "application_date": date.today().isoformat(),
                "next_dose_date": next_week,
                "veterinarian_id": 1,
            },
            format="json",
            **veterinarian_headers,
        )
        response = api_client.get("/api/vacinas/proximas/", **veterinarian_headers)
        assert response.status_code == 200
        assert len(response.data) >= 1
        assert response.data[0]["vaccine_name"] == "V10 Reforço"

    def test_invalid_jwt_rejected(self, api_client):
        response = api_client.get(
            "/api/vacinas/",
            HTTP_AUTHORIZATION="Bearer invalid-token",
        )
        assert response.status_code == 403

    def test_register_vaccine_invalid_data(self, api_client, veterinarian_headers):
        response = api_client.post(
            "/api/vacinas/",
            {
                "animal_id": 1,
                "vaccine_name": "",
                "application_date": "2026-01-10",
                "veterinarian_id": 1,
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 400
