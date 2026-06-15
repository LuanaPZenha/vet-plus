"""Testes de integração - Clients API."""

from datetime import datetime, timedelta, timezone

import jwt
import pytest
from django.conf import settings
from rest_framework.test import APIClient


def make_jwt_token(user_id=1, email="vet@test.com", role="veterinarian"):
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_headers():
    token = make_jwt_token()
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.mark.django_db
class TestClientsAPI:
    """TDD: Testes de integração para API de clientes."""

    def test_create_client_success(self, api_client, auth_headers):
        response = api_client.post(
            "/api/clientes/",
            {
                "nome_completo": "João Tutor",
                "email": "joao@test.com",
                "telefone": "11999998888",
                "cpf": "123.456.789-00",
                "endereco": "Rua das Flores, 100",
            },
            format="json",
            **auth_headers,
        )
        assert response.status_code == 201
        assert response.data["nome_completo"] == "João Tutor"
        assert response.data["email"] == "joao@test.com"
        assert "id" in response.data
        assert "criado_em" in response.data

    def test_create_client_duplicate_email_fails(self, api_client, auth_headers):
        data = {
            "nome_completo": "Duplicado",
            "email": "dup@test.com",
            "telefone": "11988887777",
            "cpf": "111.222.333-44",
            "endereco": "Rua A, 1",
        }
        api_client.post("/api/clientes/", data, format="json", **auth_headers)
        response = api_client.post("/api/clientes/", data, format="json", **auth_headers)
        assert response.status_code == 400

    def test_create_client_without_auth_fails(self, api_client):
        response = api_client.post(
            "/api/clientes/",
            {
                "nome_completo": "Sem Auth",
                "email": "semauth@test.com",
                "telefone": "11977776666",
                "cpf": "222.333.444-55",
                "endereco": "Rua B, 2",
            },
            format="json",
        )
        assert response.status_code == 403

    def test_create_client_tutor_role_forbidden(self, api_client):
        token = make_jwt_token(role="tutor", email="tutor@test.com")
        response = api_client.post(
            "/api/clientes/",
            {
                "nome_completo": "Tutor Tentando",
                "email": "tutor@test.com",
                "telefone": "11966665555",
                "cpf": "333.444.555-66",
                "endereco": "Rua C, 3",
            },
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        assert response.status_code == 403

    def test_list_clients_success(self, api_client, auth_headers):
        api_client.post(
            "/api/clientes/",
            {
                "nome_completo": "Lista Test",
                "email": "lista@test.com",
                "telefone": "11955554444",
                "cpf": "444.555.666-77",
                "endereco": "Rua D, 4",
            },
            format="json",
            **auth_headers,
        )
        response = api_client.get("/api/clientes/", **auth_headers)
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) >= 1

    def test_get_client_success(self, api_client, auth_headers):
        create_response = api_client.post(
            "/api/clientes/",
            {
                "nome_completo": "Detalhe Test",
                "email": "detalhe@test.com",
                "telefone": "11944443333",
                "cpf": "555.666.777-88",
                "endereco": "Rua E, 5",
            },
            format="json",
            **auth_headers,
        )
        client_id = create_response.data["id"]
        response = api_client.get(f"/api/clientes/{client_id}/", **auth_headers)
        assert response.status_code == 200
        assert response.data["id"] == client_id
        assert response.data["nome_completo"] == "Detalhe Test"

    def test_get_client_not_found(self, api_client, auth_headers):
        response = api_client.get("/api/clientes/99999/", **auth_headers)
        assert response.status_code == 404

    def test_tutor_can_list_and_get_clients(self, api_client, auth_headers):
        token = make_jwt_token(role="tutor", email="tutor2@test.com")
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"}

        create_response = api_client.post(
            "/api/clientes/",
            {
                "nome_completo": "Cliente Tutor",
                "email": "cliente-tutor@test.com",
                "telefone": "11933332222",
                "cpf": "666.777.888-99",
                "endereco": "Rua F, 6",
            },
            format="json",
            **auth_headers,
        )
        client_id = create_response.data["id"]

        list_response = api_client.get("/api/clientes/", **headers)
        assert list_response.status_code == 200

        detail_response = api_client.get(f"/api/clientes/{client_id}/", **headers)
        assert detail_response.status_code == 200
