from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from apps.accounts.api.serializers.password_reset_serializer import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from core.api.responses import success_response


class PasswordResetRequestView(APIView):
    """
    No login required -- this is exactly for locked-out users.
    """

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset"

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            message=(
                "If an account exists for this email, a reset "
                "code has been sent."
            ),
            status_code=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset"

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            message=(
                "Password reset successfully. You can now log in "
                "with your new password."
            ),
            status_code=status.HTTP_200_OK,
        )