"""Autenticação JWT compartilhada entre microsserviços."""

import json
import os
import urllib.error
import urllib.request
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


def _verify_token_with_auth_service(token: str) -> dict:
    verify_url = os.environ.get("AUTH_VERIFY_URL", "").strip()
    if not verify_url:
        return None

    request = urllib.request.Request(
        verify_url,
        data=json.dumps({"token": token}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise exceptions.AuthenticationFailed("Token inválido.") from exc
        raise exceptions.AuthenticationFailed("Erro ao validar token.") from exc
    except urllib.error.URLError as exc:
        raise exceptions.AuthenticationFailed("Serviço de auth indisponível.") from exc


class JWTAuthentication(authentication.BaseAuthentication):
    """Valida tokens JWT emitidos pelo serviço de autenticação."""

    def authenticate(self, request) -> Optional[tuple]:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ", 1)[1]

        if os.environ.get("AUTH_VERIFY_URL", "").strip():
            payload = _verify_token_with_auth_service(token)
        else:
            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                )
            except jwt.ExpiredSignatureError as exc:
                raise exceptions.AuthenticationFailed("Token expirado.") from exc
            except jwt.InvalidTokenError as exc:
                raise exceptions.AuthenticationFailed("Token inválido.") from exc

        user = AuthenticatedUser(
            user_id=payload["user_id"],
            email=payload["email"],
            role=payload["role"],
        )
        return (user, token)


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
