from decimal import Decimal

from apps.academic.selectors.grading_selector import (
    GradingSelector,
)
from apps.students.models import StudentProfile
from apps.students.models.student_course import CourseStatus


class GradingService:
    """
    Business logic related to grading.
    """

    @staticmethod
    def calculate_grade(
        student: StudentProfile,
        marks: Decimal,
    ):
        """
        Return the GradePoint corresponding to the student's marks.
        """

        grading_scheme = (
            GradingSelector.get_active_scheme(
                student,
            )
        )

        return (
            GradingSelector.get_grade_point(
                grading_scheme,
                marks,
            )
        )

    @staticmethod
    def calculate_grade_points(
        student: StudentProfile,
        marks: Decimal,
    ) -> Decimal:
        """
        Return the grade points for the given marks.
        """

        grade_point = (
            GradingService.calculate_grade(
                student,
                marks,
            )
        )

        return grade_point.grade_points

    @staticmethod
    def calculate_quality_points(
        student: StudentProfile,
        marks: Decimal,
        credit_hours: int,
    ) -> Decimal:
        """
        Return quality points for a course.
        """

        grade_points = (
            GradingService.calculate_grade_points(
                student,
                marks,
            )
        )

        return (
            grade_points
            * Decimal(credit_hours)
        )

    @staticmethod
    def calculate_gpa(
        student: StudentProfile,
        student_courses,
    ) -> Decimal:
        """
        Calculate GPA over any collection of StudentCourse records.

        Callers control the scope: pass courses from a single
        enrollment for SGPA, or every course a student has taken
        for CGPA. Only records with a final status (PASSED/FAILED)
        and recorded marks contribute.
        """

        completed_statuses = (
            CourseStatus.PASSED,
            CourseStatus.FAILED,
        )

        total_quality_points = Decimal("0")
        attempted_credit_hours = 0

        for student_course in student_courses:

            if student_course.status not in completed_statuses:
                continue

            if student_course.marks is None:
                continue

            credit_hours = (
                student_course.program_course.total_credit_hours
            )

            total_quality_points += (
                GradingService.calculate_quality_points(
                    student=student,
                    marks=student_course.marks,
                    credit_hours=credit_hours,
                )
            )

            attempted_credit_hours += credit_hours

        if attempted_credit_hours == 0:
            return Decimal("0.00")

        return (
            total_quality_points
            / Decimal(attempted_credit_hours)
        ).quantize(Decimal("0.00"))