"""URLs da API de Autenticação."""

from django.urls import path

from src.presentation.api.views.auth_views import LoginView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]
