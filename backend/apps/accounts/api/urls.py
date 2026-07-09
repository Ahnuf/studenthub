from django.urls import path
from .views import RegisterView, LoginView, MeView, TokenRefreshView, LogoutView, ChangePasswordView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/change/",ChangePasswordView.as_view(),name="change-password"),
]