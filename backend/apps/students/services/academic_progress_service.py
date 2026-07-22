from decimal import Decimal

from apps.students.models import StudentProfile
from apps.students.models.student_course import CourseStatus
from apps.students.selectors.enrollment_selector import EnrollmentSelector
from apps.students.selectors.transcript_selector import TranscriptSelector
from apps.academic.selectors.program_selector import ProgramSelector
from apps.academic.services.grading_service import GradingService


class AcademicProgressService:
    """
    Builds the Academic Progress Dashboard for a student.

    Design principles (docs/04-academic-progress-dashboard.md):
    - Never store calculated data; everything here is derived live
      from StudentCourse (personal) and ProgramCourse (catalog).
    - The academic catalog (ProgramCourse) is the source of truth
      for what a program requires.
    - GPA figures are resolved through GradingService, which owns
      grade interpretation via the university's active GradingScheme.

    Scope: MVP dashboard only (Academic Identity, Current Semester,
    Degree Progress, CGPA, Expected Graduation). Backlog detection,
    graduation audit, timeline, and AI insights are Phase 2/3 and
    intentionally not included here yet.
    """

    @staticmethod
    def build_dashboard(student: StudentProfile) -> dict:
        student_courses = list(
            TranscriptSelector.list_student_courses(student)
        )

        return {
            "academic_identity": (
                AcademicProgressService._build_academic_identity(
                    student
                )
            ),
            "current_semester": (
                AcademicProgressService._build_current_semester(
                    student
                )
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
        }

    @staticmethod
    def _build_academic_identity(student: StudentProfile) -> dict:
        """
        Section 1 — Academic Identity. Sourced directly from
        StudentProfile; nothing here is calculated.
        """

        return {
            "university": student.university.name,
            "program": student.program.program_name,
            "current_semester": student.current_semester,
            "joined_session": student.joined_session.display_name,
            "academic_status": student.academic_status,
            "expected_graduation_date": (
                student.expected_graduation_date
            ),
        }

    @staticmethod
    def _build_current_semester(student: StudentProfile) -> dict:
        """
        Section 2 — Current Semester workload and SGPA.
        """

        enrollment = (
            EnrollmentSelector.get_current_enrollment(student)
        )

        if enrollment is None:
            return {
                "current_courses": [],
                "current_credit_hours": 0,
                "semester_gpa": Decimal("0.00"),
            }

        current_courses = list(
            enrollment.student_courses.all()
        )

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
    def _build_degree_progress(
        student: StudentProfile,
        student_courses,
    ) -> dict:
        """
        Section 3 — Degree Progress, measured against the program's
        official curriculum (ProgramCourse).
        """

        total_credit_hours = (
            ProgramSelector.get_total_credit_hours(
                student.program
            )
        )

        total_course_count = (
            ProgramSelector.get_total_course_count(
                student.program
            )
        )

        passed_courses = [
            student_course
            for student_course in student_courses
            if student_course.status == CourseStatus.PASSED
        ]

        completed_credit_hours = sum(
            student_course.program_course.total_credit_hours
            for student_course in passed_courses
        )

        completed_course_ids = {
            student_course.program_course_id
            for student_course in passed_courses
        }

        completed_course_count = len(completed_course_ids)

        remaining_credit_hours = max(
            total_credit_hours - completed_credit_hours,
            0,
        )

        remaining_course_count = max(
            total_course_count - completed_course_count,
            0,
        )

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
    def _build_performance(
        student: StudentProfile,
        student_courses,
    ) -> dict:
        """
        Section 4 — Academic Performance. MVP scope: CGPA only.
        """

        cgpa = GradingService.calculate_gpa(
            student=student,
            student_courses=student_courses,
        )

        return {
            "cgpa": cgpa,
        }