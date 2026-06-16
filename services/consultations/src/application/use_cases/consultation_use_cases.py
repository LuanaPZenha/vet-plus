"""Casos de uso - Consultas."""

from src.domain.entities.consultation import (
    Consultation,
    ConsultationStatus,
    ConsultationType,
)
from src.domain.patterns.facade.veterinary_service_facade import (
    AnimalNotFoundError,
    ConsultationCompletionError,
    VeterinaryServiceFacade,
)
from src.domain.patterns.observer.notification_subject import (
    AppointmentReminderObserver,
    ConsultationScheduledObserver,
    EmailNotificationObserver,
    NotificationSubject,
)
class ConsultationNotFoundError(Exception):
    """Consulta não encontrada."""


class ConsultationSchedulingError(Exception):
    """Erro ao agendar consulta."""


class VeterinarianNotFoundError(Exception):
    """Veterinário não encontrado."""


class VeterinarianCreationError(Exception):
    """Erro ao cadastrar veterinário."""


class ScheduleConsultationUseCase:
    """
    Agenda uma nova consulta e notifica observers (Observer Pattern).

    Após persistir a consulta, o NotificationSubject dispara notificações
    para todos os observers registrados (agendamento, e-mail, lembrete).
    """

    def __init__(
        self,
        consultation_repository,
        veterinarian_repository,
        animal_service=None,
        notification_subject: NotificationSubject | None = None,
    ):
        self._consultation_repository = consultation_repository
        self._veterinarian_repository = veterinarian_repository
        self._animal_service = animal_service
        self._notification_subject = notification_subject or _default_notification_subject()

    def execute(self, dto) -> "ConsultationResponseDTO":
        from src.application.dto.consultation_dto import ConsultationResponseDTO

        if not self._veterinarian_repository.exists(dto.veterinarian_id):
            raise ConsultationSchedulingError(
                f"Veterinário {dto.veterinarian_id} não encontrado."
            )

        if self._animal_service is not None:
            animal = self._animal_service.get_animal(dto.animal_id)
            if animal is None:
                raise ConsultationSchedulingError(
                    f"Animal {dto.animal_id} não encontrado. Cadastre o animal antes de agendar."
                )

        try:
            consultation_type = ConsultationType(dto.type)
        except ValueError as exc:
            raise ConsultationSchedulingError(f"Tipo de consulta inválido: {dto.type}") from exc

        consultation = Consultation(
            id=None,
            animal_id=dto.animal_id,
            veterinarian_id=dto.veterinarian_id,
            scheduled_at=dto.scheduled_at,
            status=ConsultationStatus.SCHEDULED,
            type=consultation_type,
            notes=dto.notes,
        )

        if not consultation.is_valid():
            raise ConsultationSchedulingError("Dados da consulta inválidos.")

        saved = self._consultation_repository.save(consultation)

        # Observer Pattern: notifica todos os observers registrados
        self._notification_subject.notify_consultation_scheduled(saved)

        return ConsultationResponseDTO(
            id=saved.id,
            animal_id=saved.animal_id,
            veterinarian_id=saved.veterinarian_id,
            scheduled_at=saved.scheduled_at,
            status=saved.status.value,
            type=saved.type.value,
            price=saved.price,
            notes=saved.notes,
            diagnosis=saved.diagnosis,
            prescription=saved.prescription,
            created_at=saved.created_at,
        )


class ListConsultationsUseCase:
    """Lista consultas com filtros opcionais."""

    def __init__(self, consultation_repository):
        self._consultation_repository = consultation_repository

    def execute(
        self,
        animal_id: int | None = None,
        veterinarian_id: int | None = None,
        status: str | None = None,
    ) -> list["ConsultationResponseDTO"]:
        from src.application.dto.consultation_dto import ConsultationResponseDTO

        status_enum = ConsultationStatus(status) if status else None
        consultations = self._consultation_repository.list_all(
            animal_id=animal_id,
            veterinarian_id=veterinarian_id,
            status=status_enum,
        )
        return [
            ConsultationResponseDTO(
                id=c.id,
                animal_id=c.animal_id,
                veterinarian_id=c.veterinarian_id,
                scheduled_at=c.scheduled_at,
                status=c.status.value,
                type=c.type.value,
                price=c.price,
                notes=c.notes,
                diagnosis=c.diagnosis,
                prescription=c.prescription,
                created_at=c.created_at,
            )
            for c in consultations
        ]


class GetConsultationUseCase:
    """Obtém detalhes de uma consulta."""

    def __init__(self, consultation_repository):
        self._consultation_repository = consultation_repository

    def execute(self, consultation_id: int) -> "ConsultationResponseDTO":
        from src.application.dto.consultation_dto import ConsultationResponseDTO

        consultation = self._consultation_repository.find_by_id(consultation_id)
        if consultation is None:
            raise ConsultationNotFoundError(f"Consulta {consultation_id} não encontrada.")

        return ConsultationResponseDTO(
            id=consultation.id,
            animal_id=consultation.animal_id,
            veterinarian_id=consultation.veterinarian_id,
            scheduled_at=consultation.scheduled_at,
            status=consultation.status.value,
            type=consultation.type.value,
            price=consultation.price,
            notes=consultation.notes,
            diagnosis=consultation.diagnosis,
            prescription=consultation.prescription,
            created_at=consultation.created_at,
        )


class CompleteConsultationUseCase:
    """
    Conclui uma consulta usando o VeterinaryServiceFacade (Facade Pattern).

    O cálculo de preço é delegado ao Strategy Pattern dentro do Facade.
    """

    def __init__(self, consultation_repository, facade: VeterinaryServiceFacade):
        self._consultation_repository = consultation_repository
        self._facade = facade

    def execute(self, dto) -> "ConsultationResponseDTO":
        from src.application.dto.consultation_dto import ConsultationResponseDTO

        consultation = self._consultation_repository.find_by_id(dto.consultation_id)
        if consultation is None:
            raise ConsultationNotFoundError(f"Consulta {dto.consultation_id} não encontrada.")

        try:
            result = self._facade.complete_consultation(
                consultation=consultation,
                diagnosis=dto.diagnosis,
                prescription_notes=dto.prescription_notes,
                procedure=dto.procedure,
            )
        except AnimalNotFoundError as exc:
            raise ConsultationSchedulingError(str(exc)) from exc
        except ConsultationCompletionError as exc:
            raise ConsultationSchedulingError(str(exc)) from exc

        completed = result.consultation
        return ConsultationResponseDTO(
            id=completed.id,
            animal_id=completed.animal_id,
            veterinarian_id=completed.veterinarian_id,
            scheduled_at=completed.scheduled_at,
            status=completed.status.value,
            type=completed.type.value,
            price=completed.price,
            notes=completed.notes,
            diagnosis=completed.diagnosis,
            prescription=completed.prescription,
            created_at=completed.created_at,
        )


class CreateVeterinarianUseCase:
    """Cadastra um novo veterinário."""

    def __init__(self, veterinarian_repository):
        self._veterinarian_repository = veterinarian_repository

    def execute(self, dto) -> "VeterinarianResponseDTO":
        from src.application.dto.consultation_dto import VeterinarianResponseDTO
        from src.domain.entities.veterinarian import Veterinarian

        existing = self._veterinarian_repository.find_by_user_id(dto.user_id)
        if existing is not None:
            raise VeterinarianCreationError(
                "Já existe veterinário cadastrado para este usuário."
            )

        if self._veterinarian_repository.crmv_exists(dto.crmv):
            raise VeterinarianCreationError(f"CRMV {dto.crmv} já cadastrado.")

        veterinarian = Veterinarian(
            id=None,
            user_id=dto.user_id,
            full_name=dto.full_name,
            crmv=dto.crmv,
            specialty=dto.specialty,
        )

        if not veterinarian.is_valid():
            raise VeterinarianCreationError("Dados do veterinário inválidos.")

        saved = self._veterinarian_repository.save(veterinarian)
        return VeterinarianResponseDTO(
            id=saved.id,
            user_id=saved.user_id,
            full_name=saved.full_name,
            crmv=saved.crmv,
            specialty=saved.specialty,
            created_at=saved.created_at,
        )


class ListVeterinariansUseCase:
    """Lista todos os veterinários."""

    def __init__(self, veterinarian_repository):
        self._veterinarian_repository = veterinarian_repository

    def execute(self) -> list["VeterinarianResponseDTO"]:
        from src.application.dto.consultation_dto import VeterinarianResponseDTO

        veterinarians = self._veterinarian_repository.list_all()
        return [
            VeterinarianResponseDTO(
                id=v.id,
                user_id=v.user_id,
                full_name=v.full_name,
                crmv=v.crmv,
                specialty=v.specialty,
                created_at=v.created_at,
            )
            for v in veterinarians
        ]


def _default_notification_subject() -> NotificationSubject:
    """Cria subject com observers padrão para notificações de agendamento."""
    subject = NotificationSubject()
    subject.attach(ConsultationScheduledObserver())
    subject.attach(EmailNotificationObserver())
    subject.attach(AppointmentReminderObserver())
    return subject
