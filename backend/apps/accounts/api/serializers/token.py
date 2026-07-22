from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class TokenRefreshSerializer(serializers.Serializer):
    """
    Validates a refresh token and issues a new access token.
    """

    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs["refresh"]

        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            raise serializers.ValidationError(
                {"refresh": "Invalid or expired refresh token."}
            )

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }