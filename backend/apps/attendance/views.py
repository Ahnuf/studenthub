from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied

from apps.common.permissions import IsTeacherOrAdmin
from apps.attendance.selectors.attendance_selector import AttendanceSelector
from apps.attendance.serializers.attendance_serializer import (
    AttendanceMarkSerializer,
    AttendanceBulkMarkSerializer,
    AttendanceRecordSerializer,
    StudentCourseAttendanceSerializer,
)
from apps.students.models import StudentCourse
from core.api.responses import success_response, error_response


class AttendanceMarkAPIView(GenericAPIView):
    """
    Mark one student's attendance for one day. Teacher/admin only.
    """

    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    serializer_class = AttendanceMarkSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        record = serializer.save()

        return success_response(
            message="Attendance marked successfully.",
            data=AttendanceRecordSerializer(record).data,
            status_code=status.HTTP_200_OK,
        )


class AttendanceBulkMarkAPIView(GenericAPIView):
    """
    Mark attendance for a whole class session at once. Teacher/
    admin only.
    """

    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    serializer_class = AttendanceBulkMarkSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        records = serializer.save()

        return success_response(
            message=f"Attendance marked for {len(records)} student(s).",
            data=AttendanceRecordSerializer(records, many=True).data,
            status_code=status.HTTP_200_OK,
        )


class AttendanceRosterAPIView(GenericAPIView):
    """
    Return the StudentCourse roster for a course offering in a
    session -- lets a teacher build the bulk-mark payload without
    needing to already know each StudentCourse ID.
    """

    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request, *args, **kwargs):
        program_course_id = request.query_params.get("program_course_id")
        academic_session_id = request.query_params.get("academic_session_id")

        if not program_course_id or not academic_session_id:
            return error_response(
                message="program_course_id and academic_session_id are required.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        roster = AttendanceSelector.list_student_courses_for_roster(
            program_course_id=program_course_id,
            academic_session_id=academic_session_id,
        )

        data = [
            {
                "student_course_id": student_course.id,
                "student_name": (
                    student_course.enrollment.student.user.get_full_name()
                ),
                "registration_number": (
                    student_course.enrollment.student.registration_number
                ),
            }
            for student_course in roster
        ]

        return success_response(
            message="Roster fetched successfully.",
            data=data,
            status_code=status.HTTP_200_OK,
        )


class StudentCourseAttendanceAPIView(GenericAPIView):
    """
    A single StudentCourse's attendance summary + day-by-day
    records. A student may only view their own; teachers/admins
    may view any.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = StudentCourseAttendanceSerializer

    def get(self, request, student_course_id, *args, **kwargs):
        student_course = (
            StudentCourse.objects
            .select_related("enrollment__student__user")
            .filter(id=student_course_id)
            .first()
        )

        if student_course is None:
            raise NotFound("Student course not found.")

        is_owner = (
            student_course.enrollment.student.user_id == request.user.id
        )
        is_staff = request.user.role in (
            request.user.Role.TEACHER,
            request.user.Role.ADMIN,
        )

        if not is_owner and not is_staff:
            raise PermissionDenied(
                "You can only view your own attendance."
            )

        summary = AttendanceSelector.calculate_summary(student_course)
        records = AttendanceSelector.list_for_student_course(student_course)

        serializer = self.get_serializer(
            {
                "summary": summary,
                "records": records,
            }
        )

        return success_response(
            message="Attendance fetched successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )