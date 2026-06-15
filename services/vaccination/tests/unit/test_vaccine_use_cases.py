"""Testes unitários TDD - Entidades, Casos de Uso e Observer."""

from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pytest

from src.application.dto.vaccine_dto import RegisterVaccineDTO
from src.application.use_cases.vaccine_use_cases import (
    CheckUpcomingVaccinesUseCase,
    GetVaccineHistoryUseCase,
    GetVaccineUseCase,
    ListVaccinesUseCase,
    RegisterVaccineUseCase,
    VaccineNotFoundError,
    VaccineRegistrationError,
)
from src.domain.entities.vaccine import Vaccine
from src.domain.entities.vaccine_reminder import VaccineReminder
from src.domain.services.vaccine_reminder_observer import VaccineReminderObserver


class TestVaccineEntity:
    """TDD: Validação da entidade Vaccine."""

    def test_valid_vaccine(self):
        vaccine = Vaccine(
            id=1,
            animal_id=1,
            vaccine_name="V10",
            application_date=date(2026, 1, 10),
            next_dose_date=date(2026, 7, 10),
            veterinarian_id=1,
            batch_number="LOTE123",
            notes="Primeira dose",
        )
        assert vaccine.is_valid() is True

    def test_invalid_vaccine_empty_name(self):
        vaccine = Vaccine(
            id=None,
            animal_id=1,
            vaccine_name="  ",
            application_date=date(2026, 1, 10),
            next_dose_date=None,
            veterinarian_id=1,
            batch_number=None,
            notes=None,
        )
        assert vaccine.is_valid() is False

    def test_is_upcoming_within_range(self):
        today = date(2026, 6, 14)
        vaccine = Vaccine(
            id=1,
            animal_id=1,
            vaccine_name="Antirrábica",
            application_date=date(2025, 6, 14),
            next_dose_date=date(2026, 6, 20),
            veterinarian_id=1,
            batch_number=None,
            notes=None,
        )
        assert vaccine.is_upcoming(within_days=7, reference_date=today) is True

    def test_is_not_upcoming_when_no_next_dose(self):
        vaccine = Vaccine(
            id=1,
            animal_id=1,
            vaccine_name="V10",
            application_date=date(2026, 1, 10),
            next_dose_date=None,
            veterinarian_id=1,
            batch_number=None,
            notes=None,
        )
        assert vaccine.is_upcoming() is False


class TestVaccineReminderEntity:
    """TDD: Validação da entidade VaccineReminder."""

    def test_valid_reminder(self):
        reminder = VaccineReminder(
            id=1,
            vaccine_id=1,
            animal_id=1,
            reminder_date=date(2026, 6, 20),
            sent=False,
        )
        assert reminder.is_valid() is True

    def test_mark_sent(self):
        reminder = VaccineReminder(
            id=1,
            vaccine_id=1,
            animal_id=1,
            reminder_date=date(2026, 6, 20),
            sent=False,
        )
        reminder.mark_sent()
        assert reminder.sent is True


class TestRegisterVaccineUseCase:
    """TDD: Caso de uso RegisterVaccine."""

    def test_register_vaccine_success(self):
        repo = MagicMock()
        reminder_repo = MagicMock()
        saved = Vaccine(
            id=1,
            animal_id=1,
            vaccine_name="V10",
            application_date=date(2026, 1, 10),
            next_dose_date=date(2026, 7, 10),
            veterinarian_id=1,
            batch_number="LOTE123",
            notes="Primeira dose",
        )
        repo.save.return_value = saved
        reminder_repo.save.return_value = VaccineReminder(
            id=1,
            vaccine_id=1,
            animal_id=1,
            reminder_date=date(2026, 7, 10),
            sent=False,
        )

        use_case = RegisterVaccineUseCase(repo, reminder_repo)
        dto = RegisterVaccineDTO(
            animal_id=1,
            vaccine_name="V10",
            application_date=date(2026, 1, 10),
            next_dose_date=date(2026, 7, 10),
            veterinarian_id=1,
            batch_number="LOTE123",
            notes="Primeira dose",
        )
        result = use_case.execute(dto)

        assert result.id == 1
        assert result.vaccine_name == "V10"
        repo.save.assert_called_once()
        reminder_repo.save.assert_called_once()

    def test_register_vaccine_invalid_data(self):
        repo = MagicMock()
        use_case = RegisterVaccineUseCase(repo)
        dto = RegisterVaccineDTO(
            animal_id=1,
            vaccine_name="",
            application_date=date(2026, 1, 10),
            next_dose_date=None,
            veterinarian_id=1,
            batch_number=None,
            notes=None,
        )

        with pytest.raises(VaccineRegistrationError):
            use_case.execute(dto)

        repo.save.assert_not_called()

    def test_register_vaccine_invalid_next_dose_date(self):
        repo = MagicMock()
        use_case = RegisterVaccineUseCase(repo)
        dto = RegisterVaccineDTO(
            animal_id=1,
            vaccine_name="V10",
            application_date=date(2026, 6, 10),
            next_dose_date=date(2026, 1, 10),
            veterinarian_id=1,
            batch_number=None,
            notes=None,
        )

        with pytest.raises(VaccineRegistrationError):
            use_case.execute(dto)


class TestListVaccinesUseCase:
    """TDD: Caso de uso ListVaccines."""

    def test_list_all_vaccines(self):
        repo = MagicMock()
        repo.list_all.return_value = [
            Vaccine(
                id=1,
                animal_id=1,
                vaccine_name="V10",
                application_date=date(2026, 1, 10),
                next_dose_date=date(2026, 7, 10),
                veterinarian_id=1,
                batch_number=None,
                notes=None,
            ),
        ]

        use_case = ListVaccinesUseCase(repo)
        results = use_case.execute()

        assert len(results) == 1
        assert results[0].vaccine_name == "V10"


class TestGetVaccineUseCase:
    """TDD: Caso de uso GetVaccine."""

    def test_get_vaccine_success(self):
        repo = MagicMock()
        repo.find_by_id.return_value = Vaccine(
            id=1,
            animal_id=1,
            vaccine_name="V10",
            application_date=date(2026, 1, 10),
            next_dose_date=None,
            veterinarian_id=1,
            batch_number=None,
            notes=None,
        )

        use_case = GetVaccineUseCase(repo)
        result = use_case.execute(1)

        assert result.id == 1

    def test_get_vaccine_not_found(self):
        repo = MagicMock()
        repo.find_by_id.return_value = None

        use_case = GetVaccineUseCase(repo)

        with pytest.raises(VaccineNotFoundError):
            use_case.execute(999)


class TestGetVaccineHistoryUseCase:
    """TDD: Caso de uso GetVaccineHistory."""

    def test_get_history_by_animal(self):
        repo = MagicMock()
        repo.find_by_animal_id.return_value = [
            Vaccine(
                id=1,
                animal_id=5,
                vaccine_name="V10",
                application_date=date(2026, 1, 10),
                next_dose_date=date(2026, 7, 10),
                veterinarian_id=1,
                batch_number=None,
                notes=None,
            ),
            Vaccine(
                id=2,
                animal_id=5,
                vaccine_name="Antirrábica",
                application_date=date(2025, 6, 10),
                next_dose_date=date(2026, 6, 10),
                veterinarian_id=1,
                batch_number=None,
                notes=None,
            ),
        ]

        use_case = GetVaccineHistoryUseCase(repo)
        results = use_case.execute(5)

        assert len(results) == 2
        repo.find_by_animal_id.assert_called_once_with(5)


class TestVaccineReminderObserver:
    """TDD: Observer Pattern para lembretes de vacina."""

    def test_observer_sends_notification_for_upcoming_vaccine(self):
        vaccine_repo = MagicMock()
        reminder_repo = MagicMock()
        notification_service = MagicMock()

        upcoming_vaccine = Vaccine(
            id=1,
            animal_id=1,
            vaccine_name="V10",
            application_date=date(2026, 1, 10),
            next_dose_date=date(2026, 6, 20),
            veterinarian_id=1,
            batch_number=None,
            notes=None,
        )
        vaccine_repo.find_upcoming.return_value = [upcoming_vaccine]
        reminder_repo.find_by_vaccine_id.return_value = None
        saved_reminder = VaccineReminder(
            id=1,
            vaccine_id=1,
            animal_id=1,
            reminder_date=date(2026, 6, 20),
            sent=False,
        )
        reminder_repo.save.return_value = saved_reminder
        reminder_repo.find_pending.return_value = []

        observer = VaccineReminderObserver(
            vaccine_repo,
            reminder_repo,
            notification_service,
            within_days=7,
        )
        observer.check_upcoming()

        notification_service.notify_vaccine_due.assert_called_once_with(
            upcoming_vaccine,
            saved_reminder,
        )
        reminder_repo.mark_sent.assert_called_once_with(1)

    def test_observer_skips_already_sent_reminder(self):
        vaccine_repo = MagicMock()
        reminder_repo = MagicMock()
        notification_service = MagicMock()

        upcoming_vaccine = Vaccine(
            id=1,
            animal_id=1,
            vaccine_name="V10",
            application_date=date(2026, 1, 10),
            next_dose_date=date(2026, 6, 20),
            veterinarian_id=1,
            batch_number=None,
            notes=None,
        )
        vaccine_repo.find_upcoming.return_value = [upcoming_vaccine]
        reminder_repo.find_by_vaccine_id.return_value = VaccineReminder(
            id=1,
            vaccine_id=1,
            animal_id=1,
            reminder_date=date(2026, 6, 20),
            sent=True,
        )
        reminder_repo.find_pending.return_value = []

        observer = VaccineReminderObserver(
            vaccine_repo,
            reminder_repo,
            notification_service,
        )
        observer.check_upcoming()

        notification_service.notify_vaccine_due.assert_not_called()


class TestCheckUpcomingVaccinesUseCase:
    """TDD: Caso de uso CheckUpcomingVaccines."""

    @patch("src.application.use_cases.vaccine_use_cases.date")
    def test_check_upcoming_vaccines(self, mock_date):
        mock_date.today.return_value = date(2026, 6, 14)

        observer = MagicMock()
        vaccine_repo = MagicMock()
        vaccine_repo.find_upcoming.return_value = [
            Vaccine(
                id=1,
                animal_id=1,
                vaccine_name="V10",
                application_date=date(2026, 1, 10),
                next_dose_date=date(2026, 6, 20),
                veterinarian_id=1,
                batch_number=None,
                notes=None,
            ),
        ]

        use_case = CheckUpcomingVaccinesUseCase(observer, vaccine_repo, within_days=7)
        results = use_case.execute()

        observer.check_upcoming.assert_called_once()
        assert len(results) == 1
        assert results[0].days_until_due == 6
        assert results[0].vaccine_name == "V10"
