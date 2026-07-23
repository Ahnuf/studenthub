from rest_framework import serializers

from apps.attendance.models import AttendanceRecord
from apps.attendance.selectors.attendance_selector import AttendanceSelector
from apps.attendance.services.attendance_service import AttendanceService
from apps.students.models import StudentCourse


class AttendanceMarkSerializer(serializers.Serializer):
    """
    Mark a single student's attendance for a single day.
    """

    student_course_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentCourse.objects.all(),
        source="student_course",
    )

    date = serializers.DateField()

    status = serializers.ChoiceField(
        choices=AttendanceRecord._meta.get_field("status").choices,
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )

    def save(self):
        request = self.context["request"]

        return AttendanceService.mark_attendance(
            student_course=self.validated_data["student_course"],
            date=self.validated_data["date"],
            status=self.validated_data["status"],
            marked_by=request.user,
            remarks=self.validated_data.get("remarks", ""),
        )


class AttendanceBulkMarkEntrySerializer(serializers.Serializer):
    student_course_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentCourse.objects.all(),
        source="student_course",
    )

    status = serializers.ChoiceField(
        choices=AttendanceRecord._meta.get_field("status").choices,
    )


class AttendanceBulkMarkSerializer(serializers.Serializer):
    """
    Mark attendance for many students in one class session at once.
    """

    date = serializers.DateField()

    entries = AttendanceBulkMarkEntrySerializer(many=True)

    def save(self):
        request = self.context["request"]

        return AttendanceService.bulk_mark_attendance(
            entries=self.validated_data["entries"],
            date=self.validated_data["date"],
            marked_by=request.user,
        )


class AttendanceRecordSerializer(serializers.ModelSerializer):

    marked_by_name = serializers.CharField(
        source="marked_by.get_full_name",
        read_only=True,
        default=None,
    )

    class Meta:
        model = AttendanceRecord
        fields = (
            "id",
            "date",
            "status",
            "remarks",
            "marked_by_name",
            "created_at",
        )


class AttendanceSummarySerializer(serializers.Serializer):
    total_sessions = serializers.IntegerField()
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    leave_count = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()


class StudentCourseAttendanceSerializer(serializers.Serializer):
    """
    Combined response for "my attendance in this course":
    summary + the day-by-day records.
    """

    summary = AttendanceSummarySerializer()
    records = AttendanceRecordSerializer(many=True)