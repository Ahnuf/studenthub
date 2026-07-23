from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.timetable.models import TimetableEntry
from apps.timetable.selectors.timetable_selector import TimetableSelector


class TimetableService:
    """
    Business logic for timetable entry operations.
    """

    @staticmethod
    @transaction.atomic
    def create_entry(user, **validated_data) -> TimetableEntry:
        """
        Create a new timetable entry owned by the given user.

        Overlapping entries are allowed -- callers should check
        get_conflicts() afterwards to surface a warning, not to
        block the save.
        """

        entry = TimetableEntry(
            user=user,
            **validated_data,
        )

        try:
            entry.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        entry.save()

        return entry

    @staticmethod
    @transaction.atomic
    def update_entry(entry: TimetableEntry, **validated_data) -> TimetableEntry:
        """
        Update an existing timetable entry.

        `user` is never accepted in validated_data -- ownership
        can never change via this method.
        """

        validated_data.pop("user", None)

        for field, value in validated_data.items():
            setattr(entry, field, value)

        try:
            entry.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        entry.save()

        return entry

    @staticmethod
    @transaction.atomic
    def delete_entry(entry: TimetableEntry) -> None:
        """
        Delete a timetable entry.
        """

        entry.delete()

    @staticmethod
    def get_conflicts(entry: TimetableEntry) -> list[TimetableEntry]:
        """
        Return any other entries belonging to the same user that
        overlap this entry's day/time range. Purely informational
        -- never raised as an error, never blocks a save.
        """

        return list(
            TimetableSelector.find_conflicts(
                user=entry.user,
                day_of_week=entry.day_of_week,
                start_time=entry.start_time,
                end_time=entry.end_time,
                exclude_id=entry.pk,
            )
        )