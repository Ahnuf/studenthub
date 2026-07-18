from apps.students.models import StudentProfile
from apps.students.selectors.transcript_selector import TranscriptSelector
from apps.students.models.student_course import CourseStatus


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

        cgpa = (
            TranscriptService._calculate_cgpa(
                student_courses
            )
        )

        return {
            "student": student,
            "summary": {
                "earned_credit_hours": earned_credit_hours,
                "attempted_credit_hours": attempted_credit_hours,
                "cgpa": cgpa,
            },
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
    def _calculate_cgpa(
        student_courses,
    ):
        pass