from rest_framework import status
from rest_framework.views import APIView
from apps.accounts.api.serializers import LoginSerializer, UserSerializer
from core.api.responses import success_response
from apps.accounts.services.auth_services import generate_tokens


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