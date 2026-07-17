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


class EnrollmentStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"

class Enrollment(TimeStampedModel):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    academic_session = models.ForeignKey(
        AcademicSession,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    semester = models.PositiveSmallIntegerField(
        validators=[
        MinValueValidator(1),
        MaxValueValidator(12),
    ]
    )

    status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.DRAFT,
    )

    total_credit_hours = models.PositiveSmallIntegerField(
        default=0,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "academic_session",
                ],
                name="unique_student_enrollment_per_session",
            )
        ]

    from django.core.exceptions import ValidationError


    def clean(self):
        errors = {}

        # Rule 1
        if (
            self.student.university_id
            != self.academic_session.university_id
        ):
            errors["academic_session"] = (
                "Selected academic session does not belong "
                "to the student's university."
            )

        # Rule 2
        if self.semester != self.student.current_semester:
            errors["semester"] = (
                "Enrollment semester must match the student's current semester."
            )

        # Rule 3
        if self.student.academic_status != AcademicStatus.ACTIVE:
            errors["student"] = (
                "Only active students can enroll."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return (
            f"{self.student.user.get_full_name()} - "
            f"{self.academic_session.display_name}"
        )


class StudentCourse(TimeStampedModel):
    """
    Represents a single attempt of a student taking a course
    within a specific enrollment.
    """

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="student_courses",
    )

    program_course = models.ForeignKey(
        ProgramCourse,
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
            MaxValueValidator(100),
        ],
        blank=True,
        null=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "enrollment",
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
        self.validate_grade_status()

    def validate_program_course(self):
        """
        Ensure the selected ProgramCourse belongs to the
        student's enrolled program.
        """
        if (
            self.program_course.program
            != self.enrollment.student.program
        ):
            raise ValidationError(
                {
                    "program_course": (
                        "The selected course does not belong "
                        "to the student's program."
                    )
                }
            )

    def validate_grade_status(self):
        """
        Validate consistency between course status and grade.
        """

        if (
            self.status == CourseStatus.ENROLLED
            and self.grade is not None
        ):
            raise ValidationError(
                {
                    "grade": (
                        "An enrolled course cannot have a final grade."
                    )
                }
            )

        if (
            self.status == CourseStatus.PASSED
            and self.grade is None
        ):
            raise ValidationError(
                {
                    "grade": (
                        "A passed course must have a grade."
                    )
                }
            )

        if self.semester_taken != self.enrollment.semester:
            raise ValidationError(
                {
                    "semester_taken": (
                        "Semester taken must match the enrollment semester."
                    )
                }
            )

        if (
            self.status == CourseStatus.FAILED
            and self.grade is None
        ):
            raise ValidationError(
                {
                    "grade": (
                        "A failed course must have a grade."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.enrollment.student.user.get_full_name()} - "
            f"{self.program_course.course.course_code}"
        )