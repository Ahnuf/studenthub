from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models import TimeStampedModel
from apps.timetable.timetable_enums import DayOfWeek


class TimetableEntry(TimeStampedModel):
    """
    A student's personal weekly class schedule entry.

    Recurring weekly slot, not tied to a specific date. No link to
    the academic catalog, Sections, or instructors -- this is a
    personal reference tool only, set up entirely at the student's
    own discretion.

    Note: overlapping entries are intentionally allowed. Scheduling
    conflicts are surfaced as a non-blocking warning at the
    service/view layer (see TimetableService.get_conflicts), not
    enforced as a hard model invariant -- a student may genuinely
    want to log two overlapping things (e.g. an optional session
    they might skip).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="timetable_entries",
    )

    course_name = models.CharField(
        max_length=150,
    )

    day_of_week = models.PositiveSmallIntegerField(
        choices=DayOfWeek.choices,
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    location = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        ordering = ["day_of_week", "start_time"]
        verbose_name = "Timetable Entry"
        verbose_name_plural = "Timetable Entries"

    def clean(self):
        """
        Only hard invariants live here. Overlap is a soft warning,
        handled separately -- see module docstring.
        """

        if self.end_time <= self.start_time:
            raise ValidationError(
                {
                    "end_time": (
                        "End time must be after start time."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.user} - {self.course_name} - "
            f"{self.get_day_of_week_display()} "
            f"{self.start_time.strftime('%H:%M')}"
        )