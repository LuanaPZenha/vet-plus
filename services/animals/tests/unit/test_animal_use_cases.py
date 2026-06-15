"""Testes unitários TDD - Entidades e Casos de Uso."""

from datetime import date
from unittest.mock import MagicMock

import pytest

from src.application.dto.animal_dto import AddMedicalHistoryDTO, CreateAnimalDTO
from src.application.use_cases.animal_use_cases import (
    AddMedicalHistoryUseCase,
    AnimalCreationError,
    AnimalNotFoundError,
    CreateAnimalUseCase,
    GetAnimalUseCase,
    GetMedicalHistoryUseCase,
    ListAnimalsUseCase,
    MedicalHistoryError,
)
from src.domain.entities.animal import Animal
from src.domain.entities.medical_history import MedicalHistoryEntry, MedicalRecordType


class TestAnimalEntity:
    """TDD: Validação da entidade Animal."""

    def test_valid_animal(self):
        animal = Animal(
            id=1,
            name="Rex",
            species="Cão",
            breed="Labrador",
            birth_date=date(2020, 5, 10),
            weight=25.5,
            client_id=1,
        )
        assert animal.is_valid() is True

    def test_invalid_animal_empty_name(self):
        animal = Animal(
            id=None,
            name="  ",
            species="Cão",
            breed="Labrador",
            birth_date=None,
            weight=None,
            client_id=1,
        )
        assert animal.is_valid() is False

    def test_invalid_animal_zero_client_id(self):
        animal = Animal(
            id=None,
            name="Rex",
            species="Cão",
            breed="Labrador",
            birth_date=None,
            weight=None,
            client_id=0,
        )
        assert animal.is_valid() is False


class TestMedicalHistoryEntity:
    """TDD: Validação da entidade MedicalHistoryEntry."""

    def test_valid_entry(self):
        entry = MedicalHistoryEntry(
            id=1,
            animal_id=1,
            description="Consulta de rotina",
            record_type=MedicalRecordType.CONSULTATION,
        )
        assert entry.is_valid() is True

    def test_invalid_entry_empty_description(self):
        entry = MedicalHistoryEntry(
            id=None,
            animal_id=1,
            description="   ",
            record_type=MedicalRecordType.NOTE,
        )
        assert entry.is_valid() is False


class TestCreateAnimalUseCase:
    """TDD: Caso de uso CreateAnimal."""

    def test_create_animal_success(self):
        repo = MagicMock()
        saved = Animal(
            id=1,
            name="Mimi",
            species="Gato",
            breed="Siamês",
            birth_date=date(2019, 3, 15),
            weight=4.2,
            client_id=5,
        )
        repo.save.return_value = saved

        use_case = CreateAnimalUseCase(repo)
        dto = CreateAnimalDTO(
            name="Mimi",
            species="Gato",
            breed="Siamês",
            birth_date=date(2019, 3, 15),
            weight=4.2,
            client_id=5,
        )
        result = use_case.execute(dto)

        assert result.id == 1
        assert result.name == "Mimi"
        assert result.client_id == 5
        repo.save.assert_called_once()

    def test_create_animal_invalid_data(self):
        repo = MagicMock()
        use_case = CreateAnimalUseCase(repo)
        dto = CreateAnimalDTO(
            name="",
            species="Gato",
            breed="Siamês",
            birth_date=None,
            weight=None,
            client_id=1,
        )

        with pytest.raises(AnimalCreationError):
            use_case.execute(dto)

        repo.save.assert_not_called()


class TestListAnimalsUseCase:
    """TDD: Caso de uso ListAnimals."""

    def test_list_all_animals(self):
        repo = MagicMock()
        repo.list_all.return_value = [
            Animal(
                id=1,
                name="Rex",
                species="Cão",
                breed="Labrador",
                birth_date=None,
                weight=20.0,
                client_id=1,
            ),
        ]

        use_case = ListAnimalsUseCase(repo)
        results = use_case.execute()

        assert len(results) == 1
        assert results[0].name == "Rex"
        repo.list_all.assert_called_once_with(client_id=None)

    def test_list_animals_by_client(self):
        repo = MagicMock()
        repo.list_all.return_value = []

        use_case = ListAnimalsUseCase(repo)
        use_case.execute(client_id=10)

        repo.list_all.assert_called_once_with(client_id=10)


class TestGetAnimalUseCase:
    """TDD: Caso de uso GetAnimal."""

    def test_get_animal_success(self):
        repo = MagicMock()
        repo.find_by_id.return_value = Animal(
            id=1,
            name="Rex",
            species="Cão",
            breed="Labrador",
            birth_date=None,
            weight=20.0,
            client_id=1,
        )

        use_case = GetAnimalUseCase(repo)
        result = use_case.execute(1)

        assert result.id == 1
        assert result.name == "Rex"

    def test_get_animal_not_found(self):
        repo = MagicMock()
        repo.find_by_id.return_value = None

        use_case = GetAnimalUseCase(repo)

        with pytest.raises(AnimalNotFoundError):
            use_case.execute(999)


class TestMedicalHistoryUseCases:
    """TDD: Casos de uso de histórico médico."""

    def test_add_medical_history_success(self):
        animal_repo = MagicMock()
        history_repo = MagicMock()
        animal_repo.exists.return_value = True
        history_repo.save.return_value = MedicalHistoryEntry(
            id=1,
            animal_id=1,
            description="Vacina antirrábica",
            record_type=MedicalRecordType.VACCINATION,
        )

        use_case = AddMedicalHistoryUseCase(animal_repo, history_repo)
        dto = AddMedicalHistoryDTO(
            animal_id=1,
            description="Vacina antirrábica",
            record_type="vaccination",
        )
        result = use_case.execute(dto)

        assert result.record_type == "vaccination"
        history_repo.save.assert_called_once()

    def test_add_medical_history_animal_not_found(self):
        animal_repo = MagicMock()
        history_repo = MagicMock()
        animal_repo.exists.return_value = False

        use_case = AddMedicalHistoryUseCase(animal_repo, history_repo)
        dto = AddMedicalHistoryDTO(
            animal_id=999,
            description="Teste",
            record_type="note",
        )

        with pytest.raises(AnimalNotFoundError):
            use_case.execute(dto)

    def test_add_medical_history_invalid_type(self):
        animal_repo = MagicMock()
        history_repo = MagicMock()
        animal_repo.exists.return_value = True

        use_case = AddMedicalHistoryUseCase(animal_repo, history_repo)
        dto = AddMedicalHistoryDTO(
            animal_id=1,
            description="Teste",
            record_type="invalid_type",
        )

        with pytest.raises(MedicalHistoryError):
            use_case.execute(dto)

    def test_get_medical_history_success(self):
        animal_repo = MagicMock()
        history_repo = MagicMock()
        animal_repo.exists.return_value = True
        history_repo.find_by_animal_id.return_value = [
            MedicalHistoryEntry(
                id=1,
                animal_id=1,
                description="Consulta",
                record_type=MedicalRecordType.CONSULTATION,
            ),
        ]

        use_case = GetMedicalHistoryUseCase(animal_repo, history_repo)
        results = use_case.execute(1)

        assert len(results) == 1
        assert results[0].description == "Consulta"

    def test_get_medical_history_animal_not_found(self):
        animal_repo = MagicMock()
        history_repo = MagicMock()
        animal_repo.exists.return_value = False

        use_case = GetMedicalHistoryUseCase(animal_repo, history_repo)

        with pytest.raises(AnimalNotFoundError):
            use_case.execute(999)
