from apps.timetable.models import TimetableEntry


class TimetableSelector:
    """
    Read-only operations for timetable entries.

    Every method is scoped to a specific user -- there is no
    method that returns an entry without a user filter, so one
    student's schedule can never be reached by another via ID.
    """

    @staticmethod
    def list_entries(user):
        """
        Return all of the user's timetable entries, ordered by
        day of week then start time.
        """

        return (
            TimetableEntry.objects
            .filter(user=user)
        )

    @staticmethod
    def list_for_day(user, day_of_week: int):
        """
        Return the user's entries for a single day of the week.
        """

        return (
            TimetableEntry.objects
            .filter(
                user=user,
                day_of_week=day_of_week,
            )
        )

    @staticmethod
    def get_entry(user, entry_id: int):
        """
        Return a single entry scoped to the requesting user, or
        None if it doesn't exist or belongs to someone else.
        Callers must treat None as "not found" (404).
        """

        return (
            TimetableEntry.objects
            .filter(
                user=user,
                id=entry_id,
            )
            .first()
        )

    @staticmethod
    def find_conflicts(
        user,
        day_of_week: int,
        start_time,
        end_time,
        exclude_id: int | None = None,
    ):
        """
        Return other entries for this user that overlap the given
        day/time range. Used to build a non-blocking warning --
        this never prevents a save, it only informs the student.
        """

        queryset = (
            TimetableEntry.objects
            .filter(
                user=user,
                day_of_week=day_of_week,
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
        )

        if exclude_id is not None:
            queryset = queryset.exclude(pk=exclude_id)

        return queryset