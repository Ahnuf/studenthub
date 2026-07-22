from datetime import timedelta

from django.utils import timezone

from apps.assignments.models import Assignment, AssignmentStatus


class AssignmentSelector:
    """
    Read-only operations for assignments.

    Every method here is scoped to a specific user. There is no
    method that returns an assignment without a user filter --
    this is intentional, to prevent one student's assignment from
    ever being reachable by another student, even by guessing IDs.
    """

    @staticmethod
    def list_assignments(user):
        """
        Return all assignments belonging to the user, ordered by
        due date.
        """

        return (
            Assignment.objects
            .filter(user=user)
        )

    @staticmethod
    def list_upcoming(user, days: int = 7):
        """
        Return the user's assignments due within the next `days`
        days, excluding completed ones. Intended for future
        dashboard widget use.
        """

        today = timezone.localdate()
        end_date = today + timedelta(days=days)

        return (
            Assignment.objects
            .filter(
                user=user,
                due_date__gte=today,
                due_date__lte=end_date,
            )
            .exclude(
                status=AssignmentStatus.COMPLETED,
            )
        )

    @staticmethod
    def list_overdue(user):
        """
        Return the user's assignments past due date that are not
        completed. Intended for future dashboard widget use.
        """

        today = timezone.localdate()

        return (
            Assignment.objects
            .filter(
                user=user,
                due_date__lt=today,
            )
            .exclude(
                status=AssignmentStatus.COMPLETED,
            )
        )

    @staticmethod
    def get_assignment(user, assignment_id: int):
        """
        Return a single assignment scoped to the requesting user,
        or None if it doesn't exist or belongs to someone else.
        Callers must treat None as "not found" (404), never as a
        permission error -- this avoids confirming that the ID
        exists at all.
        """

        return (
            Assignment.objects
            .filter(
                user=user,
                id=assignment_id,
            )
            .first()
        )
