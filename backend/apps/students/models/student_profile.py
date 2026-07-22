from django.db import models
from apps.students.enums import AcademicStatus
from django.core.exceptions import ValidationError
from apps.academic.models import (
    AcademicSession,
    Program,
    University,
)
from core.models import TimeStampedModel
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator




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