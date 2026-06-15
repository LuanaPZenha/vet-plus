"""Casos de uso - Autenticação."""


class AuthenticationError(Exception):
    """Erro de autenticação."""


class RegistrationError(Exception):
    """Erro no registro de usuário."""


class RegisterUserUseCase:
    """Registra novo usuário no sistema."""

    def __init__(self, user_repository, token_service):
        self._user_repository = user_repository
        self._token_service = token_service

    def execute(self, dto) -> "AuthResponseDTO":
        from src.application.dto.auth_dto import AuthResponseDTO
        from src.domain.entities.user import User, UserRole

        if self._user_repository.email_exists(dto.email):
            raise RegistrationError("E-mail já cadastrado.")

        try:
            role = UserRole(dto.role)
        except ValueError as exc:
            raise RegistrationError(f"Role inválida: {dto.role}") from exc

        user = User(
            id=None,
            email=dto.email,
            full_name=dto.full_name,
            role=role,
        )
        saved_user = self._user_repository.save(user, dto.password)
        token = self._token_service.generate_token(saved_user)

        return AuthResponseDTO(
            access_token=token,
            token_type="Bearer",
            user_id=saved_user.id,
            email=saved_user.email,
            role=saved_user.role.value,
            full_name=saved_user.full_name,
        )


class LoginUserUseCase:
    """Autentica usuário e retorna token JWT."""

    def __init__(self, user_repository, token_service):
        self._user_repository = user_repository
        self._token_service = token_service

    def execute(self, dto) -> "AuthResponseDTO":
        from src.application.dto.auth_dto import AuthResponseDTO

        if not self._user_repository.verify_password(dto.email, dto.password):
            raise AuthenticationError("Credenciais inválidas.")

        user = self._user_repository.find_by_email(dto.email)
        if user is None or not user.is_active:
            raise AuthenticationError("Usuário inativo ou não encontrado.")

        token = self._token_service.generate_token(user)

        return AuthResponseDTO(
            access_token=token,
            token_type="Bearer",
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            full_name=user.full_name,
        )
