from django.db import models
from core.models import TimeStampedModel
from django.core.exceptions import ValidationError
from .university import University
# from .program_course import ProgramCourse
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from apps.academic.models.enums import (
    DegreeType,
    StudySystem,
    CourseCategory,
    SessionTerm,
    RepeatPolicy,
)



class Program(TimeStampedModel):
    """
    Represents an academic program offered by a university.
    Example:
        FAST -> BS Computer Science
    """

    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT,
        related_name="programs",
    )

    degree_type = models.CharField(
        max_length=10,
        choices=DegreeType.choices,
    )

    program_name = models.CharField(
        max_length=150,
    )

    duration_years = models.PositiveSmallIntegerField(
        default=4,
    )

    study_system = models.CharField(
        max_length=20,
        choices=StudySystem.choices,
        default=StudySystem.SEMESTER,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "university",
            "degree_type",
            "program_name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["university", "degree_type", "program_name"],
                name="unique_program_per_university",
            )
        ]

        verbose_name = "Program"
        verbose_name_plural = "Programs"

    def __str__(self):
        return f"{self.university.short_name} - {self.degree_type} {self.program_name}"