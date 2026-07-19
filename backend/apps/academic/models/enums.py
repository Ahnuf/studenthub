from django.db import models
from core.models import TimeStampedModel
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator



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

class CourseCategory(models.TextChoices):
    CORE = "CORE", "Core"
    ELECTIVE = "ELECTIVE", "Elective"
    UNIVERSITY_REQUIREMENT = "UNIVERSITY_REQUIREMENT", "University Requirement"
    GENERAL = "GENERAL", "General Education"

class SessionTerm(models.TextChoices):
    SPRING = "SPRING", "Spring"
    SUMMER = "SUMMER", "Summer"
    FALL = "FALL", "Fall"
    WINTER = "WINTER", "Winter"

class RepeatPolicy(models.TextChoices):
    """
    Defines how repeated courses affect GPA calculations.
    """

    LATEST_ATTEMPT = (
        "LATEST_ATTEMPT",
        "Latest Attempt",
    )

    HIGHEST_GRADE = (
        "HIGHEST_GRADE",
        "Highest Grade",
    )

    ALL_ATTEMPTS = (
        "ALL_ATTEMPTS",
        "All Attempts",
    )


class Grade(models.TextChoices):
    A_PLUS = "A+", "A+"
    A = "A", "A"
    A_MINUS = "A-", "A-"
    B_PLUS = "B+", "B+"
    B = "B", "B"
    B_MINUS = "B-", "B-"
    C_PLUS = "C+", "C+"
    C = "C", "C"
    C_MINUS = "C-", "C-"
    D_PLUS = "D+", "D+"
    D = "D", "D"
    F = "F", "F"