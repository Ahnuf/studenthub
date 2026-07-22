from apps.students.enums import (
    AcademicStatus,
    EnrollmentStatus,
)
from .student_profile import StudentProfile
from apps.academic.models import AcademicSession
from core.models import TimeStampedModel
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator




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