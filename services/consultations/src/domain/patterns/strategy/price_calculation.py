"""
Strategy Pattern - Cálculo de preços de consultas.

O padrão Strategy define uma família de algoritmos (estratégias de preço),
encapsula cada um e os torna intercambiáveis. O contexto (CompleteConsultation)
delega o cálculo ao objeto Strategy sem conhecer os detalhes de cada algoritmo.

Estrutura:
  - PriceCalculationStrategy (estratégia abstrata): interface calculate()
  - RegularConsultationStrategy, EmergencyConsultationStrategy, SurgeryStrategy
    (estratégias concretas): implementam regras de preço específicas
  - PriceCalculationContext (contexto): seleciona e executa a estratégia

Benefício: novos tipos de consulta com regras de preço diferentes podem ser
adicionados criando uma nova Strategy, sem modificar o código existente (OCP).
"""

from abc import ABC, abstractmethod

from src.domain.entities.consultation import Consultation, ConsultationType


class PriceCalculationStrategy(ABC):
    """Estratégia abstrata - define o contrato de cálculo de preço."""

    @abstractmethod
    def calculate(self, consultation: Consultation) -> float:
        """Calcula o preço final da consulta."""


class RegularConsultationStrategy(PriceCalculationStrategy):
    """Estratégia concreta - consulta de rotina."""

    BASE_PRICE = 150.00

    def calculate(self, consultation: Consultation) -> float:
        return self.BASE_PRICE


class EmergencyConsultationStrategy(PriceCalculationStrategy):
    """Estratégia concreta - consulta de emergência com acréscimo."""

    BASE_PRICE = 150.00
    EMERGENCY_MULTIPLIER = 2.0

    def calculate(self, consultation: Consultation) -> float:
        return round(self.BASE_PRICE * self.EMERGENCY_MULTIPLIER, 2)


class SurgeryStrategy(PriceCalculationStrategy):
    """Estratégia concreta - cirurgia com preço fixo elevado."""

    SURGERY_PRICE = 800.00

    def calculate(self, consultation: Consultation) -> float:
        return self.SURGERY_PRICE


class PriceCalculationContext:
    """
    Contexto do Strategy Pattern.

    Mantém referência à estratégia ativa e delega o cálculo de preço.
    A estratégia pode ser trocada em tempo de execução.
    """

    _strategies: dict[ConsultationType, PriceCalculationStrategy] = {
        ConsultationType.REGULAR: RegularConsultationStrategy(),
        ConsultationType.EMERGENCY: EmergencyConsultationStrategy(),
        ConsultationType.SURGERY: SurgeryStrategy(),
    }

    def __init__(self, strategy: PriceCalculationStrategy | None = None):
        self._strategy = strategy

    def set_strategy(self, strategy: PriceCalculationStrategy) -> None:
        """Permite trocar a estratégia em tempo de execução."""
        self._strategy = strategy

    def calculate_price(self, consultation: Consultation) -> float:
        """Executa o algoritmo da estratégia configurada."""
        strategy = self._strategy or self._strategies.get(
            consultation.type,
            RegularConsultationStrategy(),
        )
        return strategy.calculate(consultation)

    @classmethod
    def for_consultation_type(cls, consultation_type: ConsultationType) -> "PriceCalculationContext":
        """Factory helper que retorna contexto pré-configurado para o tipo."""
        strategy = cls._strategies.get(consultation_type, RegularConsultationStrategy())
        return cls(strategy=strategy)
