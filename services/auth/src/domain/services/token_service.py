"""Serviços de domínio - Autenticação."""

from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings

from src.domain.entities.user import User


class TokenService:
    """Gera e valida tokens JWT (Single Responsibility)."""

    def generate_token(self, user: User) -> str:
        expiration = datetime.now(timezone.utc) + timedelta(
            hours=getattr(settings, "JWT_EXPIRATION_HOURS", 24)
        )
        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value,
            "exp": expiration,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
