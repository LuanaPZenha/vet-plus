"""Modelos de persistência Django."""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("E-mail é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    """Modelo ORM - mapeamento para entidade User."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        VETERINARIAN = "veterinarian", "Veterinário"
        TUTOR = "tutor", "Tutor"

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TUTOR)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        app_label = "api"
        db_table = "users"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self) -> str:
        return self.email
