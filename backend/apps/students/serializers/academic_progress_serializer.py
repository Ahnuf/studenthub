from rest_framework import serializers


class AcademicIdentitySerializer(serializers.Serializer):
    university = serializers.CharField()
    program = serializers.CharField()
    current_semester = serializers.IntegerField()
    joined_session = serializers.CharField()
    academic_status = serializers.CharField()
    expected_graduation_date = serializers.DateField()


class CurrentCourseSerializer(serializers.Serializer):
    course_code = serializers.CharField(
        source="program_course.course_code",
    )
    course_title = serializers.CharField(
        source="program_course.course.title",
    )
    credit_hours = serializers.IntegerField(
        source="program_course.total_credit_hours",
    )
    status = serializers.CharField()


class CurrentSemesterSerializer(serializers.Serializer):
    current_courses = CurrentCourseSerializer(many=True)
    current_credit_hours = serializers.IntegerField()
    semester_gpa = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
    )


class DegreeProgressSerializer(serializers.Serializer):
    completed_credit_hours = serializers.IntegerField()
    remaining_credit_hours = serializers.IntegerField()
    completed_courses = serializers.IntegerField()
    remaining_courses = serializers.IntegerField()
    total_program_credit_hours = serializers.IntegerField()
    total_program_courses = serializers.IntegerField()
    progress_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )


class AcademicPerformanceSerializer(serializers.Serializer):
    cgpa = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
    )


class AssignmentSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course_name = serializers.CharField()
    title = serializers.CharField()
    due_date = serializers.DateField()
    status = serializers.CharField()


class AssignmentsDueSoonSerializer(serializers.Serializer):
    upcoming = AssignmentSummarySerializer(many=True)
    overdue = AssignmentSummarySerializer(many=True)


class AcademicProgressDashboardSerializer(serializers.Serializer):
    academic_identity = AcademicIdentitySerializer()
    current_semester = CurrentSemesterSerializer()
    degree_progress = DegreeProgressSerializer()
    performance = AcademicPerformanceSerializer()
    assignments_due_soon = AssignmentsDueSoonSerializer()