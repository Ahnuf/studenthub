from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel
from apps.students.models import StudentCourse


class AttendanceStatus(models.TextChoices):
    PRESENT = "PRESENT", "Present"
    ABSENT = "ABSENT", "Absent"
    LEAVE = "LEAVE", "Leave"


class AttendanceRecord(TimeStampedModel):
    """
    A single day's attendance for a student in a specific course
    enrollment (StudentCourse), not the raw catalog ProgramCourse --
    this ties attendance to a specific semester's enrollment, so a
    retake in a later semester gets its own independent record.

    Marked by a teacher/admin (see apps.common.permissions), never
    self-reported by the student.
    """

    student_course = models.ForeignKey(
        StudentCourse,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT,
    )

    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="attendance_marked",
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["student_course", "date"],
                name="unique_attendance_per_student_course_per_day",
            )
        ]
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"

    def clean(self):
        if self.date and self.date > timezone.localdate():
            raise ValidationError(
                {
                    "date": (
                        "Attendance cannot be marked for a future date."
                    )
                }
            )

    def __str__(self):
        return (
            f"{self.student_course} - {self.date} - "
            f"{self.get_status_display()}"
        )