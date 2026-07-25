from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MeView,
    TokenRefreshView,
    LogoutView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    EmailVerificationRequestView,
    EmailVerificationConfirmView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
    path("password/reset/request/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("email/verify/request/", EmailVerificationRequestView.as_view(), name="email-verify-request"),
    path("email/verify/confirm/", EmailVerificationConfirmView.as_view(), name="email-verify-confirm"),
]