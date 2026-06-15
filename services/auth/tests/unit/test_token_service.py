"""Testes unitários TDD - TokenService."""

import jwt
import pytest
from django.conf import settings

from src.domain.entities.user import User, UserRole
from src.domain.services.token_service import TokenService


@pytest.fixture
def token_service():
    return TokenService()


@pytest.fixture
def sample_user():
    return User(
        id=1,
        email="vet@test.com",
        full_name="Dr. Silva",
        role=UserRole.VETERINARIAN,
    )


class TestTokenService:
    """TDD: Red -> Green -> Refactor para geração de JWT."""

    def test_generate_token_returns_string(self, token_service, sample_user):
        token = token_service.generate_token(sample_user)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_generate_token_contains_user_data(self, token_service, sample_user):
        token = token_service.generate_token(sample_user)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        assert payload["user_id"] == 1
        assert payload["email"] == "vet@test.com"
        assert payload["role"] == "veterinarian"

    def test_decode_token_returns_payload(self, token_service, sample_user):
        token = token_service.generate_token(sample_user)
        payload = token_service.decode_token(token)
        assert payload["user_id"] == sample_user.id
