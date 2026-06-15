"""Testes unitários - Factory Method Pattern."""

from src.domain.entities.consultation import ConsultationType
from src.domain.patterns.factory.medical_record_factory import (
    ConsultationRecord,
    MedicalRecordFactory,
    SurgeryRecord,
    VaccinationRecord,
)


class TestMedicalRecordFactory:
    """Testes do Factory Method para registros médicos."""

    def test_create_consultation_record(self):
        record = MedicalRecordFactory.create_consultation_record(
            animal_id=1,
            description="Check-up de rotina",
            diagnosis="Saudável",
        )

        assert isinstance(record, ConsultationRecord)
        assert record.animal_id == 1
        assert record.record_type == "consultation"
        assert "Saudável" in record.to_history_description()

    def test_create_vaccination_record(self):
        record = MedicalRecordFactory.create_vaccination_record(
            animal_id=2,
            description="Vacinação anual",
            vaccine_name="V10",
            batch_number="LOT-123",
        )

        assert isinstance(record, VaccinationRecord)
        assert record.vaccine_name == "V10"
        assert "LOT-123" in record.to_history_description()

    def test_create_surgery_record(self):
        record = MedicalRecordFactory.create_surgery_record(
            animal_id=3,
            description="Castração",
            procedure="Orquiectomia",
            anesthesia_type="Geral",
        )

        assert isinstance(record, SurgeryRecord)
        assert record.procedure == "Orquiectomia"
        assert "Orquiectomia" in record.to_history_description()

    def test_create_record_for_regular_consultation(self):
        record = MedicalRecordFactory.create_record_for_consultation(
            consultation_type=ConsultationType.REGULAR,
            animal_id=1,
            description="Consulta de rotina",
            diagnosis="Sem alterações",
        )

        assert isinstance(record, ConsultationRecord)
        assert record.record_type == "consultation"

    def test_create_record_for_emergency_consultation(self):
        record = MedicalRecordFactory.create_record_for_consultation(
            consultation_type=ConsultationType.EMERGENCY,
            animal_id=1,
            description="Atendimento urgente",
            diagnosis="Febre",
        )

        assert isinstance(record, ConsultationRecord)
        assert "[EMERGÊNCIA]" in record.description

    def test_create_record_for_surgery_consultation(self):
        record = MedicalRecordFactory.create_record_for_consultation(
            consultation_type=ConsultationType.SURGERY,
            animal_id=1,
            description="Cirurgia ortopédica",
            procedure="Fixação de fratura",
        )

        assert isinstance(record, SurgeryRecord)
        assert record.record_type == "surgery"
