from django.db.models import QuerySet
# from apps.academic.exceptions import (
#     GradePointNotFound,
#     GradingSchemeNotFound,
# )
from apps.academic.models import (
    GradePoint,
    GradingScheme,
)
from apps.students.models import StudentProfile


class GradingSelector:
    """
    Read-only database queries related to grading.

    This selector is responsible for retrieving grading schemes
    and grade points from the database. It does not contain any
    business logic.
    """

    @staticmethod
    def get_active_scheme(
        student: StudentProfile,
    ) -> GradingScheme:
        """
        Return the active grading scheme for the student's university.
        """

        try:
            return (
                GradingScheme.objects.select_related(
                    "university",
                )
                .get(
                    university=student.program.university,
                    is_active=True,
                )
            )

        except GradingScheme.DoesNotExist as exc:
            raise GradingSchemeNotFound(
                "No active grading scheme found for the student's university."
            ) from exc

    @staticmethod
    def get_grade_point(
        grading_scheme: GradingScheme,
        marks: float,
    ) -> GradePoint:
        """
        Return the GradePoint matching the given marks.
        """

        try:
            return (
                GradePoint.objects.get(
                    grading_scheme=grading_scheme,
                    minimum_marks__lte=marks,
                    maximum_marks__gte=marks,
                )
            )

        except GradePoint.DoesNotExist as exc:
            raise GradePointNotFound(
                f"No grade point found for marks: {marks}."
            ) from exc

    @staticmethod
    def get_grade_points(
        grading_scheme: GradingScheme,
    ) -> QuerySet[GradePoint]:
        """
        Return all grade points belonging to a grading scheme.
        """

        return (
            GradePoint.objects.filter(
                grading_scheme=grading_scheme,
            )
            .order_by(
                "-minimum_marks",
            )
        )