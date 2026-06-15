"""Casos de uso - Animais."""


class AnimalNotFoundError(Exception):
    """Animal não encontrado."""


class AnimalCreationError(Exception):
    """Erro ao criar animal."""


class MedicalHistoryError(Exception):
    """Erro ao registrar histórico médico."""


class CreateAnimalUseCase:
    """Registra um novo animal no sistema."""

    def __init__(self, animal_repository):
        self._animal_repository = animal_repository

    def execute(self, dto) -> "AnimalResponseDTO":
        from src.application.dto.animal_dto import AnimalResponseDTO
        from src.domain.entities.animal import Animal

        animal = Animal(
            id=None,
            name=dto.name,
            species=dto.species,
            breed=dto.breed,
            birth_date=dto.birth_date,
            weight=dto.weight,
            client_id=dto.client_id,
        )

        if not animal.is_valid():
            raise AnimalCreationError("Dados do animal inválidos.")

        saved = self._animal_repository.save(animal)
        return AnimalResponseDTO(
            id=saved.id,
            name=saved.name,
            species=saved.species,
            breed=saved.breed,
            birth_date=saved.birth_date,
            weight=saved.weight,
            client_id=saved.client_id,
            created_at=saved.created_at,
        )


class ListAnimalsUseCase:
    """Lista animais, com filtro opcional por cliente."""

    def __init__(self, animal_repository):
        self._animal_repository = animal_repository

    def execute(self, client_id: int | None = None) -> list["AnimalResponseDTO"]:
        from src.application.dto.animal_dto import AnimalResponseDTO

        animals = self._animal_repository.list_all(client_id=client_id)
        return [
            AnimalResponseDTO(
                id=a.id,
                name=a.name,
                species=a.species,
                breed=a.breed,
                birth_date=a.birth_date,
                weight=a.weight,
                client_id=a.client_id,
                created_at=a.created_at,
            )
            for a in animals
        ]


class GetAnimalUseCase:
    """Obtém detalhes de um animal por ID."""

    def __init__(self, animal_repository):
        self._animal_repository = animal_repository

    def execute(self, animal_id: int) -> "AnimalResponseDTO":
        from src.application.dto.animal_dto import AnimalResponseDTO

        animal = self._animal_repository.find_by_id(animal_id)
        if animal is None:
            raise AnimalNotFoundError(f"Animal {animal_id} não encontrado.")

        return AnimalResponseDTO(
            id=animal.id,
            name=animal.name,
            species=animal.species,
            breed=animal.breed,
            birth_date=animal.birth_date,
            weight=animal.weight,
            client_id=animal.client_id,
            created_at=animal.created_at,
        )


class AddMedicalHistoryUseCase:
    """Adiciona entrada ao histórico médico de um animal."""

    def __init__(self, animal_repository, medical_history_repository):
        self._animal_repository = animal_repository
        self._medical_history_repository = medical_history_repository

    def execute(self, dto) -> "MedicalHistoryResponseDTO":
        from src.application.dto.animal_dto import MedicalHistoryResponseDTO
        from src.domain.entities.medical_history import MedicalHistoryEntry, MedicalRecordType

        if not self._animal_repository.exists(dto.animal_id):
            raise AnimalNotFoundError(f"Animal {dto.animal_id} não encontrado.")

        try:
            record_type = MedicalRecordType(dto.record_type)
        except ValueError as exc:
            raise MedicalHistoryError(f"Tipo de registro inválido: {dto.record_type}") from exc

        entry = MedicalHistoryEntry(
            id=None,
            animal_id=dto.animal_id,
            description=dto.description,
            record_type=record_type,
        )

        if not entry.is_valid():
            raise MedicalHistoryError("Dados do histórico médico inválidos.")

        saved = self._medical_history_repository.save(entry)
        return MedicalHistoryResponseDTO(
            id=saved.id,
            animal_id=saved.animal_id,
            description=saved.description,
            record_type=saved.record_type.value,
            created_at=saved.created_at,
        )


class GetMedicalHistoryUseCase:
    """Lista histórico médico de um animal."""

    def __init__(self, animal_repository, medical_history_repository):
        self._animal_repository = animal_repository
        self._medical_history_repository = medical_history_repository

    def execute(self, animal_id: int) -> list["MedicalHistoryResponseDTO"]:
        from src.application.dto.animal_dto import MedicalHistoryResponseDTO

        if not self._animal_repository.exists(animal_id):
            raise AnimalNotFoundError(f"Animal {animal_id} não encontrado.")

        entries = self._medical_history_repository.find_by_animal_id(animal_id)
        return [
            MedicalHistoryResponseDTO(
                id=e.id,
                animal_id=e.animal_id,
                description=e.description,
                record_type=e.record_type.value,
                created_at=e.created_at,
            )
            for e in entries
        ]
