from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from core.models import TimeStampedModel
from apps.academic.models import AcademicSession, Program, University, ProgramCourse



class AcademicStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    ON_BREAK = "ON_BREAK", "On Break"
    GRADUATED = "GRADUATED", "Graduated"
    DROPPED = "DROPPED", "Dropped"


class StudentProfile(TimeStampedModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT,
        related_name="students",
    )

    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="students",
    )

    joined_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="students",
    )

    current_semester = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ]
    )

    registration_number = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    roll_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    expected_graduation_date = models.DateField(
        # validators=[
        #     MinValueValidator(2000),
        #     MaxValueValidator(2100),
        # ]
    )

    academic_status = models.CharField(
        max_length=20,
        choices=AcademicStatus.choices,
        default=AcademicStatus.ACTIVE,
    )

    class Meta:
        ordering = [
            "university",
            "program",
            "user",
        ]       

        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

    def clean(self):

        if self.program.university != self.university:
            raise ValidationError(
                "Selected program does not belong to the selected university."
            )

        if self.joined_session.university != self.university:
            raise ValidationError(
                "Selected academic session does not belong to the selected university."
            )
            
        @property
        def profile_completion_percentage(self):

            score = 0

            if self.university:
                score += 20

            if self.program:
                score += 20

            if self.joined_session:
                score += 20

            if self.current_semester:
                score += 20

            if self.registration_number or self.roll_number:
                score += 20

            return score

    def __str__(self):
        return (
            f"{self.user.get_full_name() or self.user.username}"
            f" - "
            f"{self.program}"
        )


class CourseStatus(models.TextChoices):
    ENROLLED = "ENROLLED", "Enrolled"
    PASSED = "PASSED", "Passed"
    FAILED = "FAILED", "Failed"
    WITHDRAWN = "WITHDRAWN", "Withdrawn"
    INCOMPLETE = "INCOMPLETE", "Incomplete"

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


class StudentCourse(TimeStampedModel):
    """
    Represents a single attempt of a student taking a course.
    """

    student_profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="student_courses",
    )

    program_course = models.ForeignKey(
        ProgramCourse,
        on_delete=models.PROTECT,
        related_name="student_courses",
    )

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="student_courses",
    )

    semester_taken = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ]
    )

    attempt_number = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )

    status = models.CharField(
        max_length=20,
        choices=CourseStatus.choices,
        default=CourseStatus.ENROLLED,
    )

    grade = models.CharField(
        max_length=2,
        choices=Grade.choices,
        blank=True,
        null=True,
    )

    marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
        MinValueValidator(0),
        MaxValueValidator(100),],
        blank=True,
        null=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "-academic_session",
            "semester_taken",
        ]

    constraints = [
    models.UniqueConstraint(
    fields=[
        "student_profile",
        "program_course",
        "attempt_number",
    ],
    name="unique_student_course_attempt",
    )
    ]

    verbose_name = "Student Course"
    verbose_name_plural = "Student Courses"

    def clean(self):
        self.validate_program_course()
        self.validate_academic_session()
        self.validate_grade_status()

#   Validate Program
    def validate_program_course(self):
        if self.program_course.program != self.student_profile.program:
            raise ValidationError(
            "The selected course does not belong to the student's program."
            )

#   Validate Academic Session
    def validate_academic_session(self):
        if (self.academic_session.university != self.student_profile.university):
            raise ValidationError(
            "The selected academic session does not belong to the student's university."
            )

#   Validate Grade & Status
    def validate_grade_status(self):
        if (self.status == CourseStatus.ENROLLED and self.grade is not None):
            raise ValidationError(
                "An enrolled course cannot have a final grade."
            )

        if (self.status == CourseStatus.PASSED and self.grade is None):
            raise ValidationError(
                "A passed course must have a grade."
            )

        if (self.status == CourseStatus.FAILED and self.grade is None):
            raise ValidationError(
                "A failed course must have a grade."
            )

    def __str__(self):
        return (
        f"{self.student_profile.user} - "
        f"{self.program_course.course_code}"
        )