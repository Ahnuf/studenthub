from rest_framework import serializers

from apps.academic.models import AcademicSession


class AcademicSessionReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = (
            "id",
            "display_name",
        )