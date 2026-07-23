from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.attendance.models import AttendanceRecord
from apps.students.models import StudentCourse


class AttendanceService:
    """
    Business logic for marking attendance.
    """

    @staticmethod
    @transaction.atomic
    def mark_attendance(
        student_course: StudentCourse,
        date,
        status: str,
        marked_by,
        remarks: str = "",
    ) -> AttendanceRecord:
        """
        Create or update the attendance record for this student's
        course on this date. Re-marking a day (e.g. correcting a
        mistake) overwrites rather than erroring -- there's only
        ever one true record per student-course-per-day.
        """

        record = _get_or_new_record(student_course, date)

        record.status = status
        record.marked_by = marked_by
        record.remarks = remarks

        try:
            record.full_clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)

        record.save()

        return record

    @staticmethod
    @transaction.atomic
    def bulk_mark_attendance(
        entries: list[dict],
        date,
        marked_by,
    ) -> list[AttendanceRecord]:
        """
        Mark attendance for many students at once (a single class
        session). Each entry is
        {"student_course": StudentCourse, "status": AttendanceStatus}.

        Runs as one transaction -- if any entry is invalid, none of
        the session's attendance is partially saved.
        """

        return [
            AttendanceService.mark_attendance(
                student_course=entry["student_course"],
                date=date,
                status=entry["status"],
                marked_by=marked_by,
            )
            for entry in entries
        ]


def _get_or_new_record(student_course, date) -> AttendanceRecord:
    """
    Internal helper: fetch the existing record for this day, or
    build an unsaved one. Kept out of the selector on purpose --
    selectors are read-only by convention in this codebase, and
    this returns an object meant to be mutated and saved.
    """

    existing = AttendanceRecord.objects.filter(
        student_course=student_course,
        date=date,
    ).first()

    if existing is not None:
        return existing

    return AttendanceRecord(student_course=student_course, date=date)