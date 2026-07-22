from apps.academic.models import ProgramCourse


class ProgramSelector:
    """
    Read-only operations related to a program's official curriculum.
    """

    @staticmethod
    def list_program_courses(program):
        """
        Return all active ProgramCourse rows for a program.
        """

        return (
            ProgramCourse.objects
            .select_related(
                "course",
            )
            .filter(
                program=program,
                is_active=True,
            )
        )

    @staticmethod
    def get_total_credit_hours(program) -> int:
        """
        Return the total credit hours required to complete the program,
        derived from the program's active ProgramCourse rows.
        """

        return sum(
            program_course.total_credit_hours
            for program_course in ProgramSelector.list_program_courses(program)
        )

    @staticmethod
    def get_total_course_count(program) -> int:
        """
        Return the total number of active courses required by the program.
        """

        return ProgramSelector.list_program_courses(program).count()