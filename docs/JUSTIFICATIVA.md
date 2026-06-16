# Justificativa Técnica — Vet Plus+

Documento acadêmico que descreve o **problema de negócio** abordado pelo sistema e a **fundamentação técnica** das decisões de arquitetura, tecnologia e qualidade de software adotadas no projeto.

---

## 1. Descrição do Problema Escolhido

O gerenciamento operacional de clínicas veterinárias envolve uma complexa orquestração de fluxos de trabalho que vão desde o controle estrito de insumos até o acompanhamento do ciclo de vida clínico dos pacientes (animais de estimação). Sistemas legados ou centralizados (monolíticos) aplicados a esse cenário frequentemente enfrentam gargalos severos devido à natureza heterogênea de suas operações.

Os principais desafios identificados no cenário de clínicas veterinárias que o **Vet Plus+** visa resolver incluem:

### Acoplamento de domínios distintos

Fluxos essencialmente dinâmicos, como o agendamento de consultas urgentes, acabam competindo por recursos computacionais com rotinas pesadas de escrita e auditoria, como o controle de movimentação de grandes estoques de medicamentos.

### Rastreabilidade e integridade histórica

A falta de padronização no registro do prontuário médico e do histórico vacinal dos animais compromete a segurança clínica dos tratamentos e a tomada de decisão dos veterinários.

### Complexidade de regras de negócio variáveis

O cálculo de preços de procedimentos, a aplicação de regras de perfis de acesso (médicos, administradores e tutores) e o disparo de alertas para baixas de estoque ou vacinas pendentes exigem uma arquitetura flexível. Alterações em uma regra fiscal ou de negócio não podem desestabilizar o sistema como um todo.

---

## 2. Justificativa Técnica das Escolhas Realizadas

Para solucionar o problema proposto de forma escalável e manutenível, as seguintes decisões de arquitetura e tecnologia foram adotadas.

### 2.1. Arquitetura de microsserviços e isolamento de dados

**Abordagem Database-per-Service**

O sistema foi dividido em **6 microsserviços independentes**: Auth, Clients, Animals, Consultations, Vaccination e Inventory. Em ambiente local (`docker compose`), cada serviço possui seu próprio container **PostgreSQL 16**. Isso garante desacoplamento e impede que uma falha em um módulo (por exemplo, estoque) derrube funções críticas (por exemplo, triagem e consultas).

**Estratégia de schemas isolados para produção (Render)**

Visando contornar as limitações orçamentárias e de recursos do ambiente de produção em nuvem (plano gratuito do Render), adotou-se o **isolamento lógico via PostgreSQL Schemas**. Auth utiliza o schema `public`; os demais serviços usam schemas dedicados (`clients`, `animals`, `consultations`, `vaccination`, `inventory`). Essa abordagem emula o comportamento de bancos fisicamente separados, eliminando conflitos de migrações (`django_migrations`) sem onerar a infraestrutura com múltiplos bancos pagos.

O script `shared/prepare_postgres_schema.py` cria cada schema antes das migrations no startup do container de produção.

**Comunicação inter-serviços baseada em IDs**

A ausência de chaves estrangeiras físicas (Foreign Keys) entre os bancos dos serviços preserva a autonomia de cada domínio. A consistência dos dados e a validação de existência (por exemplo, confirmar se um `animal_id` existe ao registrar uma vacina) são resolvidas em tempo de execução via **requisições HTTP internas**, encapsuladas em clientes compartilhados (`shared/animal_client.py`).

**Stack de entrega**

- **Backend:** Python 3.13, Django 5.x, Django REST Framework, Gunicorn  
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS  
- **Autenticação:** JWT (PyJWT) com validação local ou via endpoint `POST /api/verify-token/`  
- **Containerização:** Docker e Docker Compose (local); Render (produção)  
- **Documentação de API:** drf-spectacular (OpenAPI / Swagger)

### 2.2. Clean Architecture e princípios SOLID

**Independência de framework**

A aplicação das camadas da Arquitetura Limpa (**Domain**, **Application**, **Infrastructure**, **Presentation**) garante que as regras essenciais de negócio permaneçam na camada interna (Domain), sem acoplamento ao Django ou ao protocolo HTTP. O Django REST Framework atua nas camadas externas como detalhe de infraestrutura de entrega e persistência.

A regra de dependência aponta sempre para dentro: **Presentation → Application → Domain**. A Infrastructure implementa contratos definidos no Domain.

**Alta manutenibilidade via casos de uso unificados**

Na camada de Application, cada fluxo de negócio relevante possui um caso de uso dedicado (por exemplo, `ScheduleConsultationUseCase`, `RegisterVaccineUseCase`). Isso simplifica depuração e isolamento de erros, favorecendo o cumprimento dos princípios **Responsabilidade Única (SRP)** e **Aberto/Fechado (OCP)**.

Detalhamento completo dos princípios SOLID aplicados: [SOLID.md](SOLID.md).

### 2.3. Design Patterns aplicados

Os padrões foram escolhidos conforme a necessidade real de cada domínio. Detalhamento ampliado: [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md).

| Pattern | Onde | Finalidade |
|---------|------|------------|
| **Repository** | Todos os microsserviços | Abstrair persistência |
| **Strategy** | Consultations | Cálculo de preço por tipo de consulta |
| **Factory Method** | Consultations | Criação de registros médicos |
| **Facade** | Consultations | Orquestração da conclusão de consulta |
| **Observer** | Consultations, Vaccination | Notificações e lembretes |

---

## 3. Design Patterns — Análise detalhada

### 3.1. Repository Pattern (Padrão Repositório)

**Por que foi escolhido?**  
Para isolar completamente a lógica de negócio (domínio) de como os dados são salvos ou buscados (infraestrutura).

**O problema que resolve:**  
Sem o Repository, os casos de uso chamariam diretamente o ORM do Django (por exemplo, `AnimalModel.objects.all()`). Se fosse necessário trocar o framework, usar outro banco ou simular dados em testes, seria preciso alterar o núcleo do sistema.

**Impacto na Arquitetura Limpa:**  
A camada Domain define apenas uma interface (`IAnimalRepository`, `IConsultationRepository`, etc.). A implementação concreta (`DjangoAnimalRepository`) fica na Infrastructure. Isso facilita testes unitários com mocks, sem depender do PostgreSQL em execução.

---

### 3.2. Strategy Pattern (Padrão Estratégia)

**Por que foi escolhido?**  
Para lidar com algoritmos variáveis de cálculo — neste caso, o **preço da consulta** conforme o tipo de atendimento — sem proliferar condicionais (`if/else`) no código.

**O problema que resolve:**  
Clínicas veterinárias expandem serviços constantemente: rotina, emergência, cirurgia, retorno, teleconsulta. Calcular o preço de cada modalidade com condicionais cria código rígido e difícil de manter, violando o princípio Aberto/Fechado (OCP) do SOLID.

**Impacto na Arquitetura Limpa:**  
Com o `PriceCalculationContext`, uma nova modalidade (por exemplo, **Teleconsulta**) exige apenas uma nova estratégia (`TeleconsultationPriceStrategy`) que implementa a interface de cálculo, sem alterar o fluxo existente de conclusão de consulta.

---

### 3.3. Factory Method (Padrão Fábrica)

**Por que foi escolhido?**  
Para centralizar e encapsular a criação de objetos complexos — neste caso, os **diferentes tipos de registros médicos** no prontuário.

**O problema que resolve:**  
A criação de um registro clínico exige parâmetros distintos conforme o contexto: consulta comum, procedimento cirúrgico ou triagem rápida geram estruturas diferentes. Instanciar essas classes diretamente espalha lógica de criação e acopla o consumidor à forma de construção.

**Impacto na Arquitetura Limpa:**  
A `MedicalRecordFactory` decide qual classe instanciar e como configurá-la. O caso de uso apenas solicita o registro adequado à fábrica, sem conhecer detalhes internos de cada tipo.

---

### 3.4. Facade Pattern (Padrão Fachada)

**Por que foi escolhido?**  
Para fornecer uma **interface unificada e simplificada** que gerencia um fluxo complexo envolvendo vários subsistemas — a conclusão de uma consulta veterinária.

**O problema que resolve:**  
Ao concluir um atendimento, o sistema precisa, em sequência: buscar dados do animal, calcular o valor final, atualizar o status da consulta, gerar registro no prontuário (microsserviço Animals), gerar prescrição e persistir o resultado. Se a View da API gerenciasse tudo isso, ficaria inflada, confusa e altamente acoplada.

**Impacto na Arquitetura Limpa:**  
O `VeterinaryServiceFacade` concentra a orquestração na camada de Application. A Presentation (API View) faz uma chamada simples — `complete_consultation(...)` — e a complexidade permanece encapsulada.

---

### 3.5. Observer Pattern (Padrão Observador)

**Por que foi escolhido?**  
Para criar um mecanismo reativo, permitindo que múltiplos módulos reajam a eventos importantes de forma **desacoplada**.

**O problema que resolve:**  
Quando ocorre um evento relevante (agendamento de consulta, registro de vacina), ações secundárias devem ser disparadas: confirmação, lembrete de retorno, alerta de próxima dose. Sem o Observer, a classe que agenda a consulta precisaria conhecer diretamente serviços de e-mail, calendário e notificação.

**Impacto na Arquitetura Limpa:**  
O emissor do evento não precisa saber quem escuta. O `VaccineReminderObserver`, por exemplo, reage ao registro de vacinas e calcula lembretes de próxima dose de forma isolada, preservando a coesão do módulo de vacinação.

---

## 4. Qualidade de software com TDD e BDD

O projeto adota **duas abordagens complementares** de testes:

| Abordagem | Ferramenta | Objetivo |
|-----------|------------|----------|
| **TDD** | Pytest | Garantir correção técnica das camadas (domínio, casos de uso, API) |
| **BDD** | Behave | Validar comportamento do ponto de vista do usuário da clínica |

A seção **[8. Como funcionam os testes](#8-como-funcionam-os-testes-no-vet-plus)** deste documento descreve em detalhe a estrutura, execução e fluxo de cada tipo de teste. Complemento com exemplos de ciclo Red/Green/Refactor: [TDD_BDD.md](TDD_BDD.md).

---

## 5. Clean Code

Práticas documentadas com exemplos concretos do código:

- Nomes significativos e intenção clara  
- Métodos pequenos e coesos  
- Tratamento de erros com exceções de domínio  
- DTOs para transferência entre camadas  
- Ausência de lógica de negócio nas Views  

Referência: [CLEAN_CODE.md](CLEAN_CODE.md).

---

## 6. Deploy e disponibilização

**Plataforma escolhida:** [Render](https://render.com) (plano gratuito para fins acadêmicos).

| Recurso | URL / descrição |
|---------|-----------------|
| **Aplicação (frontend + APIs)** | https://vet-plus.onrender.com |
| **Autenticação** | https://vet-plus-auth.onrender.com |
| **Blueprint** | `render.yaml` na raiz do repositório |

**Por que Render?**

- Integração nativa com GitHub e deploy automático  
- Suporte a Docker sem configuração complexa de orquestração  
- PostgreSQL gerenciado incluso no plano free (1 banco — resolvido via schemas)  
- HTTPS e domínio público sem custo adicional para demonstração acadêmica  

Guia completo: [RENDER.md](RENDER.md).

---

## 8. Como funcionam os testes no Vet Plus+

Esta seção explica **como os testes estão organizados**, **o que cada camada valida** e **como executá-los** em qualquer microsserviço do projeto.

### 8.1. Visão geral: pirâmide de testes

O Vet Plus+ segue a **pirâmide de testes** clássica, adaptada à arquitetura de microsserviços:

```
                    ┌─────────────┐
                    │    BDD      │  Behave — comportamento (5 serviços)
                    │  (Gherkin)  │
                ┌───┴─────────────┴───┐
                │    Integração       │  Pytest — API REST ponta a ponta
                │  (HTTP + DB teste)  │
            ┌───┴─────────────────────┴───┐
            │        Unitários            │  Pytest — domínio, use cases, patterns
            │   (sem HTTP, mocks/repos)   │
            └─────────────────────────────┘
```

| Camada | O que testa | Depende de |
|--------|-------------|------------|
| **Unitário** | Regras de negócio isoladas | Nada externo (ou mocks) |
| **Integração** | View → Use Case → Repository → banco | Django test DB (SQLite em memória) |
| **BDD** | Fluxos completos na linguagem do negócio | APIClient + banco de teste |

Cada microsserviço possui sua **própria suíte de testes independente**, coerente com o isolamento de domínio da arquitetura.

---

### 8.2. Estrutura de pastas (padrão em todos os serviços)

```
services/<microsserviço>/
├── tests/
│   ├── conftest.py          # Fixtures compartilhadas (JWT, headers, api_client)
│   ├── unit/                # Testes unitários
│   │   └── test_*.py
│   └── integration/         # Testes de integração da API REST
│       └── test_*_api.py
├── features/                # BDD (Behave) — onde aplicável
│   ├── *.feature            # Cenários em Gherkin (português)
│   ├── environment.py       # Setup/teardown do banco de teste
│   └── steps/
│       └── *_steps.py       # Implementação dos passos (given/when/then)
├── pytest.ini               # Configuração do Pytest
└── behave.ini               # Configuração do Behave (quando existir)
```

**Serviços com BDD (Behave):** Auth, Clients, Animals, Consultations, Vaccination.  
**Serviço sem BDD ainda:** Inventory (possui apenas Pytest unitário e integração).

---

### 8.3. TDD — Test Driven Development

#### O ciclo Red → Green → Refactor

O TDD orienta a **ordem de desenvolvimento**:

1. **Red** — Escrever um teste que descreve o comportamento esperado. O teste **falha** porque o código ainda não existe.
2. **Green** — Implementar o **mínimo** necessário para o teste passar.
3. **Refactor** — Melhorar o código (legibilidade, padrões) **sem quebrar** os testes.

**Exemplo real no projeto — `TokenService` (Auth):**

```python
# RED: teste escrito antes da implementação completa
def test_generate_token_contains_user_data(self, token_service, sample_user):
    token = token_service.generate_token(sample_user)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert payload["user_id"] == 1
    assert payload["role"] == "veterinarian"

# GREEN + REFACTOR: TokenService em src/domain/services/token_service.py
# passa a incluir user_id, email, role e expiração no payload JWT
```

Outros exemplos de TDD documentados: `PriceCalculationStrategy` (Consultations), `MedicalRecordFactory`, `VeterinaryServiceFacade`, `RegisterVaccineUseCase` (Vaccination).

#### Testes unitários — o que são e como funcionam

**Localização:** `services/*/tests/unit/`

Testam **uma unidade de código** sem subir servidor HTTP nem banco PostgreSQL real:

- **Entidades de domínio** — validações (`is_valid()`, regras de negócio)
- **Casos de uso** — com repositórios **mockados** (`MagicMock`) para isolar a lógica
- **Design Patterns** — Factory, Strategy, Facade, Observer em isolamento

**Exemplo — teste unitário de caso de uso com mock:**

```python
def test_register_vaccine_rejects_unknown_animal(self):
    repo = MagicMock()
    animal_service = MagicMock()
    animal_service.get_animal.return_value = None  # animal não existe

    use_case = RegisterVaccineUseCase(repo, animal_service=animal_service)

    with pytest.raises(VaccineRegistrationError, match="Animal 99 não encontrado"):
        use_case.execute(dto)

    repo.save.assert_not_called()  # garante que nada foi persistido
```

**Por que mocks no unitário?**  
Permitem testar regras de negócio **sem** depender de outro microsserviço, banco ou rede — alinhado ao Repository Pattern e à Clean Architecture.

#### Testes de integração — o que são e como funcionam

**Localização:** `services/*/tests/integration/`

Simulam requisições HTTP reais contra a API Django usando `APIClient` do DRF:

```
Cliente de teste  →  View  →  Use Case  →  Repository  →  Banco SQLite de teste
```

- Marcados com `@pytest.mark.django_db` para criar banco temporário
- Usam **JWT gerado localmente** via `make_jwt_token()` em `conftest.py`
- Validam status HTTP, corpo JSON, autenticação e permissões por role

**Exemplo — integração Animals API:**

```python
@pytest.mark.django_db
def test_create_animal_requires_auth(self, api_client):
    response = api_client.post("/api/animais/", {...}, format="json")
    assert response.status_code == 403  # sem token → proibido

def test_create_animal_success(self, api_client, veterinarian_headers):
    response = api_client.post("/api/animais/", {...}, format="json", **veterinarian_headers)
    assert response.status_code == 201
    assert response.data["name"] == "Rex"
```

**Fixtures de autenticação (`conftest.py`):**

| Fixture | Role simulada | Uso |
|---------|---------------|-----|
| `auth_headers` / `veterinarian_headers` | `veterinarian` | CRUD clínico |
| `tutor_auth_headers` / `tutor_headers` | `tutor` | Acesso restrito aos próprios animais |

O token é assinado com a mesma `SECRET_KEY` dos testes, reproduzindo o fluxo JWT de produção.

---

### 8.4. BDD — Behavior-Driven Development

#### O que é e por que usar

O BDD descreve comportamento em **linguagem natural estruturada (Gherkin)**, compreensível por negócio e desenvolvimento:

```gherkin
# language: pt
Funcionalidade: Agendamento de consulta
  Como tutor ou veterinário da clínica Vet Plus+
  Quero agendar consultas veterinárias
  Para que os animais recebam atendimento adequado

  Cenário: Agendar consulta com sucesso
    Dado que estou autenticado como veterinário
    E existe um veterinário cadastrado no sistema
    Quando eu agendo uma consulta com os dados:
      | animal_id | scheduled_at           | type    |
      | 1         | 2026-07-10T10:00:00Z   | regular |
    Então a consulta deve ser agendada com sucesso
    E o status da consulta deve ser "scheduled"
```

Cada linha **Dado / Quando / Então** é implementada em Python no arquivo `steps/*_steps.py`.

#### Como o Behave executa (fluxo)

```
.feature (Gherkin)
    ↓
environment.py → before_all: cria banco de teste + migrate
    ↓
before_scenario: APIClient limpo por cenário
    ↓
steps/*.py → executa given/when/then
    ↓
after_all: remove banco de teste
```

**`environment.py` (Consultations) — responsabilidades:**

| Hook | Função |
|------|--------|
| `before_all` | Sobe ambiente Django, roda `migrate` no banco de teste |
| `before_scenario` | Cria `APIClient` novo para cada cenário (isolamento) |
| `after_scenario` | Limpa contexto |
| `after_all` | Destrói banco de teste |

**Steps reutilizam utilitários de teste:**

```python
@given("que estou autenticado como veterinário")
def step_authenticated_veterinarian(context):
    token = make_jwt_token(user_id=1, role="veterinarian")
    context.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
```

Assim, BDD e testes de integração **compartilham** a mesma estratégia de autenticação (`tests/conftest.py`).

#### Cenários BDD por microsserviço

| Microsserviço | Arquivo `.feature` | Cenários principais |
|---------------|-------------------|---------------------|
| **Auth** | `authentication.feature` | Registro, login com JWT |
| **Clients** | `client_registration.feature` | Cadastro de tutor |
| **Animals** | `animal_registration.feature` | Cadastro e listagem de animal |
| **Consultations** | `appointment_scheduling.feature` | Agendar, sem auth, consultar detalhe |
| **Vaccination** | `vaccination_control.feature` | Registrar vacina, histórico, doses próximas |

---

### 8.5. Cobertura por microsserviço

| Microsserviço | Unitários (Pytest) | Integração (Pytest) | BDD (Behave) | Foco principal |
|---------------|-------------------|---------------------|--------------|----------------|
| **Auth** | `test_token_service.py` | `test_auth_api.py` | `authentication.feature` | JWT, login, registro |
| **Clients** | use cases + repository | `test_clients_api.py` | `client_registration.feature` | CRUD tutores |
| **Animals** | `test_animal_use_cases.py` | `test_animals_api.py` | `animal_registration.feature` | Pets, histórico, role tutor |
| **Consultations** | factory, strategy, facade, observer | `test_consultations_api.py` | `appointment_scheduling.feature` | Patterns + agendamento |
| **Vaccination** | `test_vaccine_use_cases.py` | `test_vaccination_api.py` | `vaccination_control.feature` | Vacinas, lembretes |
| **Inventory** | `test_medicine_use_cases.py` | `test_medicine_api.py` | — | Estoque, movimentações |

O microsserviço **Consultations** concentra a maior diversidade de testes unitários porque abriga **quatro Design Patterns** testados de forma isolada.

---

### 8.6. Como executar os testes

#### Pré-requisito comum

```bash
cd services/<microsserviço>
pip install -r requirements.txt
```

Defina o `PYTHONPATH` incluindo a pasta do serviço e `shared/`:

```bash
# Linux / Mac
export PYTHONPATH=$PWD:$PWD/../../shared

# Windows (PowerShell)
$env:PYTHONPATH="$PWD;$PWD\..\..\shared"
```

#### Pytest — unitários

```bash
cd services/consultations
pytest tests/unit/ -v
```

#### Pytest — integração

```bash
cd services/animals
pytest tests/integration/ -v
```

#### Pytest — suíte completa de um serviço

```bash
cd services/vaccination
pytest tests/ -v --tb=short
```

#### Behave — BDD

```bash
cd services/consultations
behave features/ -v
```

#### Executar todos os serviços (Linux / Mac)

```bash
for dir in services/*/; do
  echo "======== $(basename $dir) ========"
  (cd "$dir" && PYTHONPATH=$PWD:$PWD/../../shared pytest tests/ -q --tb=line)
done
```

#### Windows (PowerShell)

```powershell
Get-ChildItem services -Directory | ForEach-Object {
  Write-Host "======== $($_.Name) ========"
  Push-Location $_.FullName
  $env:PYTHONPATH = "$PWD;$PWD\..\..\shared"
  pytest tests/ -q --tb=line
  Pop-Location
}
```

---

### 8.7. Banco de dados nos testes

| Contexto | Banco usado |
|----------|-------------|
| Testes Pytest (`@pytest.mark.django_db`) | SQLite temporário criado pelo Django |
| Testes Behave (`environment.py`) | SQLite via `DiscoverRunner.setup_databases()` |
| Produção local (Docker) | PostgreSQL 16 por serviço |
| Produção (Render) | PostgreSQL compartilhado com schemas |

Os testes **não alteram** o banco de produção. Cada execução cria e destrói dados temporários.

---

### 8.8. O que os testes garantem na prática

| Risco | Como os testes mitigam |
|-------|------------------------|
| Regra de negócio incorreta | Unitários nos use cases e entidades |
| API retornando status errado | Integração com `APIClient` |
| Regressão ao refatorar patterns | Unitários de Factory, Strategy, Facade, Observer |
| Fluxo do usuário quebrado | BDD em Gherkin (português) |
| Acesso sem autenticação | Cenários BDD e integração com/sem JWT |
| Tutor acessando animal alheio | Integração Animals com `tutor_headers` |

---

### 8.9. Relação com a arquitetura do projeto

Os testes **reforçam** as decisões arquiteturais documentadas neste arquivo:

- **Clean Architecture** — unitários atacam Domain e Application sem Django HTTP
- **Repository Pattern** — mocks substituem repositórios nos use cases
- **Microsserviços** — cada serviço testa seu domínio; integração entre serviços é simulada via mocks ou HTTP em BDD quando necessário
- **SOLID (SRP)** — um arquivo de teste por responsabilidade (factory, strategy, facade…)

Para exemplos adicionais de ciclos TDD e trechos de steps BDD, consulte [TDD_BDD.md](TDD_BDD.md).

---

## 7. Resumo acadêmico

Em suma, a escolha de **microsserviços**, **Arquitetura Limpa**, **SOLID**, **Design Patterns**, **TDD/BDD** e **Docker** justifica-se pela busca de **baixo acoplamento** e **alta coesão**.

Juntos, esses elementos garantem que o backend do Vet Plus+ possa crescer em funcionalidades sem que uma alteração em uma ponta do sistema gere um efeito dominó de erros em outras partes — refletindo boas práticas da Engenharia de Software moderna e atendendo ao problema real de gestão operacional em clínicas veterinárias.

---

## Referências internas do projeto

| Documento | Conteúdo |
|-----------|----------|
| [README.md](../README.md) | Visão geral, execução e API |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitetura Limpa em detalhe |
| [SOLID.md](SOLID.md) | Princípios SOLID com exemplos |
| [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md) | Padrões de projeto |
| [CLEAN_CODE.md](CLEAN_CODE.md) | Boas práticas de código |
| [TDD_BDD.md](TDD_BDD.md) | Exemplos TDD (Red/Green/Refactor) e trechos BDD complementares |
| [RENDER.md](RENDER.md) | Deploy em produção |
