from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.accounts.models import OTPPurpose
from apps.accounts.services.otp_service import OTPService

User = get_user_model()


class PasswordResetService:
    """
    Password reset via a one-time code, no login required.
    """

    @staticmethod
    def request_reset(email: str) -> None:
        """
        Deliberately silent if the email doesn't match an account
        -- the view always returns the same generic message either
        way, so this endpoint can't be used to discover which
        emails are registered.
        """

        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            return

        code = OTPService.generate_otp(user, OTPPurpose.PASSWORD_RESET)
        OTPService.send_otp_email(user, OTPPurpose.PASSWORD_RESET, code)

    @staticmethod
    @transaction.atomic
    def confirm_reset(email: str, code: str, new_password: str) -> None:
        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            # Same generic error as an invalid code -- still no
            # confirmation of whether the email exists.
            raise ValidationError({"code": "Invalid or expired code."})

        OTPService.verify_otp(user, OTPPurpose.PASSWORD_RESET, code)

        try:
            validate_password(new_password, user)
        except DjangoValidationError as e:
            raise ValidationError({"new_password": e.messages})

        user.set_password(new_password)
        user.save(update_fields=["password"])