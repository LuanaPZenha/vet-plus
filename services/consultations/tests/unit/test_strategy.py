"""Testes unitários - Strategy Pattern."""

from datetime import datetime, timezone

from src.domain.entities.consultation import (
    Consultation,
    ConsultationStatus,
    ConsultationType,
)
from src.domain.patterns.strategy.price_calculation import (
    EmergencyConsultationStrategy,
    PriceCalculationContext,
    RegularConsultationStrategy,
    SurgeryStrategy,
)


def _make_consultation(consultation_type: ConsultationType) -> Consultation:
    return Consultation(
        id=1,
        animal_id=1,
        veterinarian_id=1,
        scheduled_at=datetime.now(timezone.utc),
        status=ConsultationStatus.SCHEDULED,
        type=consultation_type,
    )


class TestPriceCalculationStrategy:
    """Testes do Strategy Pattern para cálculo de preços."""

    def test_regular_consultation_price(self):
        strategy = RegularConsultationStrategy()
        consultation = _make_consultation(ConsultationType.REGULAR)

        assert strategy.calculate(consultation) == 150.00

    def test_emergency_consultation_price(self):
        strategy = EmergencyConsultationStrategy()
        consultation = _make_consultation(ConsultationType.EMERGENCY)

        assert strategy.calculate(consultation) == 300.00

    def test_surgery_price(self):
        strategy = SurgeryStrategy()
        consultation = _make_consultation(ConsultationType.SURGERY)

        assert strategy.calculate(consultation) == 800.00

    def test_context_selects_strategy_by_type(self):
        regular_context = PriceCalculationContext.for_consultation_type(ConsultationType.REGULAR)
        emergency_context = PriceCalculationContext.for_consultation_type(ConsultationType.EMERGENCY)
        surgery_context = PriceCalculationContext.for_consultation_type(ConsultationType.SURGERY)

        regular = _make_consultation(ConsultationType.REGULAR)
        emergency = _make_consultation(ConsultationType.EMERGENCY)
        surgery = _make_consultation(ConsultationType.SURGERY)

        assert regular_context.calculate_price(regular) == 150.00
        assert emergency_context.calculate_price(emergency) == 300.00
        assert surgery_context.calculate_price(surgery) == 800.00

    def test_context_allows_runtime_strategy_swap(self):
        context = PriceCalculationContext(strategy=RegularConsultationStrategy())
        consultation = _make_consultation(ConsultationType.REGULAR)

        assert context.calculate_price(consultation) == 150.00

        context.set_strategy(SurgeryStrategy())
        assert context.calculate_price(consultation) == 800.00
