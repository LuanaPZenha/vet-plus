"""Testes de integração - Animals API."""

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


@pytest.mark.django_db
class TestAnimalsAPI:
    """TDD: Testes de integração para API de animais."""

    def test_create_animal_requires_auth(self, api_client):
        response = api_client.post(
            "/api/animais/",
            {
                "name": "Rex",
                "species": "Cão",
                "breed": "Labrador",
                "client_id": 1,
            },
            format="json",
        )
        assert response.status_code == 403

    def test_create_animal_success(self, api_client, veterinarian_headers):
        response = api_client.post(
            "/api/animais/",
            {
                "name": "Rex",
                "species": "Cão",
                "breed": "Labrador",
                "birth_date": "2020-05-10",
                "weight": "25.50",
                "client_id": 1,
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 201
        assert response.data["name"] == "Rex"
        assert response.data["species"] == "Cão"
        assert response.data["client_id"] == 1

    def test_list_animals(self, api_client, veterinarian_headers):
        api_client.post(
            "/api/animais/",
            {
                "name": "Mimi",
                "species": "Gato",
                "breed": "Siamês",
                "client_id": 2,
            },
            format="json",
            **veterinarian_headers,
        )
        response = api_client.get("/api/animais/", **veterinarian_headers)
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_get_animal_by_id(self, api_client, veterinarian_headers):
        create_response = api_client.post(
            "/api/animais/",
            {
                "name": "Thor",
                "species": "Cão",
                "breed": "Pastor",
                "client_id": 3,
            },
            format="json",
            **veterinarian_headers,
        )
        animal_id = create_response.data["id"]
        response = api_client.get(f"/api/animais/{animal_id}/", **veterinarian_headers)
        assert response.status_code == 200
        assert response.data["name"] == "Thor"

    def test_get_animal_not_found(self, api_client, veterinarian_headers):
        response = api_client.get("/api/animais/9999/", **veterinarian_headers)
        assert response.status_code == 404

    def test_add_medical_history(self, api_client, veterinarian_headers):
        create_response = api_client.post(
            "/api/animais/",
            {
                "name": "Luna",
                "species": "Gato",
                "breed": "Persa",
                "client_id": 4,
            },
            format="json",
            **veterinarian_headers,
        )
        animal_id = create_response.data["id"]
        response = api_client.post(
            f"/api/animais/{animal_id}/historico/",
            {
                "description": "Consulta de rotina - saudável",
                "record_type": "consultation",
            },
            format="json",
            **veterinarian_headers,
        )
        assert response.status_code == 201
        assert response.data["record_type"] == "consultation"

    def test_get_medical_history(self, api_client, veterinarian_headers):
        create_response = api_client.post(
            "/api/animais/",
            {
                "name": "Bob",
                "species": "Cão",
                "breed": "Poodle",
                "client_id": 5,
            },
            format="json",
            **veterinarian_headers,
        )
        animal_id = create_response.data["id"]
        api_client.post(
            f"/api/animais/{animal_id}/historico/",
            {
                "description": "Vacina V10",
                "record_type": "vaccination",
            },
            format="json",
            **veterinarian_headers,
        )
        response = api_client.get(
            f"/api/animais/{animal_id}/historico/",
            **veterinarian_headers,
        )
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["description"] == "Vacina V10"

    def test_tutor_cannot_access_other_client_animal(self, api_client, veterinarian_headers, tutor_headers):
        create_response = api_client.post(
            "/api/animais/",
            {
                "name": "OutroPet",
                "species": "Cão",
                "breed": "Vira-lata",
                "client_id": 99,
            },
            format="json",
            **veterinarian_headers,
        )
        animal_id = create_response.data["id"]
        response = api_client.get(f"/api/animais/{animal_id}/", **tutor_headers)
        assert response.status_code == 403

    def test_invalid_jwt_rejected(self, api_client):
        response = api_client.get(
            "/api/animais/",
            HTTP_AUTHORIZATION="Bearer invalid-token",
        )
        assert response.status_code == 403
