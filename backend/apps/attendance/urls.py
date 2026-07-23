from django.urls import path

from apps.attendance.views.attendance_view import (
    AttendanceMarkAPIView,
    AttendanceBulkMarkAPIView,
    AttendanceRosterAPIView,
    StudentCourseAttendanceAPIView,
)

app_name = "attendance"

urlpatterns = [
    path(
        "mark/",
        AttendanceMarkAPIView.as_view(),
        name="attendance-mark",
    ),
    path(
        "bulk-mark/",
        AttendanceBulkMarkAPIView.as_view(),
        name="attendance-bulk-mark",
    ),
    path(
        "roster/",
        AttendanceRosterAPIView.as_view(),
        name="attendance-roster",
    ),
    path(
        "student-courses/<int:student_course_id>/",
        StudentCourseAttendanceAPIView.as_view(),
        name="attendance-by-student-course",
    ),
]