"""Casos de uso - Vacinação."""

from datetime import date


class VaccineNotFoundError(Exception):
    """Vacina não encontrada."""


class VaccineRegistrationError(Exception):
    """Erro ao registrar vacina."""


def _to_response_dto(vaccine) -> "VaccineResponseDTO":
    from src.application.dto.vaccine_dto import VaccineResponseDTO

    return VaccineResponseDTO(
        id=vaccine.id,
        animal_id=vaccine.animal_id,
        vaccine_name=vaccine.vaccine_name,
        application_date=vaccine.application_date,
        next_dose_date=vaccine.next_dose_date,
        veterinarian_id=vaccine.veterinarian_id,
        batch_number=vaccine.batch_number,
        notes=vaccine.notes,
        created_at=vaccine.created_at,
    )


class RegisterVaccineUseCase:
    """Registra uma nova vacina no sistema."""

    def __init__(self, vaccine_repository, reminder_repository=None):
        self._vaccine_repository = vaccine_repository
        self._reminder_repository = reminder_repository

    def execute(self, dto) -> "VaccineResponseDTO":
        from src.domain.entities.vaccine import Vaccine
        from src.domain.entities.vaccine_reminder import VaccineReminder

        vaccine = Vaccine(
            id=None,
            animal_id=dto.animal_id,
            vaccine_name=dto.vaccine_name,
            application_date=dto.application_date,
            next_dose_date=dto.next_dose_date,
            veterinarian_id=dto.veterinarian_id,
            batch_number=dto.batch_number,
            notes=dto.notes,
        )

        if not vaccine.is_valid():
            raise VaccineRegistrationError("Dados da vacina inválidos.")

        if vaccine.next_dose_date and vaccine.next_dose_date < vaccine.application_date:
            raise VaccineRegistrationError(
                "A data da próxima dose não pode ser anterior à data de aplicação."
            )

        saved = self._vaccine_repository.save(vaccine)

        if self._reminder_repository and saved.next_dose_date:
            reminder = VaccineReminder(
                id=None,
                vaccine_id=saved.id,
                animal_id=saved.animal_id,
                reminder_date=saved.next_dose_date,
                sent=False,
            )
            self._reminder_repository.save(reminder)

        return _to_response_dto(saved)


class ListVaccinesUseCase:
    """Lista todas as vacinas, com filtro opcional por animal."""

    def __init__(self, vaccine_repository):
        self._vaccine_repository = vaccine_repository

    def execute(self, animal_id: int | None = None) -> list["VaccineResponseDTO"]:
        vaccines = self._vaccine_repository.list_all(animal_id=animal_id)
        return [_to_response_dto(v) for v in vaccines]


class GetVaccineUseCase:
    """Obtém detalhes de uma vacina por ID."""

    def __init__(self, vaccine_repository):
        self._vaccine_repository = vaccine_repository

    def execute(self, vaccine_id: int) -> "VaccineResponseDTO":
        vaccine = self._vaccine_repository.find_by_id(vaccine_id)
        if vaccine is None:
            raise VaccineNotFoundError(f"Vacina {vaccine_id} não encontrada.")
        return _to_response_dto(vaccine)


class GetVaccineHistoryUseCase:
    """Obtém histórico de vacinação de um animal."""

    def __init__(self, vaccine_repository):
        self._vaccine_repository = vaccine_repository

    def execute(self, animal_id: int) -> list["VaccineResponseDTO"]:
        vaccines = self._vaccine_repository.find_by_animal_id(animal_id)
        return [_to_response_dto(v) for v in vaccines]


class CheckUpcomingVaccinesUseCase:
    """Verifica vacinas com próxima dose se aproximando e dispara lembretes."""

    def __init__(self, observer, vaccine_repository, within_days: int = 7):
        self._observer = observer
        self._vaccine_repository = vaccine_repository
        self._within_days = within_days

    def execute(self) -> list["UpcomingVaccineDTO"]:
        from src.application.dto.vaccine_dto import UpcomingVaccineDTO

        self._observer.check_upcoming()

        today = date.today()
        upcoming = self._vaccine_repository.find_upcoming(self._within_days)
        return [
            UpcomingVaccineDTO(
                id=v.id,
                animal_id=v.animal_id,
                vaccine_name=v.vaccine_name,
                next_dose_date=v.next_dose_date,
                days_until_due=(v.next_dose_date - today).days,
            )
            for v in upcoming
            if v.next_dose_date is not None
        ]
