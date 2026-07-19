from apps.students.enums import CourseStatus
from apps.academic.models.enums import Grade
from .enrollment import Enrollment
from apps.academic.models import ProgramCourse
from core.models import TimeStampedModel
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



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
            f"{self.program_course.course_code}"
        )