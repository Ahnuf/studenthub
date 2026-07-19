from django.db import models
from core.models import TimeStampedModel
from django.core.exceptions import ValidationError
from .program import Program
from .course import Course
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from apps.academic.models.enums import (
    DegreeType,
    StudySystem,
    CourseCategory,
    SessionTerm,
    RepeatPolicy,
)



class ProgramCourse(TimeStampedModel):
    """
    Represents how a specific program offers a specific course.

    Stores all university/program-specific information such as
    course code, credit hours and recommended semester.
    """

    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="program_courses",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="program_courses",
    )

    course_code_validator = RegexValidator(
    regex=r"^[A-Za-z]{2,6}-?\d{2,4}[A-Za-z]?$",
    message=(
        "Course code must look like "
        "CS101, CSC-201, MTH101, SE301 etc."
        ),
    )

    course_code = models.CharField(
        max_length=20,
        validators=[
            course_code_validator,
        ],
    )

    recommended_semester = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
    )

    theory_credit_hours = models.PositiveSmallIntegerField(
        validators=[
        MinValueValidator(0),
        MaxValueValidator(6),
    ]
    )

    lab_credit_hours = models.PositiveSmallIntegerField(
        default=0,
        validators=[
        MinValueValidator(0),
        MaxValueValidator(3),
    ]
    )

    category = models.CharField(
        max_length=24,
        choices=CourseCategory.choices,
        default=CourseCategory.CORE,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "program",
            "recommended_semester",
            "course_code",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["program", "course"],
                name="unique_course_per_program",
            ),
            models.UniqueConstraint(
                fields=["program", "course_code"],
                name="unique_course_code_per_program",
            ),
        ]

        verbose_name = "Program Course"
        verbose_name_plural = "Program Courses"

    @property
    def total_credit_hours(self):
        return self.theory_credit_hours + self.lab_credit_hours

    def __str__(self):
        return (
            f"{self.program} | "
            f"{self.course_code} - "
            f"{self.course.title}"
        )