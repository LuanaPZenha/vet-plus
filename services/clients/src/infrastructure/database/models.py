"""Modelos de persistência Django."""

from django.db import models


class ClientModel(models.Model):
    """Modelo ORM - mapeamento para entidade Client."""

    full_name = models.CharField(max_length=200, verbose_name="Nome completo")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    address = models.TextField(verbose_name="Endereço")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "api"
        db_table = "clients"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.full_name
