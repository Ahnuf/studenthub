from django.db import models
from core.models import TimeStampedModel
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


class Course(TimeStampedModel):
    """
    Represents an academic course/subject.

    This model stores only the generic course information.
    University-specific information such as course code,
    credit hours, and recommended semester is stored
    in ProgramCourse.
    """

    title = models.CharField(
        max_length=200,
        unique=True,
    )

    short_title = models.CharField(
    max_length=10,
    blank = True, 
    null = True, 
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title