from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.api.responses import success_response
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, LogoutSerializer
from apps.accounts.services.auth_services import register_user, generate_tokens, change_password
from apps.accounts.api.serializers import ChangePasswordSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer










