from rest_framework import status
from rest_framework.views import APIView
from apps.accounts.api.serializers.register import RegisterSerializer
from apps.accounts.services.auth_services import register_user
from core.api.responses import success_response


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = register_user(serializer.validated_data)

        return success_response(
            message="User registered successfully.",
            data={
                "id": user.id,
                "email": user.email,
            },
            status_code=status.HTTP_201_CREATED,
        )