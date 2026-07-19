from django.db import models
from core.models import TimeStampedModel
from .university import University
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from apps.academic.models.enums import (
    DegreeType,
    StudySystem,
    CourseCategory,
    SessionTerm,
    RepeatPolicy,
)



class AcademicSession(TimeStampedModel):
    """
    Represents an academic session for a university.

    Example:
        FAST - Fall 2026
    """

    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT,
        related_name="academic_sessions",
    )

    term = models.CharField(
        max_length=10,
        choices=SessionTerm.choices,
    )

    year = models.PositiveSmallIntegerField(
        validators=[
        MinValueValidator(2000),
        MaxValueValidator(2100),
    ]
    )

    start_date = models.DateField()

    end_date = models.DateField()

    is_current = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "-year",
            "term",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["university", "term", "year"],
                name="unique_session_per_university",
            )
        ]

        verbose_name = "Academic Session"
        verbose_name_plural = "Academic Sessions"

    def clean(self):
        """
        Validate academic session.
        """

        if self.end_date <= self.start_date:
            raise ValidationError(
                "End date must be after the start date."
            )

        if self.is_current:
            existing = AcademicSession.objects.filter(
                university=self.university,
                is_current=True,
            ).exclude(pk=self.pk)

            if existing.exists():
                raise ValidationError(
                    "Only one current academic session is allowed per university."
                )

    def __str__(self):
        return (
            f"{self.university.short_name} - "
            f"{self.get_term_display()} {self.year}"
        )

    @property
    def display_name(self):
        return f"{self.get_term_display()} {self.year}"