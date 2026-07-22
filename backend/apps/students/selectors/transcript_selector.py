from django.db.models import QuerySet
from apps.students.models import (
    Enrollment,
    StudentCourse,
    StudentProfile,
)
from apps.students.models.student_course import CourseStatus


class TranscriptSelector:
    """
    Selector responsible only for reading transcript-related data.
    """

    @staticmethod
    def list_student_courses(
        student: StudentProfile,
    ) -> QuerySet[StudentCourse]:
        """
        Return all StudentCourse records for a student.
        """

        return (
            StudentCourse.objects.filter(
                enrollment__student=student,
            )
            .select_related(
                "enrollment",
                "program_course",
                "program_course__course",
            )
            .order_by(
                "enrollment__semester",
                "program_course__course__course_code",
            )
        )

    @staticmethod
    def list_passed_courses(
        student: StudentProfile,
    ) -> QuerySet[StudentCourse]:
        """
        Return only passed courses.
        """

        return (
            TranscriptSelector.list_student_courses(student)
            .filter(
                status=CourseStatus.PASSED,
            )
        )

    @staticmethod
    def list_completed_enrollments(
        student: StudentProfile,
    ) -> QuerySet[Enrollment]:
        """
        Return all enrollments ordered by semester.
        """

        return (
            Enrollment.objects.filter(
                student=student,
            )
            .select_related(
                "academic_session",
            )
            .order_by(
                "semester",
            )
        )

    @staticmethod
    def list_enrollments(
        student: StudentProfile,
    ):
        """
        Return all enrollments for a student ordered by semester.
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
            )
            .order_by(
                "semester",
            )
        )