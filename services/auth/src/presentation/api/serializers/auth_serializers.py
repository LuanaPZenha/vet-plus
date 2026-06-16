"""Serializers REST - Autenticação."""

from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=200)
    role = serializers.ChoiceField(
        choices=["admin", "veterinarian", "tutor"],
        default="tutor",
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class VerifyTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class AuthResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    role = serializers.CharField()
    full_name = serializers.CharField()
