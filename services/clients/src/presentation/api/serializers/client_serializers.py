"""Serializers REST - Clientes."""

from rest_framework import serializers


class CreateClientSerializer(serializers.Serializer):
    nome_completo = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    telefone = serializers.CharField(max_length=20)
    cpf = serializers.CharField(max_length=14)
    endereco = serializers.CharField()


class ClientResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome_completo = serializers.CharField()
    email = serializers.EmailField()
    telefone = serializers.CharField()
    cpf = serializers.CharField()
    endereco = serializers.CharField()
    criado_em = serializers.DateTimeField()

    @staticmethod
    def from_dto(dto) -> dict:
        return {
            "id": dto.id,
            "nome_completo": dto.full_name,
            "email": dto.email,
            "telefone": dto.phone,
            "cpf": dto.cpf,
            "endereco": dto.address,
            "criado_em": dto.created_at,
        }
