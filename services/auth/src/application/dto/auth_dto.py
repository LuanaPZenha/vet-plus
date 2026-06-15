"""DTOs - Autenticação."""

from dataclasses import dataclass


@dataclass
class RegisterUserDTO:
    email: str
    password: str
    full_name: str
    role: str


@dataclass
class LoginDTO:
    email: str
    password: str


@dataclass
class AuthResponseDTO:
    access_token: str
    token_type: str
    user_id: int
    email: str
    role: str
    full_name: str
