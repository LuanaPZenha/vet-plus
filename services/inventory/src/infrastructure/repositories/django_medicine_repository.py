from decimal import Decimal

from django.db.models import F

from src.domain.entities.medicine import Medicine, MedicineCategory, MovementType, StockMovement
from src.domain.repositories.medicine_repository import IMedicineRepository, IStockMovementRepository
from src.infrastructure.database.models import MedicineModel, StockMovementModel


class DjangoMedicineRepository(IMedicineRepository):
    def _to_entity(self, model: MedicineModel) -> Medicine:
        return Medicine(
            id=model.id,
            name=model.name,
            generic_name=model.generic_name,
            category=MedicineCategory(model.category),
            unit=model.unit,
            quantity=model.quantity,
            min_stock=model.min_stock,
            batch_number=model.batch_number,
            expiration_date=model.expiration_date,
            supplier=model.supplier,
            unit_price=model.unit_price,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def save(self, medicine: Medicine) -> Medicine:
        model = MedicineModel.objects.create(
            name=medicine.name,
            generic_name=medicine.generic_name,
            category=medicine.category.value,
            unit=medicine.unit,
            quantity=medicine.quantity,
            min_stock=medicine.min_stock,
            batch_number=medicine.batch_number,
            expiration_date=medicine.expiration_date,
            supplier=medicine.supplier,
            unit_price=medicine.unit_price,
        )
        return self._to_entity(model)

    def find_by_id(self, medicine_id: int) -> Medicine | None:
        try:
            return self._to_entity(MedicineModel.objects.get(id=medicine_id))
        except MedicineModel.DoesNotExist:
            return None

    def find_all(self) -> list[Medicine]:
        return [self._to_entity(m) for m in MedicineModel.objects.all()]

    def update(self, medicine: Medicine) -> Medicine:
        MedicineModel.objects.filter(id=medicine.id).update(
            name=medicine.name,
            generic_name=medicine.generic_name,
            category=medicine.category.value,
            unit=medicine.unit,
            quantity=medicine.quantity,
            min_stock=medicine.min_stock,
            batch_number=medicine.batch_number,
            expiration_date=medicine.expiration_date,
            supplier=medicine.supplier,
            unit_price=medicine.unit_price,
        )
        return self.find_by_id(medicine.id)

    def find_low_stock(self) -> list[Medicine]:
        models = MedicineModel.objects.filter(quantity__lte=F("min_stock"))
        return [self._to_entity(m) for m in models]


class DjangoStockMovementRepository(IStockMovementRepository):
    def _to_entity(self, model: StockMovementModel) -> StockMovement:
        return StockMovement(
            id=model.id,
            medicine_id=model.medicine_id,
            movement_type=MovementType(model.movement_type),
            quantity=model.quantity,
            reason=model.reason,
            performed_by=model.performed_by,
            stock_after=model.stock_after,
            created_at=model.created_at,
        )

    def save(self, movement: StockMovement) -> StockMovement:
        model = StockMovementModel.objects.create(
            medicine_id=movement.medicine_id,
            movement_type=movement.movement_type.value,
            quantity=movement.quantity,
            reason=movement.reason,
            performed_by=movement.performed_by,
            stock_after=movement.stock_after,
        )
        return self._to_entity(model)

    def find_all(self, medicine_id: int | None = None) -> list[StockMovement]:
        qs = StockMovementModel.objects.all()
        if medicine_id:
            qs = qs.filter(medicine_id=medicine_id)
        return [self._to_entity(m) for m in qs]
