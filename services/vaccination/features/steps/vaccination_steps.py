"""Steps Behave - Controle de Vacinação."""

from behave import given, then, when

from tests.conftest import make_jwt_token


@given("que estou autenticado como veterinário")
def step_authenticated_veterinarian(context):
    token = make_jwt_token(user_id=1, email="vet@test.com", role="veterinarian")
    context.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


@given("que não estou autenticado")
def step_not_authenticated(context):
    context.client.credentials()


@given('existe uma vacina "{vaccine_name}" para o animal {animal_id:d}')
def step_existing_vaccine(context, vaccine_name, animal_id):
    token = make_jwt_token(user_id=1, email="vet@test.com", role="veterinarian")
    context.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = context.client.post(
        "/api/vacinas/",
        {
            "animal_id": animal_id,
            "vaccine_name": vaccine_name,
            "application_date": "2026-02-15",
            "veterinarian_id": 1,
        },
        format="json",
    )
    context.last_vaccine_id = response.data["id"]
    context.last_response = response


@when("eu registro uma vacina com os dados:")
def step_register_vaccine(context):
    row = context.table[0]
    data = {
        "animal_id": int(row["animal_id"]),
        "vaccine_name": row["vaccine_name"],
        "application_date": row["application_date"],
        "veterinarian_id": int(row["veterinarian_id"]),
    }
    if "next_dose_date" in row.headings and row["next_dose_date"]:
        data["next_dose_date"] = row["next_dose_date"]
    if "batch_number" in row.headings and row["batch_number"]:
        data["batch_number"] = row["batch_number"]
    if "notes" in row.headings and row["notes"]:
        data["notes"] = row["notes"]

    context.last_response = context.client.post(
        "/api/vacinas/",
        data,
        format="json",
    )
    if context.last_response.status_code == 201:
        context.last_vaccine_id = context.last_response.data["id"]


@when("eu tento registrar uma vacina com os dados:")
def step_try_register_vaccine(context):
    row = context.table[0]
    context.last_response = context.client.post(
        "/api/vacinas/",
        {
            "animal_id": int(row["animal_id"]),
            "vaccine_name": row["vaccine_name"],
            "application_date": row["application_date"],
            "veterinarian_id": int(row["veterinarian_id"]),
        },
        format="json",
    )


@when("eu consulto o histórico de vacinação do animal {animal_id:d}")
def step_get_vaccine_history(context, animal_id):
    context.last_response = context.client.get(
        f"/api/vacinas/animal/{animal_id}/",
    )


@then("a vacina deve ser registrada com sucesso")
def step_vaccine_registered(context):
    assert context.last_response.status_code == 201
    assert "id" in context.last_response.data


@then('o nome da vacina deve ser "{expected_name}"')
def step_vaccine_name(context, expected_name):
    assert context.last_response.data["vaccine_name"] == expected_name


@then("o animal da vacina deve ser {expected_animal_id:d}")
def step_vaccine_animal(context, expected_animal_id):
    assert context.last_response.data["animal_id"] == expected_animal_id


@then("devo receber erro de autenticação")
def step_auth_error(context):
    assert context.last_response.status_code == 403


@then('devo ver a vacina "{expected_name}" no histórico')
def step_see_vaccine_in_history(context, expected_name):
    assert context.last_response.status_code == 200
    names = [item["vaccine_name"] for item in context.last_response.data]
    assert expected_name in names
