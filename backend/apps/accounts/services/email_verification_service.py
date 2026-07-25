from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.accounts.models import OTPPurpose
from apps.accounts.services.otp_service import OTPService


class EmailVerificationService:
    """
    Email verification via a one-time code, for an already-
    authenticated (but unverified) user.
    """

    @staticmethod
    def request_verification(user) -> None:
        if user.is_verified:
            raise ValidationError(
                {"email": "This email is already verified."}
            )

        code = OTPService.generate_otp(user, OTPPurpose.EMAIL_VERIFICATION)
        OTPService.send_otp_email(user, OTPPurpose.EMAIL_VERIFICATION, code)

    @staticmethod
    @transaction.atomic
    def confirm_verification(user, code: str) -> None:
        OTPService.verify_otp(user, OTPPurpose.EMAIL_VERIFICATION, code)

        user.is_verified = True
        user.save(update_fields=["is_verified"])