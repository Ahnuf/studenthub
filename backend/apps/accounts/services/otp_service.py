import random
import string
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.accounts.models import OTP, OTPPurpose

OTP_LENGTH = 6
OTP_VALIDITY_MINUTES = 10
OTP_RESEND_COOLDOWN_SECONDS = 60


class OTPService:
    """
    Shared one-time-code mechanism used by both password reset and
    email verification. Each purpose gets its own OTP rows, kept
    separate by the `purpose` field -- generating a code for one
    purpose never invalidates a code for the other.
    """

    @staticmethod
    @transaction.atomic
    def generate_otp(user, purpose: str) -> str:
        """
        Create a new OTP, invalidating any previous unused OTP for
        the same (user, purpose). Returns the raw code -- this is
        the only moment it ever exists in plain text; only its
        hash is persisted.
        """

        OTPService._enforce_cooldown(user, purpose)

        OTP.objects.filter(
            user=user, purpose=purpose, is_used=False
        ).update(is_used=True)

        raw_code = "".join(random.choices(string.digits, k=OTP_LENGTH))

        OTP.objects.create(
            user=user,
            purpose=purpose,
            code_hash=make_password(raw_code),
            expires_at=timezone.now() + timedelta(minutes=OTP_VALIDITY_MINUTES),
        )

        return raw_code

    @staticmethod
    def _enforce_cooldown(user, purpose: str):
        recent = (
            OTP.objects
            .filter(user=user, purpose=purpose)
            .order_by("-created_at")
            .first()
        )

        if recent is None:
            return

        elapsed = (timezone.now() - recent.created_at).total_seconds()

        if elapsed < OTP_RESEND_COOLDOWN_SECONDS:
            raise ValidationError(
                {
                    "code": (
                        "Please wait before requesting another code."
                    )
                }
            )

    @staticmethod
    @transaction.atomic
    def verify_otp(user, purpose: str, raw_code: str) -> OTP:
        """
        Validates a code against the latest unused OTP for this
        (user, purpose). Marks it used on success -- a code can
        never be verified twice, even if it hasn't expired yet.
        """

        otp = (
            OTP.objects
            .filter(user=user, purpose=purpose, is_used=False)
            .order_by("-created_at")
            .first()
        )

        if otp is None or otp.is_expired() or not otp.check_code(raw_code):
            raise ValidationError(
                {"code": "Invalid or expired code."}
            )

        otp.is_used = True
        otp.save(update_fields=["is_used", "updated_at"])

        return otp

    @staticmethod
    def send_otp_email(user, purpose: str, code: str):
        """
        Uses whatever EMAIL_BACKEND is configured in settings. With
        Django's console backend (recommended until real SMTP is
        set up), this just logs the email to the server console --
        $0, nothing actually sent, but the same code path works
        unchanged once real email sending is configured later.
        """

        if purpose == OTPPurpose.PASSWORD_RESET:
            subject = "Your StudentHub password reset code"
            action = "reset your password"
        else:
            subject = "Your StudentHub verification code"
            action = "verify your email"

        message = (
            f"Your code to {action} is: {code}\n\n"
            f"This code expires in {OTP_VALIDITY_MINUTES} minutes. "
            "If you didn't request this, you can ignore this email."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[user.email],
        )