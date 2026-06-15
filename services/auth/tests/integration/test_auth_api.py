"""Testes de integração - Auth API."""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestAuthAPI:
    """TDD: Testes de integração para registro e login."""

    def test_register_user_success(self, api_client):
        response = api_client.post(
            "/api/register/",
            {
                "email": "tutor@test.com",
                "password": "senha1234",
                "full_name": "João Tutor",
                "role": "tutor",
            },
            format="json",
        )
        assert response.status_code == 201
        assert "access_token" in response.data
        assert response.data["email"] == "tutor@test.com"

    def test_register_duplicate_email_fails(self, api_client):
        data = {
            "email": "dup@test.com",
            "password": "senha1234",
            "full_name": "Duplicado",
            "role": "tutor",
        }
        api_client.post("/api/register/", data, format="json")
        response = api_client.post("/api/register/", data, format="json")
        assert response.status_code == 400

    def test_login_success(self, api_client):
        api_client.post(
            "/api/register/",
            {
                "email": "login@test.com",
                "password": "senha1234",
                "full_name": "Login Test",
                "role": "veterinarian",
            },
            format="json",
        )
        response = api_client.post(
            "/api/login/",
            {"email": "login@test.com", "password": "senha1234"},
            format="json",
        )
        assert response.status_code == 200
        assert response.data["token_type"] == "Bearer"

    def test_login_invalid_credentials(self, api_client):
        response = api_client.post(
            "/api/login/",
            {"email": "naoexiste@test.com", "password": "wrong"},
            format="json",
        )
        assert response.status_code == 401
