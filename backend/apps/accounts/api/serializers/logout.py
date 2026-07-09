from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        token = RefreshToken(self.validated_data["refresh"])
        token.blacklist()