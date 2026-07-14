from rest_framework import serializers

from apps.academic.models import Program


class ProgramReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = (
            "id",
            "program_name",
            "degree_type",
        )