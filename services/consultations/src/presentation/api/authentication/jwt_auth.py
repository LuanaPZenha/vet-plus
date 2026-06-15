"""Autenticação JWT - validação de tokens emitidos pelo serviço de autenticação."""

from dataclasses import dataclass
from typing import Optional

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


@dataclass
class AuthenticatedUser:
    """Representação do usuário autenticado via JWT."""

    user_id: int
    email: str
    role: str
    is_authenticated: bool = True


class JWTAuthentication(authentication.BaseAuthentication):
    """Valida tokens JWT emitidos pelo serviço de autenticação."""

    def authenticate(self, request) -> Optional[tuple]:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
            user = AuthenticatedUser(
                user_id=payload["user_id"],
                email=payload["email"],
                role=payload["role"],
            )
            return (user, token)
        except jwt.ExpiredSignatureError as exc:
            raise exceptions.AuthenticationFailed("Token expirado.") from exc
        except jwt.InvalidTokenError as exc:
            raise exceptions.AuthenticationFailed("Token inválido.") from exc


class IsAuthenticatedRole:
    """Permissão baseada em roles do usuário."""

    allowed_roles: list[str] = []

    def has_permission(self, request, view) -> bool:
        user = request.user
        if not getattr(user, "is_authenticated", False):
            return False
        if not self.allowed_roles:
            return True
        return user.role in self.allowed_roles


class IsStaffRole(IsAuthenticatedRole):
    """Permite acesso apenas para administradores e veterinários."""

    allowed_roles = ["admin", "veterinarian"]


class IsAnyAuthenticatedRole(IsAuthenticatedRole):
    """Permite acesso para qualquer usuário autenticado."""

    allowed_roles = ["admin", "veterinarian", "tutor"]
