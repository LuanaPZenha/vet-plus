"""Steps Behave - Agendamento de Consultas."""

from behave import given, then, when

from tests.conftest import make_jwt_token


@given("que estou autenticado como veterinário")
def step_authenticated_veterinarian(context):
    token = make_jwt_token(user_id=1, email="vet@test.com", role="veterinarian")
    context.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


@given("que não estou autenticado")
def step_not_authenticated(context):
    context.client.credentials()


@given("existe um veterinário cadastrado no sistema")
def step_existing_veterinarian(context):
    from src.domain.entities.veterinarian import Veterinarian
    from src.infrastructure.repositories.django_veterinarian_repository import DjangoVeterinarianRepository

    repo = DjangoVeterinarianRepository()
    existing = repo.find_by_user_id(1)
    if existing:
        context.veterinarian_id = existing.id
        return

    saved = repo.save(
        Veterinarian(
            id=None,
            user_id=1,
            full_name="Dr. João Silva",
            crmv="SP-12345",
            specialty="Clínica Geral",
        )
    )
    context.veterinarian_id = saved.id


@given("existe uma consulta agendada para o animal {animal_id:d}")
def step_existing_consultation(context, animal_id):
    response = context.client.post(
        "/api/consultas/",
        {
            "animal_id": animal_id,
            "veterinarian_id": context.veterinarian_id,
            "scheduled_at": "2026-07-15T14:00:00Z",
            "type": "regular",
            "notes": "Consulta existente",
        },
        format="json",
    )
    context.last_consultation_id = response.data["id"]
    context.last_response = response


@when("eu agendo uma consulta com os dados:")
def step_schedule_consultation(context):
    row = context.table[0]
    context.last_response = context.client.post(
        "/api/consultas/",
        {
            "animal_id": int(row["animal_id"]),
            "veterinarian_id": context.veterinarian_id,
            "scheduled_at": row["scheduled_at"],
            "type": row["type"],
            "notes": row.get("notes", ""),
        },
        format="json",
    )
    if context.last_response.status_code == 201:
        context.last_consultation_id = context.last_response.data["id"]


@when("eu tento agendar uma consulta com os dados:")
def step_try_schedule_consultation(context):
    row = context.table[0]
    context.last_response = context.client.post(
        "/api/consultas/",
        {
            "animal_id": int(row["animal_id"]),
            "veterinarian_id": context.veterinarian_id,
            "scheduled_at": row["scheduled_at"],
            "type": row["type"],
        },
        format="json",
    )


@when("eu consulto os detalhes da consulta")
def step_get_consultation_details(context):
    context.last_response = context.client.get(
        f"/api/consultas/{context.last_consultation_id}/",
    )


@then("a consulta deve ser agendada com sucesso")
def step_consultation_scheduled(context):
    assert context.last_response.status_code == 201
    assert "id" in context.last_response.data


@then('o status da consulta deve ser "{expected_status}"')
def step_consultation_status(context, expected_status):
    assert context.last_response.data["status"] == expected_status


@then('o tipo da consulta deve ser "{expected_type}"')
def step_consultation_type(context, expected_type):
    assert context.last_response.data["type"] == expected_type


@then("devo receber erro de autenticação")
def step_auth_error(context):
    assert context.last_response.status_code == 403


@then("devo ver o animal_id {expected_animal_id:d}")
def step_see_animal_id(context, expected_animal_id):
    assert context.last_response.data["animal_id"] == expected_animal_id


@then('devo ver o status "{expected_status}"')
def step_see_status(context, expected_status):
    assert context.last_response.data["status"] == expected_status
