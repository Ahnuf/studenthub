from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)

from core.models import TimeStampedModel

from apps.academic.models.grading_scheme import GradingScheme
from apps.academic.models.enums import Grade
from django.core.exceptions import ValidationError

# other imports...


class GradePoint(TimeStampedModel):
    """
    Maps a grade to grade points and mark ranges.
    """

    grading_scheme = models.ForeignKey(
        GradingScheme,
        on_delete=models.CASCADE,
        related_name="grade_points",
    )

    grade = models.CharField(
        max_length=2,
        choices=Grade.choices,
    )

    grade_points = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4),
        ],
    )

    minimum_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    maximum_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    class Meta:
        ordering = ("-grade_points",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "grading_scheme",
                    "grade",
                ],
                name="unique_grade_per_scheme",
            )
        ]

        verbose_name = "Grade Point"
        verbose_name_plural = "Grade Points"

    def clean(self):
        """
        Validate the grade point configuration.
        """

        self._validate_mark_range()
        self._validate_overlapping_ranges()

    def _validate_mark_range(self):
        """
        Ensure minimum marks are not greater than maximum marks.
        """

        if self.minimum_marks > self.maximum_marks:
            raise ValidationError(
                {
                    "minimum_marks": (
                        "Minimum marks cannot be greater than maximum marks."
                    )
                }
            )

    def _validate_overlapping_ranges(self):
        """
        Ensure mark ranges do not overlap within the same grading scheme.
        """

        overlapping = (
            GradePoint.objects.filter(
                grading_scheme=self.grading_scheme,
            )
            .exclude(
                pk=self.pk,
            )
            .filter(
                minimum_marks__lte=self.maximum_marks,
                maximum_marks__gte=self.minimum_marks,
            )
        )

        if overlapping.exists():
            raise ValidationError(
                {
                    "minimum_marks": (
                        "Mark ranges cannot overlap within the same grading scheme."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.grading_scheme.name} - "
            f"{self.grade} ({self.grade_points})"
        )