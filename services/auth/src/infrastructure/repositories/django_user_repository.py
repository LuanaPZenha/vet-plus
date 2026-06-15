"""Implementação concreta do repositório de usuários (Repository Pattern)."""

from typing import Optional

from src.domain.entities.user import User, UserRole
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.database.models import UserModel


class DjangoUserRepository(IUserRepository):
    """Adaptador Django ORM para IUserRepository."""

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            role=UserRole(model.role),
            is_active=model.is_active,
            created_at=model.created_at,
        )

    def save(self, user: User, password: str) -> User:
        model = UserModel.objects.create(
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            is_active=user.is_active,
        )
        model.set_password(password)
        model.save()
        return self._to_entity(model)

    def find_by_email(self, email: str) -> Optional[User]:
        try:
            model = UserModel.objects.get(email=email)
            return self._to_entity(model)
        except UserModel.DoesNotExist:
            return None

    def find_by_id(self, user_id: int) -> Optional[User]:
        try:
            model = UserModel.objects.get(id=user_id)
            return self._to_entity(model)
        except UserModel.DoesNotExist:
            return None

    def verify_password(self, email: str, password: str) -> bool:
        try:
            model = UserModel.objects.get(email=email)
            return model.check_password(password)
        except UserModel.DoesNotExist:
            return False

    def email_exists(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()
