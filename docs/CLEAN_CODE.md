# Clean Code — Vet+ Clinic

Este documento explica as práticas de Clean Code aplicadas no projeto, com exemplos concretos de onde cada prática foi implementada.

---

## 1. Nomes Significativos

Nomes de variáveis, classes e métodos devem revelar intenção, sem necessidade de comentários explicativos.

| Ruim | Bom (projeto) | Localização |
|------|---------------|-------------|
| `d` | `diagnosis` | `VeterinaryServiceFacade.complete_consultation()` |
| `repo` | `consultation_repository` | Use cases |
| `calc()` | `calculate_price()` | `PriceCalculationContext` |
| `UserModel` genérico | `ConsultationModel`, `VaccineModel` | Infrastructure |

**Exemplo:**

```python
# Nome revela intenção
class ScheduleConsultationUseCase:
    def execute(self, dto: CreateConsultationDTO) -> Consultation:
        consultation = Consultation(
            animal_id=dto.animal_id,
            veterinarian_id=dto.veterinarian_id,
            scheduled_at=dto.scheduled_at,
            status=ConsultationStatus.SCHEDULED,
            type=ConsultationType(dto.consultation_type),
        )
```

---

## 2. Métodos Pequenos

Cada método faz **uma coisa** e a faz bem. Métodos longos foram decompostos.

**Exemplo — Facade decompõe fluxo complexo:**

```python
class VeterinaryServiceFacade:
    def complete_consultation(self, consultation, diagnosis, prescription_notes=""):
        animal = self._fetch_animal(consultation.animal_id)          # ~5 linhas
        price = self._calculate_price(consultation)                  # ~3 linhas
        record = self._create_medical_record(consultation, diagnosis) # ~8 linhas
        self._update_medical_history(animal.id, record)              # ~4 linhas
        prescription = self._generate_prescription(animal, diagnosis, prescription_notes)
        return self._finalize_consultation(consultation, prescription, animal, record)
```

Cada método privado (`_fetch_animal`, `_calculate_price`, etc.) tem 3–8 linhas.

---

## 3. Classes Coesas

Cada classe agrupa responsabilidades relacionadas. Classes com responsabilidades misturadas foram separadas.

| Classe | Responsabilidade única |
|--------|----------------------|
| `TokenService` | Apenas JWT |
| `RegisterUserUseCase` | Apenas registro |
| `RegularConsultationStrategy` | Apenas preço regular |
| `DjangoUserRepository` | Apenas persistência de usuários |
| `ConsultationScheduledObserver` | Apenas registrar notificação de agendamento |

---

## 4. Evitar Duplicação (DRY)

Lógica repetida foi extraída para funções/métodos reutilizáveis.

**Exemplo — Conversão ORM → Entidade centralizada:**

```python
class DjangoConsultationRepository(IConsultationRepository):
    def _to_entity(self, model: ConsultationModel) -> Consultation:
        """Conversão reutilizada por save, find_by_id, find_all, update."""
        return Consultation(
            id=model.id,
            animal_id=model.animal_id,
            veterinarian_id=model.veterinarian_id,
            scheduled_at=model.scheduled_at,
            status=ConsultationStatus(model.status),
            type=ConsultationType(model.type),
            price=model.price,
            notes=model.notes,
        )
```

**Exemplo — Settings compartilhadas:**

O módulo `shared/django_settings.py` evita duplicar configuração Django em 5 serviços.

---

## 5. Comentários Apenas Quando Necessários

O código é autoexplicativo. Comentários existem apenas em:
- Design Patterns (explicação acadêmica do padrão)
- Docstrings de interfaces públicas
- Regras de negócio não óbvias

**Comentários úteis (Design Patterns):**

```python
"""
Factory Method Pattern - Registros médicos.
O padrão Factory Method define uma interface para criar objetos...
"""
```

**Sem comentários desnecessários:**

```python
# Ruim (óbvio):
# Incrementa o contador
counter += 1

# Bom (código autoexplicativo):
consultation.status = ConsultationStatus.COMPLETED
```

---

## 6. Separação de Responsabilidades

A Clean Architecture garante separação em camadas:

```
View (HTTP)  →  Use Case (orquestração)  →  Repository (persistência)  →  Entity (regras)
```

**Nenhuma view acessa ORM diretamente.** Todas delegam a use cases:

```python
class ConsultationListCreateView(APIView):
    def post(self, request):
        serializer = CreateConsultationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = ScheduleConsultationUseCase(
            DjangoConsultationRepository(),
            self._get_notification_subject(),
        )
        result = use_case.execute(CreateConsultationDTO(**serializer.validated_data))
        return Response(ConsultationSerializer(result).data, status=201)
```

---

## 7. Tipagem Adequada

Python 3.13+ type hints em todas as interfaces e métodos públicos:

```python
from abc import ABC, abstractmethod

class IConsultationRepository(ABC):
    @abstractmethod
    def save(self, consultation: Consultation) -> Consultation: ...

    @abstractmethod
    def find_by_id(self, consultation_id: int) -> Consultation | None: ...

    @abstractmethod
    def find_all(self) -> list[Consultation]: ...
```

**DTOs tipados:**

```python
@dataclass
class CreateConsultationDTO:
    animal_id: int
    veterinarian_id: int
    scheduled_at: datetime
    consultation_type: str
    notes: str = ""
```

**Enums para valores fixos:**

```python
class ConsultationStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
```

---

## 8. Tratamento de Erros Explícito

Exceções de domínio específicas em vez de genéricas:

```python
class AuthenticationError(Exception):
    """Erro de autenticação."""

class AnimalNotFoundError(Exception):
    """Animal não encontrado no microsserviço de animais."""

class ConsultationCompletionError(Exception):
    """Erro ao concluir consulta via Facade."""
```

**Uso nas views:**

```python
try:
    result = use_case.execute(dto)
except AuthenticationError as exc:
    return Response({"error": str(exc)}, status=401)
except RegistrationError as exc:
    return Response({"error": str(exc)}, status=400)
```

---

## Resumo

| Prática | Onde aplicada |
|---------|---------------|
| Nomes significativos | Todas as camadas |
| Métodos pequenos | Facade, Use Cases, Repositories |
| Classes coesas | Cada use case, strategy, observer |
| Evitar duplicação | `_to_entity()`, `shared/django_settings.py` |
| Comentários mínimos | Apenas patterns e docstrings |
| Separação de responsabilidades | Clean Architecture (4 camadas) |
| Tipagem | Interfaces, DTOs, Enums |
| Erros explícitos | Exceções de domomínio por contexto |
