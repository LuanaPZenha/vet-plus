"""Steps Behave - Cadastro de clientes."""

from behave import given, then, when

from features.environment import set_auth_token


@given("que possuo um token JWT válido de veterinário")
def step_valid_vet_token(context):
    set_auth_token(context, role="veterinarian", email="vet@behave.com")


@given('que já existe um cliente cadastrado com e-mail "{email}"')
def step_existing_client(context, email):
    set_auth_token(context, role="veterinarian", email="vet@behave.com")
    context.api_client.post(
        "/api/clientes/",
        {
            "nome_completo": "Cliente Existente",
            "email": email,
            "telefone": "11900001111",
            "cpf": "111.111.111-11",
            "endereco": "Rua Existente, 1",
        },
        format="json",
        **context.auth_headers,
    )


@when("eu cadastrar um cliente com os dados:")
def step_register_client(context):
    payload = {}
    if len(context.table.headings) == 2:
        payload[context.table.headings[0]] = context.table.headings[1]
    for row in context.table:
        if len(row.cells) >= 2:
            payload[row.cells[0]] = row.cells[1]

    context.last_response = context.api_client.post(
        "/api/clientes/",
        payload,
        format="json",
        **context.auth_headers,
    )


@then("o cadastro deve ser realizado com sucesso")
def step_registration_success(context):
    assert context.last_response is not None
    data = context.get_response_data(context.last_response)
    assert context.last_response.status_code == 201, data


@then('a resposta deve conter o nome "{nome}"')
def step_response_contains_name(context, nome):
    data = context.get_response_data(context.last_response)
    assert data["nome_completo"] == nome


@then('a resposta deve conter o e-mail "{email}"')
def step_response_contains_email(context, email):
    data = context.get_response_data(context.last_response)
    assert data["email"] == email


@then("o cadastro deve falhar com erro de validação")
def step_registration_validation_error(context):
    assert context.last_response is not None
    assert context.last_response.status_code == 400
