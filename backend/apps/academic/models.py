from django.db import models
from core.models import TimeStampedModel



class University(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    short_name = models.CharField(
        max_length=20,
        unique=True,
    )

    country = models.CharField(
        max_length=100,
        default="Pakistan",
    )

    province = models.CharField(
        max_length=100,
        default = "Punjab",
    )

    city = models.CharField(
        max_length=100,
    )

    website = models.URLField(
        blank=True,
    )

    # Will add this later on. 

    # logo = models.ImageField(
    #     upload_to="universities/logos/",
    #     blank=True,
    #     null=True,
    # )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "University"
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.short_name


class DegreeType(models.TextChoices):
    BS = "BS", "Bachelor of Science"
    BBA = "BBA", "Bachelor of Business Administration"
    MBA = "MBA", "Master of Business Administration"
    MS = "MS", "Master of Science"
    PHD = "PHD", "Doctor of Philosophy"


class StudySystem(models.TextChoices):
    SEMESTER = "SEMESTER", "Semester"
    TRIMESTER = "TRIMESTER", "Trimester"
    ANNUAL = "ANNUAL", "Annual"


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