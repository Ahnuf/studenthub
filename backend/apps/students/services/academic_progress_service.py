from datetime import date
from decimal import Decimal

from apps.students.models import StudentProfile
from apps.students.models.student_course import CourseStatus
from apps.students.selectors.enrollment_selector import EnrollmentSelector
from apps.students.selectors.transcript_selector import TranscriptSelector
from apps.academic.selectors.program_selector import ProgramSelector
from apps.academic.services.grading_service import GradingService
from apps.assignments.selectors.assignments_selector import AssignmentSelector
from apps.timetable.selectors.timetable_selector import TimetableSelector
from apps.notes.selectors.notes_selector import NoteSelector
from apps.flashcards.selectors.flashcard_selector import FlashcardSelector
from apps.QA.selectors.QA_selector import QASelector
from apps.attendance.selectors.attendance_selector import AttendanceSelector


class AcademicProgressService:
    """
    Builds the Academic Progress Dashboard for a student.

    This service is intentionally the one place in the codebase
    that fans out across almost every app (assignments, timetable,
    notes, flashcards, QA, attendance) -- that's expected here,
    since its entire job is aggregation. Every other service in
    the project should stay narrowly scoped; this one is the
    exception by design.

    Design principles (docs/04-academic-progress-dashboard.md):
    - Never store calculated data; everything here is derived live.
    - The academic catalog (ProgramCourse) is the source of truth
      for what a program requires.
    - GPA figures are resolved through GradingService.
    """

    @staticmethod
    def build_dashboard(student: StudentProfile) -> dict:
        student_courses = list(
            TranscriptSelector.list_student_courses(student)
        )

        current_enrollment = EnrollmentSelector.get_current_enrollment(student)

        current_student_courses = (
            list(current_enrollment.student_courses.all())
            if current_enrollment is not None
            else []
        )

        current_course_ids = [
            sc.program_course.course_id
            for sc in current_student_courses
        ]

        return {
            "academic_identity": (
                AcademicProgressService._build_academic_identity(student)
            ),
            "current_semester": (
                AcademicProgressService._build_current_semester(student)
            ),
            "degree_progress": (
                AcademicProgressService._build_degree_progress(
                    student=student,
                    student_courses=student_courses,
                )
            ),
            "performance": (
                AcademicProgressService._build_performance(
                    student=student,
                    student_courses=student_courses,
                )
            ),
            "assignments_due_soon": (
                AcademicProgressService._build_assignments_summary(student)
            ),
            "timetable_today": (
                AcademicProgressService._build_timetable_today(student)
            ),
            "recent_notes": (
                AcademicProgressService._build_recent_notes(current_course_ids)
            ),
            "flashcards": (
                AcademicProgressService._build_flashcards_summary(
                    student=student,
                    course_ids=current_course_ids,
                )
            ),
            "qa_activity": (
                AcademicProgressService._build_qa_activity(student)
            ),
            "attendance": (
                AcademicProgressService._build_attendance_summary(
                    current_student_courses
                )
            ),
        }

    @staticmethod
    def _build_academic_identity(student: StudentProfile) -> dict:
        return {
            "university": student.university.name,
            "program": student.program.program_name,
            "current_semester": student.current_semester,
            "joined_session": student.joined_session.display_name,
            "academic_status": student.academic_status,
            "expected_graduation_date": student.expected_graduation_date,
        }

    @staticmethod
    def _build_current_semester(student: StudentProfile) -> dict:
        enrollment = EnrollmentSelector.get_current_enrollment(student)

        if enrollment is None:
            return {
                "current_courses": [],
                "current_credit_hours": 0,
                "semester_gpa": Decimal("0.00"),
            }

        current_courses = list(enrollment.student_courses.all())

        current_credit_hours = sum(
            student_course.program_course.total_credit_hours
            for student_course in current_courses
        )

        semester_gpa = GradingService.calculate_gpa(
            student=student,
            student_courses=current_courses,
        )

        return {
            "current_courses": current_courses,
            "current_credit_hours": current_credit_hours,
            "semester_gpa": semester_gpa,
        }

    @staticmethod
    def _build_degree_progress(student: StudentProfile, student_courses) -> dict:
        total_credit_hours = ProgramSelector.get_total_credit_hours(student.program)
        total_course_count = ProgramSelector.get_total_course_count(student.program)

        passed_courses = [
            sc for sc in student_courses
            if sc.status == CourseStatus.PASSED
        ]

        completed_credit_hours = sum(
            sc.program_course.total_credit_hours for sc in passed_courses
        )

        completed_course_ids = {sc.program_course_id for sc in passed_courses}
        completed_course_count = len(completed_course_ids)

        remaining_credit_hours = max(total_credit_hours - completed_credit_hours, 0)
        remaining_course_count = max(total_course_count - completed_course_count, 0)

        if total_credit_hours == 0:
            progress_percentage = Decimal("0.00")
        else:
            progress_percentage = (
                Decimal(completed_credit_hours)
                / Decimal(total_credit_hours)
                * Decimal("100")
            ).quantize(Decimal("0.01"))

        return {
            "completed_credit_hours": completed_credit_hours,
            "remaining_credit_hours": remaining_credit_hours,
            "completed_courses": completed_course_count,
            "remaining_courses": remaining_course_count,
            "total_program_credit_hours": total_credit_hours,
            "total_program_courses": total_course_count,
            "progress_percentage": progress_percentage,
        }

    @staticmethod
    def _build_performance(student: StudentProfile, student_courses) -> dict:
        cgpa = GradingService.calculate_gpa(
            student=student,
            student_courses=student_courses,
        )
        return {"cgpa": cgpa}

    @staticmethod
    def _build_assignments_summary(student: StudentProfile) -> dict:
        upcoming = list(
            AssignmentSelector.list_upcoming(user=student.user, days=7)
        )
        overdue = list(
            AssignmentSelector.list_overdue(user=student.user)
        )
        return {"upcoming": upcoming, "overdue": overdue}

    @staticmethod
    def _build_timetable_today(student: StudentProfile) -> list:
        """
        Python's date.weekday() returns 0=Monday..6=Sunday, which
        matches TimetableEntry's DayOfWeek.IntegerChoices exactly.
        """

        today_weekday = date.today().weekday()

        return list(
            TimetableSelector.list_for_day(student.user, today_weekday)
        )

    @staticmethod
    def _build_recent_notes(course_ids: list) -> list:
        return list(
            NoteSelector.list_recent_for_courses(course_ids, limit=5)
        )

    @staticmethod
    def _build_flashcards_summary(student: StudentProfile, course_ids: list) -> dict:
        available_decks = FlashcardSelector.count_decks_for_courses(course_ids)
        progress = FlashcardSelector.get_progress_summary(student.user)

        return {
            "available_decks": available_decks,
            "cards_reviewed": progress["cards_reviewed"],
            "cards_known": progress["cards_known"],
        }

    @staticmethod
    def _build_qa_activity(student: StudentProfile) -> dict:
        return {
            "my_questions": list(
                QASelector.list_my_questions(student.user, limit=5)
            ),
            "my_answers": list(
                QASelector.list_my_answers(student.user, limit=5)
            ),
        }

    @staticmethod
    def _build_attendance_summary(current_student_courses: list) -> dict:
        """
        Attendance rows are teacher/admin-marked (authoritative),
        unlike everything else on this dashboard which is student-
        owned data -- so this widget is read-only in a stronger
        sense than the others: the student can't edit any of it
        from here, only see it.
        """

        course_summaries = []
        total_present = 0
        total_countable = 0

        for student_course in current_student_courses:
            summary = AttendanceSelector.calculate_summary(student_course)

            course_summaries.append({
                "course_code": student_course.program_course.course_code,
                "course_title": student_course.program_course.course.title,
                **summary,
            })

            total_present += summary["present_count"]
            total_countable += summary["present_count"] + summary["absent_count"]

        overall_percentage = (
            round((total_present / total_countable) * 100, 2)
            if total_countable > 0
            else 0.0
        )

        # 75% is a common institutional eligibility threshold;
        # adjust if your universities use a different figure.
        at_risk_courses = [
            c["course_code"]
            for c in course_summaries
            if c["total_sessions"] > 0 and c["attendance_percentage"] < 75
        ]

        return {
            "overall_percentage": overall_percentage,
            "courses": course_summaries,
            "at_risk_courses": at_risk_courses,
        }