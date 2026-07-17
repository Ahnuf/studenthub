from rest_framework import serializers
from apps.students.models import StudentProfile
from apps.students.services.student_service import StudentService


class StudentProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProfile

        exclude = (
            "user",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):

        user = self.context["request"].user

        return StudentService.create_profile(
            user=user,
            **validated_data,
        )


class StudentProfileDetailSerializer(serializers.ModelSerializer):

    university_name = serializers.CharField(
        source="university.name",
        read_only=True,
    )

    program_name = serializers.CharField(
        source="program.program_name",
        read_only=True,
    )

    joined_session_name = serializers.CharField(
        source="joined_session.display_name",
        read_only=True,
    )

    class Meta:

        model = StudentProfile

        fields = (
            "id",
            "university",
            "university_name",
            "program",
            "program_name",
            "joined_session",
            "joined_session_name",
            "current_semester",
            "registration_number",
            "roll_number",
            "expected_graduation_date",
            "academic_status",
        )

        read_only_fields = (
            "user",
            "created_at",
            "updated_at",
        )


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:

        model = StudentProfile

        exclude = (
            "user",
            "created_at",
            "updated_at",
        )

    def update(self, instance, validated_data):

        return StudentService.update_profile(
            instance,
            **validated_data,
        )