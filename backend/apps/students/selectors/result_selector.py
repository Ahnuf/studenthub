from apps.students.models import StudentCourse


class ResultSelector:
    """
    Read-only operations related to student results.
    """

    @staticmethod
    def get_student_course(
        student_course_id: int,
    ) -> StudentCourse | None:
        """
        Retrieve a StudentCourse by its ID.
        """

        return (
            StudentCourse.objects
            .select_related(
                "enrollment",
                "enrollment__student",
                "program_course",
                "program_course__course",
            )
            .filter(
                id=student_course_id,
            )
            .first()
        )