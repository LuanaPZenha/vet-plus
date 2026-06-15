# TDD e BDD — Vet+ Clinic

## Test Driven Development (TDD)

O TDD segue o ciclo **Red → Green → Refactor**:

1. **Red**: Escrever um teste que falha
2. **Green**: Implementar o código mínimo para passar
3. **Refactor**: Melhorar o código mantendo os testes verdes

---

## Exemplo TDD Completo: TokenService

### Ciclo 1 — Gerar token

**Red (teste que falha):**

```python
def test_generate_token_returns_string(self, token_service, sample_user):
    token = token_service.generate_token(sample_user)
    assert isinstance(token, str)
    assert len(token) > 0
```

**Green (implementação mínima):**

```python
class TokenService:
    def generate_token(self, user: User) -> str:
        payload = {"user_id": user.id, "email": user.email}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
```

**Refactor:** Adicionar expiração, role no payload.

### Ciclo 2 — Payload completo

**Red:**

```python
def test_generate_token_contains_user_data(self, token_service, sample_user):
    token = token_service.generate_token(sample_user)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert payload["user_id"] == 1
    assert payload["role"] == "veterinarian"
```

**Green:** Adicionar campos ao payload.

---

## Exemplo TDD: Strategy de Preços

**Red:**

```python
def test_regular_consultation_price():
    strategy = RegularConsultationStrategy()
    consultation = Consultation(type=ConsultationType.REGULAR, ...)
    assert strategy.calculate(consultation) == 150.00

def test_emergency_consultation_price():
    strategy = EmergencyConsultationStrategy()
    consultation = Consultation(type=ConsultationType.EMERGENCY, ...)
    assert strategy.calculate(consultation) == 300.00
```

**Green:** Implementar cada Strategy.

**Refactor:** Extrair `PriceCalculationContext` para seleção automática.

---

## Testes Unitários (Pytest)

Localização: `services/*/tests/unit/`

| Serviço | Testes | Foco |
|---------|--------|------|
| Auth | `test_token_service.py` | JWT generation/decode |
| Consultations | `test_factory.py` | MedicalRecordFactory |
| Consultations | `test_strategy.py` | PriceCalculationStrategy |
| Consultations | `test_facade.py` | VeterinaryServiceFacade |
| Consultations | `test_observer.py` | NotificationSubject |
| Vaccination | `test_vaccine_use_cases.py` | RegisterVaccine, CheckUpcoming |

### Executar

```bash
cd services/consultations
pytest tests/unit/ -v
```

---

## Testes de Integração (Pytest)

Localização: `services/*/tests/integration/`

Testam a API REST completa (HTTP → View → Use Case → Repository → DB).

**Exemplo — Auth API:**

```python
@pytest.mark.django_db
class TestAuthAPI:
    def test_register_user_success(self, api_client):
        response = api_client.post("/api/register/", {
            "email": "tutor@test.com",
            "password": "senha1234",
            "full_name": "João Tutor",
            "role": "tutor",
        }, format="json")
        assert response.status_code == 201
        assert "access_token" in response.data

    def test_login_success(self, api_client):
        # ... register first ...
        response = api_client.post("/api/login/", {
            "email": "login@test.com",
            "password": "senha1234",
        }, format="json")
        assert response.status_code == 200
        assert response.data["token_type"] == "Bearer"
```

### Executar

```bash
cd services/auth
pytest tests/integration/ -v
```

---

## BDD com Behave

### Estrutura

```
features/
├── appointment_scheduling.feature   # Cenários em Gherkin (português)
├── environment.py                   # Setup global
└── steps/
    └── consultation_steps.py        # Step definitions
```

### Feature: Agendamento de Consulta

```gherkin
# language: pt
Funcionalidade: Agendamento de consulta
  Como tutor de um animal
  Eu quero agendar consultas veterinárias
  Para cuidar da saúde do meu pet

  Cenário: Agendar consulta com sucesso
    Dado que existe um animal cadastrado
    And existe um veterinário disponível
    When o tutor agenda uma consulta
    Then a consulta deve ser registrada
    And o status deve ser "scheduled"
```

### Feature: Controle de Vacinação

```gherkin
# language: pt
Funcionalidade: Controle de Vacinação
  Como veterinário
  Eu quero registrar vacinas aplicadas
  Para manter o controle vacinal dos animais

  Cenário: Registrar vacina
    Dado que existe um animal cadastrado
    When o veterinário registra uma vacina
    Then a vacina deve aparecer no histórico
```

### Step Definitions

```python
@given("que existe um animal cadastrado")
def step_animal_exists(context):
    context.animal_id = 1
    # ... setup via API ou fixture ...

@when("o tutor agenda uma consulta")
def step_schedule_consultation(context):
    context.response = requests.post(
        f"{BASE_URL}/api/consultas/",
        headers={"Authorization": f"Bearer {context.token}"},
        json={
            "animal_id": context.animal_id,
            "veterinarian_id": context.vet_id,
            "scheduled_at": "2024-07-01T10:00:00",
            "consultation_type": "regular",
        },
    )

@then("a consulta deve ser registrada")
def step_consultation_registered(context):
    assert context.response.status_code == 201
```

### Executar Behave

```bash
cd services/consultations
behave features/ -v

cd services/vaccination
behave features/ -v
```

---

## Cobertura de Testes por Serviço

| Serviço | Unitários | Integração | BDD |
|---------|-----------|------------|-----|
| Auth | 3 | 4 | 2 cenários |
| Clients | 6 | 6 | 2 cenários |
| Animals | 8 | 9 | 3 cenários |
| Consultations | 12 | 8 | 3 cenários |
| Vaccination | 10 | 8 | 3 cenários |
