from apps.students.models import StudentProfile
from apps.students.selectors.transcript_selector import TranscriptSelector
from apps.students.models.student_course import CourseStatus
from decimal import Decimal
from apps.academic.services.grading_service import GradingService


class TranscriptService:
    """
    Service responsible for transcript business logic.
    """

    @staticmethod
    def get_transcript(
        student: StudentProfile,
    ):
        """
        Return transcript data for a student.
        """

        student_courses = (
            TranscriptSelector.list_student_courses(student)
        )

        earned_credit_hours = (
            TranscriptService._calculate_earned_credit_hours(
                student_courses
            )
        )

        attempted_credit_hours = (
            TranscriptService._calculate_attempted_credit_hours(
                student_courses
            )
        )

        cgpa = TranscriptService._calculate_cgpa(
            student=student,
            student_courses=student_courses,
        )

        semester_results = (
            TranscriptService._build_semester_results(
                student
            )
        )

        return {
            "student": student,
            "summary": {
                "earned_credit_hours": earned_credit_hours,
                "attempted_credit_hours": attempted_credit_hours,
                "cgpa": cgpa,
            },
            "semesters": semester_results,
            "courses": student_courses,
        }


    @staticmethod
    def _calculate_earned_credit_hours(
        student_courses,
    ) -> int:
        """
        Calculate the total earned credit hours.

        Only passed courses contribute to earned credits.
        """

        return sum(
            student_course.program_course.total_credit_hours
            for student_course in student_courses
            if student_course.status == CourseStatus.PASSED
        )


    @staticmethod
    def _calculate_attempted_credit_hours(
        student_courses,
    ) -> int:
        """
        Calculate the total attempted credit hours.
        """

        return sum(
            student_course.program_course.total_credit_hours
            for student_course in student_courses
        )

    @staticmethod
    def _calculate_semester_gpa(
        student: StudentProfile,
        enrollment,
    ) -> Decimal:
        """
        Calculate GPA for a single semester.
        """

        total_quality_points = Decimal("0")
        attempted_credit_hours = 0

        completed_statuses = (
            CourseStatus.PASSED,
            CourseStatus.FAILED,
        )

        for student_course in enrollment.student_courses.all():

            if student_course.status not in completed_statuses:
                continue

            if student_course.marks is None:
                continue

            credit_hours = (
                student_course.program_course.total_credit_hours
            )

            total_quality_points += (
                GradingService.calculate_quality_points(
                    student=student,
                    marks=student_course.marks,
                    credit_hours=credit_hours,
                )
            )

            attempted_credit_hours += credit_hours

        if attempted_credit_hours == 0:
            return Decimal("0.00")

        return (
            total_quality_points
            / Decimal(attempted_credit_hours)
        ).quantize(
            Decimal("0.00")
        )

    @staticmethod
    def _calculate_cgpa(
        student: StudentProfile,
        student_courses,
    ) -> Decimal:
        """
        Calculate the student's cumulative GPA.
        """

        total_quality_points = Decimal("0")
        attempted_credit_hours = 0

        completed_statuses = (
            CourseStatus.PASSED,
            CourseStatus.FAILED,
        )

        for student_course in student_courses:

            if student_course.status not in completed_statuses:
                continue

            if student_course.marks is None:
                continue

            credit_hours = (
                student_course.program_course.total_credit_hours
            )

            total_quality_points += (
                GradingService.calculate_quality_points(
                    student=student,
                    marks=student_course.marks,
                    credit_hours=credit_hours,
                )
            )

            attempted_credit_hours += credit_hours

        if attempted_credit_hours == 0:
            return Decimal("0.00")

        return (
            total_quality_points
            / Decimal(attempted_credit_hours)
        ).quantize(Decimal("0.00"))

    @staticmethod
    def _build_semester_results(
        student: StudentProfile,
    ):
        """
        Build semester-wise transcript data.
        """

        semesters = []

        enrollments = (
            TranscriptSelector.list_enrollments(student)
        )

        for enrollment in enrollments:

            student_courses = list(
                enrollment.student_courses.all()
            )

            earned_credit_hours = sum(
                course.program_course.total_credit_hours
                for course in student_courses
                if course.status == CourseStatus.PASSED
            )

            attempted_credit_hours = sum(
                course.program_course.total_credit_hours
                for course in student_courses
            )

            semesters.append(
                {
                    "semester": enrollment.semester,
                    "academic_session": (
                        enrollment.academic_session.display_name
                    ),
                    "gpa": (
                        TranscriptService._calculate_semester_gpa(
                            student,
                            enrollment,
                        )
                    ),
                    "earned_credit_hours": earned_credit_hours,
                    "attempted_credit_hours": attempted_credit_hours,
                    "courses": student_courses,
                }
            )

        return semesters