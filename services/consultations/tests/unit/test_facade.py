"""Testes unitários - Facade Pattern."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

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
from src.domain.services.animal_service import AnimalReference
from src.infrastructure.services.animal_services import (
    InMemoryAnimalService,
    InMemoryMedicalHistoryService,
)


def _scheduled_consultation(consultation_type: ConsultationType = ConsultationType.REGULAR) -> Consultation:
    return Consultation(
        id=1,
        animal_id=10,
        veterinarian_id=1,
        scheduled_at=datetime(2026, 6, 15, 10, 0, tzinfo=timezone.utc),
        status=ConsultationStatus.SCHEDULED,
        type=consultation_type,
        notes="Consulta de teste",
    )


class TestVeterinaryServiceFacade:
    """Testes do Facade Pattern para conclusão de consultas."""

    def setup_method(self):
        self.animal_service = InMemoryAnimalService()
        self.animal_service.register_animal(
            AnimalReference(id=10, name="Rex", species="Cão", client_id=1)
        )
        self.medical_history_service = InMemoryMedicalHistoryService()
        self.consultation_repository = MagicMock()
        self.facade = VeterinaryServiceFacade(
            animal_service=self.animal_service,
            medical_history_service=self.medical_history_service,
            consultation_repository=self.consultation_repository,
        )

    def test_complete_consultation_regular(self):
        consultation = _scheduled_consultation(ConsultationType.REGULAR)
        self.consultation_repository.update.return_value = Consultation(
            id=1,
            animal_id=10,
            veterinarian_id=1,
            scheduled_at=consultation.scheduled_at,
            status=ConsultationStatus.COMPLETED,
            type=ConsultationType.REGULAR,
            price=150.00,
            diagnosis="Saudável",
            prescription="Repouso",
        )

        result = self.facade.complete_consultation(
            consultation=consultation,
            diagnosis="Saudável",
            prescription_notes="Repouso por 2 dias",
        )

        assert result.consultation.price == 150.00
        assert result.animal_name == "Rex"
        assert "PRESCRIÇÃO" in result.prescription
        assert len(self.medical_history_service.records) == 1
        self.consultation_repository.update.assert_called_once()

    def test_complete_consultation_emergency_price(self):
        consultation = _scheduled_consultation(ConsultationType.EMERGENCY)
        self.consultation_repository.update.side_effect = lambda c: c

        result = self.facade.complete_consultation(
            consultation=consultation,
            diagnosis="Febre alta",
        )

        assert result.consultation.price == 300.00

    def test_complete_consultation_surgery_price(self):
        consultation = _scheduled_consultation(ConsultationType.SURGERY)
        self.consultation_repository.update.side_effect = lambda c: c

        result = self.facade.complete_consultation(
            consultation=consultation,
            diagnosis="Fratura",
            procedure="Fixação",
        )

        assert result.consultation.price == 800.00
        assert self.medical_history_service.records[0]["record_type"] == "surgery"

    def test_complete_consultation_animal_not_found(self):
        consultation = _scheduled_consultation()
        consultation.animal_id = 999

        mock_animal_service = MagicMock()
        mock_animal_service.get_animal.return_value = None
        facade = VeterinaryServiceFacade(
            animal_service=mock_animal_service,
            medical_history_service=self.medical_history_service,
            consultation_repository=self.consultation_repository,
        )

        with pytest.raises(AnimalNotFoundError):
            facade.complete_consultation(consultation=consultation, diagnosis="Teste")

    def test_complete_consultation_already_completed(self):
        consultation = _scheduled_consultation()
        consultation.status = ConsultationStatus.COMPLETED

        with pytest.raises(ConsultationCompletionError):
            self.facade.complete_consultation(consultation=consultation, diagnosis="Teste")
