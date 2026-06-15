"""Step definitions para autenticação."""

import os

import django
import requests
from behave import given, then, when

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

BASE_URL = os.environ.get("AUTH_BASE_URL", "http://localhost:8001")


@given("que o serviço de autenticação está disponível")
def step_service_available(context):
    context.base_url = BASE_URL


@given('que existe um usuário "{email}" com senha "{password}"')
def step_user_exists(context, email, password):
    requests.post(
        f"{context.base_url}/api/register/",
        json={
            "email": email,
            "password": password,
            "full_name": "Usuário Teste",
            "role": "veterinarian",
        },
    )


@when('eu registro um usuário com email "{email}" e senha "{password}"')
def step_register(context, email, password):
    context.response = requests.post(
        f"{context.base_url}/api/register/",
        json={
            "email": email,
            "password": password,
            "full_name": "Tutor Teste",
            "role": "tutor",
        },
    )


@when('eu faço login com email "{email}" e senha "{password}"')
def step_login(context, email, password):
    context.response = requests.post(
        f"{context.base_url}/api/login/",
        json={"email": email, "password": password},
    )


@then("o registro deve ser realizado com sucesso")
def step_register_success(context):
    assert context.response.status_code == 201


@then("o login deve ser realizado com sucesso")
def step_login_success(context):
    assert context.response.status_code == 200


@then("um token JWT deve ser retornado")
@then("um token Bearer deve ser retornado")
def step_token_returned(context):
    data = context.response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
