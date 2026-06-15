"""Steps Behave - Registro de Animais."""

from behave import given, then, when

from tests.conftest import make_jwt_token


@given("que estou autenticado como veterinário")
def step_authenticated_veterinarian(context):
    token = make_jwt_token(user_id=1, email="vet@test.com", role="veterinarian")
    context.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


@given("que não estou autenticado")
def step_not_authenticated(context):
    context.client.credentials()


@given('existe um animal "{name}" do tipo "{species}" para o cliente {client_id:d}')
def step_existing_animal(context, name, species, client_id):
    token = make_jwt_token(user_id=1, email="vet@test.com", role="veterinarian")
    context.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = context.client.post(
        "/api/animais/",
        {
            "name": name,
            "species": species,
            "breed": "SRD",
            "client_id": client_id,
        },
        format="json",
    )
    context.last_animal_id = response.data["id"]
    context.last_response = response


@when("eu registro um animal com os dados:")
def step_register_animal(context):
    row = context.table[0]
    data = {
        "name": row["name"],
        "species": row["species"],
        "breed": row["breed"],
        "client_id": int(row["client_id"]),
    }
    if "birth_date" in row.headings and row["birth_date"]:
        data["birth_date"] = row["birth_date"]
    if "weight" in row.headings and row["weight"]:
        data["weight"] = row["weight"]

    context.last_response = context.client.post(
        "/api/animais/",
        data,
        format="json",
    )
    if context.last_response.status_code == 201:
        context.last_animal_id = context.last_response.data["id"]


@when("eu tento registrar um animal com os dados:")
def step_try_register_animal(context):
    row = context.table[0]
    context.last_response = context.client.post(
        "/api/animais/",
        {
            "name": row["name"],
            "species": row["species"],
            "breed": row["breed"],
            "client_id": int(row["client_id"]),
        },
        format="json",
    )


@when("eu consulto os detalhes do animal")
def step_get_animal_details(context):
    context.last_response = context.client.get(
        f"/api/animais/{context.last_animal_id}/",
    )


@then("o animal deve ser criado com sucesso")
def step_animal_created(context):
    assert context.last_response.status_code == 201
    assert "id" in context.last_response.data


@then('o nome do animal deve ser "{expected_name}"')
def step_animal_name(context, expected_name):
    assert context.last_response.data["name"] == expected_name


@then('a espécie do animal deve ser "{expected_species}"')
def step_animal_species(context, expected_species):
    assert context.last_response.data["species"] == expected_species


@then("devo receber erro de autenticação")
def step_auth_error(context):
    assert context.last_response.status_code == 403


@then('devo ver o nome "{expected_name}"')
def step_see_name(context, expected_name):
    assert context.last_response.data["name"] == expected_name


@then('devo ver a espécie "{expected_species}"')
def step_see_species(context, expected_species):
    assert context.last_response.data["species"] == expected_species
