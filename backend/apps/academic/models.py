from django.db import models
from core.models import TimeStampedModel
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator



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

class CourseCategory(models.TextChoices):
    CORE = "CORE", "Core"
    ELECTIVE = "ELECTIVE", "Elective"
    UNIVERSITY_REQUIREMENT = "UNIVERSITY_REQUIREMENT", "University Requirement"
    GENERAL = "GENERAL", "General Education"


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


class SessionTerm(models.TextChoices):
    SPRING = "SPRING", "Spring"
    SUMMER = "SUMMER", "Summer"
    FALL = "FALL", "Fall"
    WINTER = "WINTER", "Winter"


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


