"""
Facade Pattern - Orquestração do fluxo veterinário.

O padrão Facade fornece uma interface unificada e simplificada para um
conjunto de interfaces de subsistemas complexos. O cliente (CompleteConsultationUseCase)
interage apenas com o Facade, que coordena internamente múltiplos serviços.

Subsistemas coordenados:
  1. IAnimalService - busca dados do animal
  2. IConsultationRepository - atualiza status da consulta
  3. MedicalRecordFactory - cria registro médico adequado (Factory Method)
  4. IMedicalHistoryService - persiste registro no histórico
  5. PriceCalculationContext - calcula preço (Strategy)
  6. Geração de prescrição

Benefício: o caso de uso não precisa conhecer a ordem nem os detalhes de
cada subsistema; o Facade encapsula toda a complexidade do fluxo de conclusão.
"""

from dataclasses import dataclass

from src.domain.entities.consultation import Consultation, ConsultationStatus
from src.domain.patterns.factory.medical_record_factory import MedicalRecordFactory
from src.domain.patterns.strategy.price_calculation import PriceCalculationContext
from src.domain.repositories.consultation_repository import IConsultationRepository
from src.domain.services.animal_service import IAnimalService, IMedicalHistoryService


class AnimalNotFoundError(Exception):
    """Animal não encontrado no microsserviço de animais."""


class ConsultationCompletionError(Exception):
    """Erro ao concluir consulta via Facade."""


@dataclass
class ConsultationCompletionResult:
    """Resultado consolidado do fluxo de conclusão."""

    consultation: Consultation
    medical_record_description: str
    prescription: str
    animal_name: str


class VeterinaryServiceFacade:
    """
    Facade que simplifica o fluxo de conclusão de consulta veterinária.

    Coordena: buscar animal → calcular preço → gerar prescrição →
    criar registro médico → atualizar histórico → persistir consulta.
    """

    def __init__(
        self,
        animal_service: IAnimalService,
        medical_history_service: IMedicalHistoryService,
        consultation_repository: IConsultationRepository,
        record_factory: MedicalRecordFactory | None = None,
        price_context: PriceCalculationContext | None = None,
    ):
        self._animal_service = animal_service
        self._medical_history_service = medical_history_service
        self._consultation_repository = consultation_repository
        self._record_factory = record_factory or MedicalRecordFactory()
        self._price_context = price_context or PriceCalculationContext()

    def complete_consultation(
        self,
        consultation: Consultation,
        diagnosis: str,
        prescription_notes: str = "",
        procedure: str = "",
    ) -> ConsultationCompletionResult:
        """
        Interface simplificada do Facade: executa todo o fluxo de conclusão.

        O cliente chama apenas este método; internamente o Facade orquestra
        todos os subsistemas na ordem correta.
        """
        if not consultation.can_complete():
            raise ConsultationCompletionError(
                f"Consulta #{consultation.id} não pode ser concluída (status: {consultation.status})."
            )

        # 1. Buscar animal no microsserviço de animais
        animal = self._animal_service.get_animal(consultation.animal_id)
        if animal is None:
            raise AnimalNotFoundError(f"Animal {consultation.animal_id} não encontrado.")

        # 2. Calcular preço via Strategy Pattern
        price = self._price_context.calculate_price(consultation)

        # 3. Gerar prescrição
        prescription = self._generate_prescription(
            animal_name=animal.name,
            diagnosis=diagnosis,
            prescription_notes=prescription_notes,
            consultation_type=consultation.type.value,
        )

        # 4. Criar registro médico via Factory Method
        medical_record = self._record_factory.create_record_for_consultation(
            consultation_type=consultation.type,
            animal_id=consultation.animal_id,
            description=diagnosis or consultation.notes or "Consulta concluída",
            diagnosis=diagnosis,
            procedure=procedure,
        )

        # 5. Atualizar histórico médico do animal
        history_entry = self._medical_history_service.add_record(
            animal_id=consultation.animal_id,
            description=medical_record.to_history_description(),
            record_type=medical_record.record_type,
        )

        # 6. Atualizar consulta com status, preço, diagnóstico e prescrição
        consultation.status = ConsultationStatus.COMPLETED
        consultation.price = price
        consultation.diagnosis = diagnosis
        consultation.prescription = prescription
        updated = self._consultation_repository.update(consultation)

        return ConsultationCompletionResult(
            consultation=updated,
            medical_record_description=history_entry.get("description", medical_record.to_history_description()),
            prescription=prescription,
            animal_name=animal.name,
        )

    @staticmethod
    def _generate_prescription(
        animal_name: str,
        diagnosis: str,
        prescription_notes: str,
        consultation_type: str,
    ) -> str:
        """Gera texto de prescrição veterinária."""
        lines = [
            f"=== PRESCRIÇÃO VETERINÁRIA - {animal_name.upper()} ===",
            f"Tipo: {consultation_type}",
            f"Diagnóstico: {diagnosis or 'Não informado'}",
        ]
        if prescription_notes:
            lines.append(f"Medicamentos/Instruções: {prescription_notes}")
        else:
            lines.append("Medicamentos/Instruções: Conforme avaliação clínica.")
        lines.append("=== FIM DA PRESCRIÇÃO ===")
        return "\n".join(lines)
