from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from apps.accounts.api.serializers.email_verification_serializer import (
    EmailVerificationConfirmSerializer,
)
from apps.accounts.services.email_verification_service import (
    EmailVerificationService,
)
from core.api.responses import success_response


class EmailVerificationRequestView(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "email_verification"

    def post(self, request):
        EmailVerificationService.request_verification(request.user)

        return success_response(
            message="Verification code sent to your email.",
            status_code=status.HTTP_200_OK,
        )


class EmailVerificationConfirmView(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "email_verification"

    def post(self, request):
        serializer = EmailVerificationConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        EmailVerificationService.confirm_verification(
            request.user, serializer.validated_data["code"]
        )

        return success_response(
            message="Email verified successfully.",
            status_code=status.HTTP_200_OK,
        )