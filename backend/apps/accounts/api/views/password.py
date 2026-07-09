from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            change_password(
                request.user,
                serializer.validated_data["current_password"],
                serializer.validated_data["new_password"],
            )
        except ValueError as exc:
            from rest_framework import status
            from rest_framework.response import Response

            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Password changed successfully."
        )