from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.academic.models import Grade
from apps.academic.services.grading_service import GradingService
from apps.students.models import (
    StudentCourse,
    CourseStatus,
)
from apps.students.selectors.result_selector import ResultSelector


class StudentResultService:
    """
    Handles publishing final results for student courses.
    """

    @staticmethod
    @transaction.atomic
    def publish_result(
        student_course_id: int,
        marks: Decimal,
    ) -> StudentCourse:
        """
        Publish the final result for a student's course.
        """

        student_course = (
            ResultSelector.get_student_course(
                student_course_id
            )
        )

        if student_course is None:
            raise ValidationError(
                {
                    "student_course_id": (
                        "Student course does not exist."
                    )
                }
            )

        StudentResultService._validate_student_course(
            student_course,
        )

        StudentResultService._validate_marks(
            marks,
        )

        grade_point = (
            GradingService.calculate_grade(
                student=student_course.enrollment.student,
                marks=marks,
            )
        )

        StudentResultService._update_student_course(
            student_course=student_course,
            marks=marks,
            grade=grade_point.grade,
        )

        return student_course

    @staticmethod
    def _validate_student_course(
        student_course: StudentCourse,
    ):
        """
        Ensure the student course is eligible for result publishing.
        """

        if (
            student_course.status
            != CourseStatus.ENROLLED
        ):
            raise ValidationError(
                {
                    "student_course": (
                        "Results have already been published."
                    )
                }
            )

    @staticmethod
    def _validate_marks(
        marks: Decimal,
    ):
        """
        Validate marks.
        """

        if marks < 0 or marks > 100:
            raise ValidationError(
                {
                    "marks": (
                        "Marks must be between 0 and 100."
                    )
                }
            )

    @staticmethod
    def _update_student_course(
        student_course: StudentCourse,
        marks: Decimal,
        grade: Grade,
    ):
        """
        Update the student course with the published result.
        """

        student_course.marks = marks
        student_course.grade = grade

        if grade == Grade.F:
            student_course.status = (
                CourseStatus.FAILED
            )
        else:
            student_course.status = (
                CourseStatus.PASSED
            )

        student_course.full_clean()
        student_course.save()