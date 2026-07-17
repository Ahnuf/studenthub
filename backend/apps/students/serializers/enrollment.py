from rest_framework import serializers
from apps.academic.models import AcademicSession
from apps.students.services.enrollment_service import EnrollmentService
from apps.students.models import Enrollment, StudentCourse



class EnrollmentCreateSerializer(serializers.Serializer):
    """
    Serializer for creating a new student enrollment.
    """

    academic_session_id = serializers.PrimaryKeyRelatedField(
        queryset=AcademicSession.objects.all(),
        source="academic_session",
    )

    program_course_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )

    def create(self, validated_data):
        """
        Create a new enrollment using the EnrollmentService.
        """

        student_profile = self.context["student_profile"]

        return EnrollmentService.create_enrollment(
            student=student_profile,
            academic_session=validated_data["academic_session"],
            program_course_ids=validated_data["program_course_ids"],
        )


class StudentCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for enrolled courses.
    """

    course_code = serializers.CharField(
        source="program_course.course_code",
        read_only=True,
    )

    course_title = serializers.CharField(
        source="program_course.course.title",
        read_only=True,
    )

    credit_hours = serializers.IntegerField(
        source="program_course.total_credit_hours",
        read_only=True,
    )

    category = serializers.CharField(
        source="program_course.get_category_display",
        read_only=True,
    )

    class Meta:
        model = StudentCourse
        fields = (
            "id",
            "course_code",
            "course_title",
            "credit_hours",
            "category",
        )

class EnrollmentResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for enrollment details.
    """

    academic_session = serializers.StringRelatedField()

    status = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    student_courses = StudentCourseSerializer(
        # source="student_courses",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "academic_session",
            "semester",
            "status",
            "total_credit_hours",
            "submitted_at",
            "student_courses",
        )