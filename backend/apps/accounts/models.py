from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "student"
        TEACHER = "TEACHER", "teacher"
        ADMIN = "ADMIN", "admin"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        )

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.user.email} Profile"


class OTPPurpose(models.TextChoices):
    PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"
    EMAIL_VERIFICATION = "EMAIL_VERIFICATION", "Email Verification"


class OTP(models.Model):
    """
    A single one-time code issued to a user for a specific purpose
    (password reset or email verification). The code itself is
    never stored in plain text -- only its hash, using the same
    hasher Django already uses for passwords.

    Generating a new OTP for a (user, purpose) invalidates any
    previous unused one for that same purpose, both in application
    logic (see OTPService) and via the DB constraint below, so
    there's never more than one active code to be confused about.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps",
    )

    purpose = models.CharField(
        max_length=30,
        choices=OTPPurpose.choices,
    )

    code_hash = models.CharField(max_length=128)

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "purpose"],
                condition=models.Q(is_used=False),
                name="unique_active_otp_per_user_purpose",
            )
        ]

    def is_expired(self) -> bool:
        from django.utils import timezone
        return timezone.now() >= self.expires_at

    def check_code(self, raw_code: str) -> bool:
        from django.contrib.auth.hashers import check_password
        return check_password(raw_code, self.code_hash)

    def __str__(self):
        status = "used" if self.is_used else "active"
        return f"{self.user} - {self.get_purpose_display()} - {status}"