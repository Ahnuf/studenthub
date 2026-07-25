from rest_framework import serializers

from apps.accounts.services.password_reset_service import PasswordResetService


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def save(self):
        PasswordResetService.request_reset(self.validated_data["email"])


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
    new_password = serializers.CharField(write_only=True)

    def save(self):
        PasswordResetService.confirm_reset(
            email=self.validated_data["email"],
            code=self.validated_data["code"],
            new_password=self.validated_data["new_password"],
        )