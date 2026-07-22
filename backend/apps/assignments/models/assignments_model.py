from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from apps.assignments.models.assignments_enums import AssignmentStatus


class Assignment(TimeStampedModel):
    """
    A student's personal record of an assignment/deadline.

    This is a personal productivity record, not a submission or
    grading system. It has no link to the academic catalog and is
    not tied to official coursework platforms.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    course_name = models.CharField(
        max_length=150,
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=AssignmentStatus.choices,
        default=AssignmentStatus.PENDING,
    )

    class Meta:
        ordering = ["due_date"]
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"

    def __str__(self):
        return f"{self.user} - {self.course_name} - {self.title}"
