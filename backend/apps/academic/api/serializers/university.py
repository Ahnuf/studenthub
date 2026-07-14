from rest_framework import serializers

from apps.academic.models import University


class UniversityReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = (
            "id",
            "name",
            "short_name",
        )