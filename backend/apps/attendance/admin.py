from django.contrib import admin

from apps.attendance.models import AttendanceRecord


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student_course",
        "date",
        "status",
        "marked_by",
    )
    list_filter = (
        "status",
        "date",
    )
    search_fields = (
        "student_course__enrollment__student__user__email",
        "student_course__program_course__course_code",
    )
    ordering = ("-date",)