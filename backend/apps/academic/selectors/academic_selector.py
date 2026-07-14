from apps.academic.models import (
    AcademicSession,
    Program,
    University,
)


class AcademicSelector:
    """
    Read-only operations for academic lookup data.
    """

    @staticmethod
    def list_universities():
        return (
            University.objects
            .all()
            .order_by("name")
        )

    @staticmethod
    def list_programs(university_id=None):
        queryset = (
            Program.objects
            .select_related("university")
            .order_by("program_name")
        )

        if university_id:
            queryset = queryset.filter(
                university_id=university_id
            )

        return queryset

    @staticmethod
    def list_sessions(university_id=None):
        queryset = (
            AcademicSession.objects
            .select_related("university")
            .order_by("-start_date")
        )

        if university_id:
            queryset = queryset.filter(
                university_id=university_id
            )

        return queryset