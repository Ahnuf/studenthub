from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.api.responses import success_response
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from apps.accounts.services.auth_services import register_user, generate_tokens
from rest_framework_simplejwt.serializers import TokenRefreshSerializer



class TokenRefreshView(APIView):
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return success_response(
            message="Token refreshed successfully.",
            data=serializer.validated_data,
            status_code=status.HTTP_200_OK,
        )


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        tokens = generate_tokens(user)

        return success_response(
            message="Login successful.",
            data={
                "user": UserSerializer(user).data,
                "tokens": tokens,
            },
            status_code=status.HTTP_200_OK,
        )

class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = create_user(serializer.validated_data)

        return Response(
            {
                "success": True,
                "message": "User registered successfully.",
                "data": {
                    "id": user.id,
                    "email": user.email,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return success_response(
            message="User fetched successfully.",
            data=serializer.data,
        )