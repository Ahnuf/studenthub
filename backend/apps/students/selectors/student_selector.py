from django.contrib.auth import get_user_model

from apps.students.models import StudentProfile


User = get_user_model()


class StudentSelector:
    """
    Read-only operations for student-related data.
    """

    @staticmethod
    def get_profile(user: User) -> StudentProfile | None:
        """
        Returns the student's profile if it exists.
        """

        return (
            StudentProfile.objects
            .select_related(
                "university",
                "program",
                "joined_session",
            )
            .filter(user=user)
            .first()
        )

    @staticmethod
    def profile_exists(user: User) -> bool:
        """
        Returns True if the user already has a student profile.
        """

        return StudentProfile.objects.filter(user=user).exists()

    @staticmethod
    def get_profile_or_raise(user: User) -> StudentProfile:
        """
        Returns the student's profile or raises DoesNotExist.
        """

        return StudentProfile.objects.select_related(
            "university",
            "program",
            "joined_session",
        ).get(user=user)