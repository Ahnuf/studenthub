from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.accounts.api.serializers.register import RegisterSerializer
from apps.accounts.services.auth_services import register_user, generate_tokens, change_password


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = register_user(serializer.validated_data)

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