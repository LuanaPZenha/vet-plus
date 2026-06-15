"""
Factory Method Pattern - Registros médicos.

O padrão Factory Method define uma interface para criar objetos, mas permite
que subclasses (ou, neste caso, métodos especializados da fábrica) decidam
qual classe concreta instanciar.

Estrutura:
  - MedicalRecord (produto abstrato): interface comum para registros médicos
  - ConsultationRecord, VaccinationRecord, SurgeryRecord (produtos concretos)
  - MedicalRecordFactory (criador): expõe factory methods que delegam a criação
    do tipo correto de registro com base no tipo da consulta

Benefício: o código cliente (Facade) não precisa conhecer as classes concretas;
apenas chama factory.create_record(consultation_type, ...) e recebe o registro adequado.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.consultation import ConsultationType


@dataclass
class MedicalRecord(ABC):
    """Produto abstrato do Factory Method - registro médico base."""

    animal_id: int
    description: str
    record_type: str
    created_at: datetime | None = None

    @abstractmethod
    def to_history_description(self) -> str:
        """Formata a descrição para persistência no histórico médico."""


@dataclass
class ConsultationRecord(MedicalRecord):
    """Produto concreto - registro de consulta de rotina."""

    diagnosis: str = ""

    def to_history_description(self) -> str:
        base = f"Consulta: {self.description}"
        if self.diagnosis:
            return f"{base} | Diagnóstico: {self.diagnosis}"
        return base


@dataclass
class VaccinationRecord(MedicalRecord):
    """Produto concreto - registro de vacinação."""

    vaccine_name: str = ""
    batch_number: str = ""

    def to_history_description(self) -> str:
        parts = [f"Vacinação: {self.description}"]
        if self.vaccine_name:
            parts.append(f"Vacina: {self.vaccine_name}")
        if self.batch_number:
            parts.append(f"Lote: {self.batch_number}")
        return " | ".join(parts)


@dataclass
class SurgeryRecord(MedicalRecord):
    """Produto concreto - registro de cirurgia."""

    procedure: str = ""
    anesthesia_type: str = ""

    def to_history_description(self) -> str:
        parts = [f"Cirurgia: {self.description}"]
        if self.procedure:
            parts.append(f"Procedimento: {self.procedure}")
        if self.anesthesia_type:
            parts.append(f"Anestesia: {self.anesthesia_type}")
        return " | ".join(parts)


class MedicalRecordFactory:
    """
    Criador (Creator) do Factory Method.

    Cada método create_* é um factory method que encapsula a lógica de
    instanciação do produto concreto correspondente.
    """

    @staticmethod
    def create_consultation_record(
        animal_id: int,
        description: str,
        diagnosis: str = "",
    ) -> ConsultationRecord:
        """Factory Method para registros de consulta."""
        return ConsultationRecord(
            animal_id=animal_id,
            description=description,
            record_type="consultation",
            diagnosis=diagnosis,
            created_at=datetime.now(),
        )

    @staticmethod
    def create_vaccination_record(
        animal_id: int,
        description: str,
        vaccine_name: str = "",
        batch_number: str = "",
    ) -> VaccinationRecord:
        """Factory Method para registros de vacinação."""
        return VaccinationRecord(
            animal_id=animal_id,
            description=description,
            record_type="vaccination",
            vaccine_name=vaccine_name,
            batch_number=batch_number,
            created_at=datetime.now(),
        )

    @staticmethod
    def create_surgery_record(
        animal_id: int,
        description: str,
        procedure: str = "",
        anesthesia_type: str = "",
    ) -> SurgeryRecord:
        """Factory Method para registros de cirurgia."""
        return SurgeryRecord(
            animal_id=animal_id,
            description=description,
            record_type="surgery",
            procedure=procedure,
            anesthesia_type=anesthesia_type,
            created_at=datetime.now(),
        )

    @classmethod
    def create_record_for_consultation(
        cls,
        consultation_type: ConsultationType,
        animal_id: int,
        description: str,
        diagnosis: str = "",
        procedure: str = "",
    ) -> MedicalRecord:
        """
        Factory Method polimórfico: seleciona o factory method adequado
        com base no tipo da consulta concluída.
        """
        if consultation_type == ConsultationType.SURGERY:
            return cls.create_surgery_record(
                animal_id=animal_id,
                description=description,
                procedure=procedure or description,
            )
        if consultation_type == ConsultationType.EMERGENCY:
            return cls.create_consultation_record(
                animal_id=animal_id,
                description=f"[EMERGÊNCIA] {description}",
                diagnosis=diagnosis,
            )
        return cls.create_consultation_record(
            animal_id=animal_id,
            description=description,
            diagnosis=diagnosis,
        )
