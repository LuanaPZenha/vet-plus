"""Factory Method Pattern - registros médicos."""

from src.domain.patterns.factory.medical_record_factory import (
    ConsultationRecord,
    MedicalRecord,
    MedicalRecordFactory,
    SurgeryRecord,
    VaccinationRecord,
)

__all__ = [
    "ConsultationRecord",
    "MedicalRecord",
    "MedicalRecordFactory",
    "SurgeryRecord",
    "VaccinationRecord",
]
