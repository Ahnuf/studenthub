from rest_framework import serializers


class TranscriptSummarySerializer(serializers.Serializer):
    earned_credit_hours = serializers.IntegerField()
    attempted_credit_hours = serializers.IntegerField()
    cgpa = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
    )


class TranscriptCourseSerializer(serializers.Serializer):
    course_code = serializers.CharField(
        source="program_course.course_code",
    )
    course_title = serializers.CharField(
        source="program_course.course.title",
    )
    credit_hours = serializers.IntegerField(
        source="program_course.total_credit_hours",
    )
    semester = serializers.IntegerField(
        source="semester_taken",
    )
    marks = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        allow_null=True,
    )
    grade = serializers.CharField(
        allow_null=True,
    )
    status = serializers.CharField()


class SemesterTranscriptSerializer(serializers.Serializer):
    semester = serializers.IntegerField()
    academic_session = serializers.CharField()
    earned_credit_hours = serializers.IntegerField()
    attempted_credit_hours = serializers.IntegerField()
    gpa = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
    )
    courses = TranscriptCourseSerializer(
        many=True,
    )


class TranscriptStudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    registration_number = serializers.CharField()
    name = serializers.CharField()
    program = serializers.CharField()
    current_semester = serializers.IntegerField()

class TranscriptSerializer(serializers.Serializer):
    student = serializers.SerializerMethodField()
    semesters = SemesterTranscriptSerializer(many=True)
    summary = TranscriptSummarySerializer()
    courses = TranscriptCourseSerializer(
        many=True,
    )

    def get_student(self, obj):
        student = obj["student"]

        return {
            "id": student.id,
            "registration_number": student.registration_number,
            "name": student.user.get_full_name(),
            "program": student.program.program_name,
            "current_semester": student.current_semester,
        }