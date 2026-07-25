from rest_framework import serializers


class EmailVerificationConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)