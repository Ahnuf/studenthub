from apps.students.models import Enrollment, StudentCourse, CourseStatus
from apps.academic.models import ProgramCourse


class EnrollmentSelector:
    """
    Read-only operations related to student enrollments.
    """

    @staticmethod
    def get_program_courses(
        program_course_ids: list[int],
    ):
        """
        Retrieve ProgramCourse objects for the provided IDs.
        """
        return (
            ProgramCourse.objects
            .select_related(
                "program",
                "course",
            )
        .filter(
            id__in=program_course_ids,
            is_active=True,
        )
    )

    @staticmethod
    def get_enrollment(student, academic_session):
        return (
            Enrollment.objects
            .select_related(
                "student",
                "academic_session",
            )
            .filter(
                student=student,
                academic_session=academic_session,
            )
            .first()
        )

    @staticmethod
    def get_current_enrollment(student):
        """
        Return the student's Enrollment tied to their university's
        current AcademicSession (is_current=True), if one exists.
        """

        return (
            Enrollment.objects
            .select_related(
                "academic_session",
            )
            .prefetch_related(
                "student_courses",
                "student_courses__program_course",
                "student_courses__program_course__course",
            )
            .filter(
                student=student,
                academic_session__is_current=True,
            )
            .first()
        )

    @staticmethod
    def list_completed_courses(student):
        return (
            StudentCourse.objects
            .select_related(
                "program_course",
                "program_course__course",
            )
            .filter(
                enrollment__student=student,
                status=CourseStatus.PASSED,
            )
        )

    @staticmethod
    def list_student_courses(student):
        return (
            StudentCourse.objects
            .select_related(
                "program_course",
                "program_course__course",
                "enrollment",
            )
            .filter(
                enrollment__student=student,
            )
        )