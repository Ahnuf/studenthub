from apps.attendance.models import AttendanceRecord, AttendanceStatus
from apps.students.models import StudentCourse


class AttendanceSelector:
    """
    Read-only operations for attendance.
    """

    @staticmethod
    def list_for_student_course(student_course: StudentCourse):
        """
        Return all attendance records for a single student's
        course enrollment, most recent first.
        """

        return (
            AttendanceRecord.objects
            .filter(student_course=student_course)
            .select_related("marked_by")
        )

    @staticmethod
    def get_record(student_course: StudentCourse, date):
        return (
            AttendanceRecord.objects
            .filter(
                student_course=student_course,
                date=date,
            )
            .first()
        )

    @staticmethod
    def list_student_courses_for_roster(
        program_course_id: int,
        academic_session_id: int,
    ):
        """
        Return the StudentCourse rows that make up the "roster" for
        a given course offering in a given session -- used to bulk
        mark attendance for everyone enrolled at once.
        """

        return (
            StudentCourse.objects
            .filter(
                program_course_id=program_course_id,
                enrollment__academic_session_id=academic_session_id,
            )
            .select_related(
                "enrollment__student__user",
                "program_course",
            )
        )

    @staticmethod
    def calculate_summary(student_course: StudentCourse) -> dict:
        """
        Return attendance counts and percentage for a student's
        course enrollment. Leave days are excluded from the
        percentage denominator -- an excused absence shouldn't
        count against the student the way an unexcused one does.
        """

        records = AttendanceRecord.objects.filter(
            student_course=student_course,
        )

        present_count = records.filter(
            status=AttendanceStatus.PRESENT,
        ).count()

        absent_count = records.filter(
            status=AttendanceStatus.ABSENT,
        ).count()

        leave_count = records.filter(
            status=AttendanceStatus.LEAVE,
        ).count()

        countable_sessions = present_count + absent_count

        if countable_sessions == 0:
            attendance_percentage = 0.0
        else:
            attendance_percentage = round(
                (present_count / countable_sessions) * 100,
                2,
            )

        return {
            "total_sessions": present_count + absent_count + leave_count,
            "present_count": present_count,
            "absent_count": absent_count,
            "leave_count": leave_count,
            "attendance_percentage": attendance_percentage,
        }